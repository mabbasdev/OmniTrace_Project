import os
import time
from datetime import datetime
from plyer import notification # You'll need: pip install plyer

class OmniTraceBase:
    def __init__(self, dev_mode=False):
        self.dev_mode = dev_mode
        # Hidden Root: AppData/Local/SystemConfig
        self.root = os.path.join(os.environ['LOCALAPPDATA'], "SystemConfig")
        
    def notify(self, title, message):
        """Sends alerts only during development phase"""
        if self.dev_mode:
            notification.notify(
                title=f"Omni-Trace [DEV]: {title}",
                message=message,
                timeout=3
            )

    def get_path(self):
        """Creates and returns the specific folder for the current hour"""
        now = datetime.now()
        folder_path = os.path.join(
            self.root, 
            now.strftime("%Y-%m-%d"), 
            now.strftime("%H-00")
        )
        
        # Create subfolders
        for sub in ["Logs", "Screenshots", "Webcam"]:
            os.makedirs(os.path.join(folder_path, sub), exist_ok=True)
            
        return folder_path

    def log_event(self, event_text):
        """Writes text events to the hourly log file"""
        path = os.path.join(self.get_path(), "Logs", "activity_log.txt")
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} {event_text}\n")
            
        # If in dev mode, let us know it's working
        # self.notify("Log Written", event_text[:30])


# --- TEST RUN ---
if __name__ == "__main__":
    engine = OmniTraceBase(dev_mode=False)
    engine.notify("Phase 1 Active", "Folder structure initialized.")
    engine.log_event("System initialized and monitoring started.")
    print(f"Build Phase 1 complete. Files located in: {engine.root}")