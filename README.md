# Battery Alert 🔋

[![Continuous Integration](https://github.com/Hardeepcoder/BatteryAlert/actions/workflows/ci.yml/badge.svg)](https://github.com/Hardeepcoder/BatteryAlert/actions/workflows/ci.yml)
[![Build & Release](https://github.com/Hardeepcoder/BatteryAlert/actions/workflows/build.yml/badge.svg)](https://github.com/Hardeepcoder/BatteryAlert/actions/workflows/build.yml)
[![Latest Release](https://img.shields.io/github/v/release/Hardeepcoder/BatteryAlert?style=flat-square&color=10b981)](https://github.com/Hardeepcoder/BatteryAlert/releases/latest)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?style=flat-square)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Zero Telemetry](https://img.shields.io/badge/telemetry-0%25%20(100%25%20offline)-success?style=flat-square)](SECURITY.md)

An open-source, production-ready, cross-platform background battery telemetry utility for **Windows**, **macOS**, and **Android**. 

Battery Alert continuously monitors battery telemetry in real-time. When your device reaches a designated charging limit (such as 80% or 90%) while plugged in, it delivers **native operating system notifications** and **multilingual voice alerts** (English, Hindi, Punjabi) so you can unplug your charger, prevent thermal buildup, and significantly extend lithium-ion battery lifespan.

---

## 🎯 Why Battery Alert?

Modern lithium-ion laptop and smartphone batteries experience maximum electrochemical stress when held at **100% state of charge (SoC)** while plugged into continuous wall power. Academic battery research demonstrates that limiting charging cycles to **80%–90%** can double or triple long-term battery cell health and usable cycle count.

Battery Alert operates with a **zero-telemetry, local-first philosophy**:
- **0% Background CPU**: Event-driven polling avoids draining the battery while monitoring it.
- **100% Offline**: No network tracking, no account registration, no analytics.
- **Multilingual Native Audio**: Human voice alerts recorded in English, Hindi (हिंदी), and Punjabi (ਪੰਜਾਬੀ).

---

## 🏗️ System Architecture

```text
+-----------------------------------------------------------------------+
|                         BATTERY ALERT ENGINE                          |
+-----------------------------------------------------------------------+
                                  |
               [Hardware Telemetry Polling (psutil)]
                                  |
                                  v
                    +---------------------------+
                    | BatteryStatus Telemetry   |
                    | - percent: float          |
                    | - power_plugged: bool     |
                    | - is_charging: bool       |
                    +---------------------------+
                                  |
            [Threshold & Repeating Interval Evaluation]
                                  |
                                  v
        +-----------------------------------------------+
        |               ALERT DISPATCHER                |
        +-----------------------------------------------+
               /                                 \
              v                                   v
+-----------------------------+     +-----------------------------+
|    Native OS Notification   |     |    Subprocess Audio Engine  |
| - macOS: AppKit NSPanel     |     | - Loudness Enhancer Boost   |
| - Windows: Win32 Tray Popup |     | - Multilingual WAV Assets   |
+-----------------------------+     +-----------------------------+
```

---

## ✨ Key Features

- 🤫 **Silent Tray / Menu Bar Operation**: Runs quietly in the macOS menu bar or Windows system tray with zero desktop clutter.
- 🎯 **Configurable Alert Thresholds**: Trigger alerts at **70%**, **75%**, **80%**, **85%**, **90%**, **95%**, or **100%**.
- 🗣️ **Multilingual Voice Selection**:
  - **English** (Female / Male)
  - **Hindi (हिंदी)** (Female / Male)
  - **Punjabi (ਪੰਜਾਬੀ)** (Female / Male)
- 🔊 **Three-Stage Loudness Booster**: Normal, High, and Maximum audio amplification to guarantee you hear alerts even in busy office or home environments.
- ⏱️ **Smart Anti-Spam Reminders**: Configurable repeat intervals (**Alert Once**, **2 Min**, **5 Min**, **10 Min**, **15 Min**, **30 Min**) capped at 3 alerts per charging session.
- 🚀 **Auto-Launch on Startup**: Native macOS `LaunchAgent` and Windows Registry startup hook.
- 🛡️ **Subprocess Isolation**: Audio playback and notifications run in detached worker threads to prevent UI freezes.

---

## 📥 Official Downloads & Ecosystem

Download pre-compiled packages directly from [GitHub Releases](https://github.com/Hardeepcoder/BatteryAlert/releases/latest).

| Platform | Format / Type | Direct Download Link |
| :--- | :--- | :--- |
| 🍏 **macOS (Apple Silicon)** | M1/M2/M3/M4 Disk Image | [📥 Download BatteryAlert-macOS-AppleSilicon.dmg](https://github.com/Hardeepcoder/BatteryAlert/releases/latest) |
| 🍏 **macOS (Intel)** | Intel x86_64 Disk Image | [📥 Download BatteryAlert-macOS-Intel.dmg](https://github.com/Hardeepcoder/BatteryAlert/releases/latest) |
| 🪟 **Windows** | Setup Installer (`.exe`) | [📥 Download BatteryAlertSetup.exe](https://github.com/Hardeepcoder/BatteryAlert/releases/latest) |
| 🤖 **Android Companion** | APK Package (Android 8.0+) | [📥 Download BatteryAlert-Android-v1.0.0.apk](https://github.com/Hardeepcoder/BatteryAlert/releases/latest) |

---

## 💻 Local Development & Build Guide

### Prerequisites
- Python 3.9, 3.10, 3.11, or 3.12
- macOS 11+ or Windows 10/11
- Inno Setup 6 (optional, for compiling Windows `.exe` installer)

### Quickstart Setup
```bash
# 1. Clone repository
git clone https://github.com/Hardeepcoder/BatteryAlert.git
cd BatteryAlert

# 2. Create isolated virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run test suite
python3 -m unittest discover tests -v

# 5. Launch application
python3 app.py
```

### Building Binaries

#### 🪟 Windows Setup Installer
```cmd
pyinstaller --noconfirm --onedir --windowed --name "BatteryAlert" ^
  --icon "icon/app.ico" ^
  --add-data "assets;assets" ^
  --add-data "config;config" ^
  --add-data "icon;icon" ^
  app.py

iscc installer.iss
```

#### 🍏 macOS DMG (Apple Silicon & Intel)
```bash
pyinstaller --noconfirm --onedir --windowed --name "BatteryAlert" \
  --icon "icon/app.icns" \
  --add-data "assets:assets" \
  --add-data "config:config" \
  --add-data "icon:icon" \
  --hidden-import "AppKit" \
  --hidden-import "objc" \
  app.py

hdiutil create -volname "BatteryAlert" -srcfolder "dist/BatteryAlert.app" -ov -format UDZO "dist/BatteryAlert-macOS.dmg"
```

---

## 🧪 Testing & Continuous Integration

Battery Alert runs automated matrix testing across **Ubuntu, macOS, and Windows** across Python 3.9–3.12 on every push and pull request via [GitHub Actions](.github/workflows/ci.yml).

Run all unit tests locally:
```bash
python3 -m unittest discover tests -v
```

---

## 🔒 Security & Privacy

We treat security and telemetry with the highest standard:
- **No data collection or cloud sync**: All sensor calculations occur locally on your device.
- **Responsible Disclosure**: Please review our [SECURITY.md](SECURITY.md) for vulnerability reporting guidelines.

---

## 🤝 Contributing

We welcome community feedback, pull requests, and bug reports! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting code.

---

## 📜 Version History

- **`v1.4.0`**: Added macOS AppKit NSPanel native settings modal, drag-and-drop Applications DMG layout, and Android APK companion release integration.
- **`v1.1.0`**: Split macOS builds into independent Intel and Apple Silicon native DMGs; introduced thread-safe Cocoa loop handling.
- **`v1.0.2`**: Full Windows Inno Setup installer integration with Microsoft Store `/VERYSILENT` switches.
- **`v1.0.0`**: Initial release with voice selection, customizable alert thresholds, and automated CI build pipeline.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

Developed with ❤️ by **Coding's Art - HardeepCoder** • [codingsart.com](https://codingsart.com)
