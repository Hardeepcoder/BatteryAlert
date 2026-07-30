# Battery Alert 🔋

[![Build & Release](https://github.com/Hardeepcoder/BatteryAlert/actions/workflows/build.yml/badge.svg)](https://github.com/Hardeepcoder/BatteryAlert/actions/workflows/build.yml)
[![Latest Release](https://img.shields.io/github/v/release/Hardeepcoder/BatteryAlert?style=flat-square&color=10b981)](https://github.com/Hardeepcoder/BatteryAlert/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A lightweight, production-ready cross-platform background utility for **Windows** and **macOS**. 

Battery Alert monitors your laptop's battery charging telemetry in real-time. When your battery reaches a configurable charge level while plugged in, it alerts you using **native operating system notifications** and **voice alerts** so you can unplug your charger and preserve battery health.

---

## 📸 Screenshots

*(Screenshots placeholder)*

```text
+-------------------------------------------------------------+
|                     BATTERY ALERT                           |
|  [Menu Bar / System Tray Icon] -> [Native Settings Modal]   |
+-------------------------------------------------------------+
```

---

## ✨ Features

- 🤫 **Silent Background Operation**: Runs quietly in the macOS menu bar or Windows system tray.
- 🎯 **Configurable Alert Levels**: Set alerts at **80%**, **90%**, **95%**, or **100%**.
- 🗣️ **Voice Selection**: Choose between **Female** and **Male** voice alerts.
- 🔔 **Alert Types**: Support for **Voice + Notification**, **Voice Only**, or **Notification Only**.
- ⏱️ **Smart Reminders**: Optional reminder intervals (**Alert Once**, **5 Minutes**, **10 Minutes**, **15 Minutes**) — up to 3 alerts max per charging session.
- 🚀 **Launch on Startup**: Option to automatically start on system boot.
- ⚡ **Ultra-Low Resource Footprint**: Built with Python standard library and lightweight hooks — uses near 0% CPU and minimal RAM.

---

## 📦 Installation

Download pre-compiled installers directly from our official [GitHub Releases](https://github.com/Hardeepcoder/BatteryAlert/releases/latest).

### 🪟 Windows Setup
1. Download **`BatteryAlert.exe`** from [Releases](https://github.com/Hardeepcoder/BatteryAlert/releases/latest).
2. Double-click `BatteryAlert.exe` to run.
3. Look for the battery icon in your Windows System Tray (near the clock).

### 🍎 macOS Setup
1. Download **`BatteryAlert.dmg`** from [Releases](https://github.com/Hardeepcoder/BatteryAlert/releases/latest).
2. Open `BatteryAlert.dmg` and drag `BatteryAlert.app` to your **Applications** folder.
3. Launch `BatteryAlert` from Applications. It will appear in your top Menu Bar.

---

## 💻 Building from Source

### Requirements
- Python 3.9+
- macOS 11+ or Windows 10/11

### Setup Steps
```bash
# 1. Clone the repository
git clone https://github.com/Hardeepcoder/BatteryAlert.git
cd BatteryAlert

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run application locally
python app.py
```

### Packaging Executables

- **Windows Executable**:
  ```cmd
  pyinstaller --noconfirm --onefile --windowed --name "BatteryAlert" --icon "icon/app.ico" --add-data "assets;assets" --add-data "config;config" --add-data "icon;icon" app.py
  ```

- **macOS DMG**:
  ```bash
  pyinstaller --noconfirm --onedir --windowed --name "BatteryAlert" --icon "icon/app.icns" --add-data "assets:assets" --add-data "config:config" --add-data "icon:icon" app.py
  hdiutil create -volname "BatteryAlert" -srcfolder "dist/BatteryAlert.app" -ov -format UDZO "dist/BatteryAlert.dmg"
  ```

---

## 📜 Version History

- **`v1.0.0`**: Initial official release with native macOS Cocoa dialogs, Windows system tray, voice selection, customizable alert thresholds, and automated GitHub Release CI pipeline.

---

## 🗺️ Roadmap

- [ ] Custom WAV file voice uploads.
- [ ] Low battery percentage alert option (e.g. alert when battery drops below 20%).
- [ ] Linux desktop support via LibNotify and AppIndicator.

---

## ❓ Frequently Asked Questions (FAQ)

#### Q: Does Battery Alert work if Launch on Startup is disabled?
**A:** Yes! If Launch on Startup is OFF, the app works whenever you manually launch `BatteryAlert`. If enabled, it automatically starts in the background whenever you turn on your laptop.

#### Q: Will it alert if my laptop is running on battery power?
**A:** No. Alerts are triggered **only when the charger is connected** and the battery reaches your configured charge level.

#### Q: How do I stop or exit the application?
**A:** Right-click the battery icon in your macOS Menu Bar or Windows System Tray and select **Exit**.

---

## 🤝 Contribution

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Hardeepcoder/BatteryAlert/issues).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

Developed by **Coding's Art - HardeepCoder** • [codingsart.com](https://codingsart.com)
