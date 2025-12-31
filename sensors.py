import win32gui
import win32process
import psutil
import time
from datetime import datetime
from pynput import keyboard
import threading

class OmniSensors:
    def __init__(self, engine):
        self.engine = engine
        self.current_window_title = ""
        self.current_pid = None
        self.start_time = time.time()

    def get_active_info(self):
        """Returns (Window Title, PID, Process Name)"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid).name()
            return title, pid, process
        except:
            return None, None, None

    def on_press(self, key):
        new_title, new_pid, new_proc = self.get_active_info()
        
        # LOGIC: Detecting Task Switching or State Changes
        if new_pid != self.current_pid or new_title != self.current_window_title:
            now = time.time()
            duration = round(now - self.start_time, 2)

            # 1. Handle the "Previous" App
            if self.current_pid:
                # Check if the process still exists in the system
                if psutil.pid_exists(self.current_pid):
                    status = "[MINIMIZED / LOST FOCUS]"
                else:
                    status = "[CLOSED / TERMINATED]"
                
                self.engine.log_event(f"\n{status}: {self.current_window_title} (Used for {duration}s)")

            # 2. Handle the "New" App (Task Switching)
            if new_pid:
                switch_msg = f"\n[SWITCHED TO / FOCUS BACK]: {new_title} ({new_proc})"
                self.engine.log_event(switch_msg)
                
                # Update State
                self.current_window_title = new_title
                self.current_pid = new_pid
                self.start_time = now
                
                if self.engine.dev_mode:
                    self.engine.notify("Task Switch", f"Active: {new_proc}")

        # Standard Keystroke Logging
        try:
            k = str(key.char)
        except AttributeError:
            k = f"[{str(key)}]"
        self.engine.log_event(k)

    def monitor_usb(self):
        # (Keep your existing USB monitoring code here...)
        pass

    def start(self):
        keyboard.Listener(on_press=self.on_press).start()
        # Add a secondary thread to check for 'silent' closes (Alt+F4 without typing)
        threading.Thread(target=self.background_state_check, daemon=True).start()

    def background_state_check(self):
        """Checks if the current window closed without a key being pressed"""
        while True:
            time.sleep(2) # Check every 2 seconds
            new_title, new_pid, _ = self.get_active_info()
            if new_pid != self.current_pid:
                # Trigger the logic by simulating a neutral event or calling a check
                # For simplicity, we can call the same logic as 'on_press' but with None
                self.on_press(None)