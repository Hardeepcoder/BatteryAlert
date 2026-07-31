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

## 📥 Official Download Links

Download pre-compiled installers directly from our official [GitHub Releases](https://github.com/Hardeepcoder/BatteryAlert/releases/latest).

| Platform | Recommended Package | Direct Download Link |
| :--- | :--- | :--- |
| 🤖 **Android** | APK Package (Android 8.0+) | [📥 Download BatteryAlert-Android-v1.0.0.apk](https://github.com/Hardeepcoder/BatteryAlert/releases/download/v1.4.0/BatteryAlert-Android-v1.0.0.apk) |
| 🪟 **Windows** | Setup Installer (`.exe`) | [📥 Download BatteryAlertSetup.exe](https://github.com/Hardeepcoder/BatteryAlert/releases/download/v1.4.0/BatteryAlertSetup.exe) |
| 🍏 **macOS (Apple Silicon)** | M1/M2/M3/M4 Disk Image | [📥 Download BatteryAlert-macOS-AppleSilicon.dmg](https://github.com/Hardeepcoder/BatteryAlert/releases/download/v1.4.0/BatteryAlert-macOS-AppleSilicon.dmg) |
| 🍏 **macOS (Intel)** | Intel Mac Disk Image | [📥 Download BatteryAlert-macOS-Intel.dmg](https://github.com/Hardeepcoder/BatteryAlert/releases/download/v1.4.0/BatteryAlert-macOS-Intel.dmg) |

---

## 📦 Supported Platforms

### 🤖 Android
- **Supported OS**: Android 8.0 (Oreo) and newer (Android 9, 10, 11, 12, 13, 14, 15)
- **Features**: Automatic charging detection foreground service, `LoudnessEnhancer` audio boost (+150% / +200%), multilingual voice alerts (English, Hindi, Punjabi), dynamic Light/Dark theme toggle.

### 🪟 Windows Setup (Recommended)
1. Download **`BatteryAlertSetup.exe`** from [Releases](https://github.com/Hardeepcoder/BatteryAlert/releases/latest).
2. Double-click `BatteryAlertSetup.exe` to run the professional setup wizard.
3. The installer automatically sets up:
   - Installation to `Program Files\Battery Charge Alert`
   - Start Menu and Desktop shortcuts
   - Clean Add/Remove Programs integration & Uninstaller
4. Look for the battery icon in your Windows System Tray (near the clock).

#### 🛒 Microsoft Store & Silent Installation Switches
`BatteryAlertSetup.exe` supports fully silent, non-interactive installation suitable for **Microsoft Store EXE submission** and enterprise deployment:
- **Silent Install Command**:
  ```cmd
  BatteryAlertSetup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART
  ```
- **Silent Uninstall Command**:
  ```cmd
  "{uninstaller_path}" /VERYSILENT /NORESTART
  ```
- **Installer Return Codes**:
  - `0`: Success (Installation completed successfully)
  - `1`: Cancelled (User cancelled the installation or clicked Cancel)
  - `2`: Reboot required (Installation succeeded but requires a system reboot)
  - `3`: Installation in progress (Another instance of setup is already running)

### 🍎 macOS Setup
We provide separate optimized packages for each macOS architecture:
- **For Intel-based Macs**: Download **`BatteryAlert-macOS-Intel.dmg`**
- **For Apple Silicon Macs (M1/M2/M3/M4)**: Download **`BatteryAlert-macOS-AppleSilicon.dmg`**

1. Open the downloaded `.dmg` file.
2. Drag `BatteryAlert.app` into your **Applications** folder.
3. **First Launch (macOS Security Bypass)**:
   - In Finder, open **Applications** ➔ **Right-Click** (or `Control + Click`) on **BatteryAlert.app** and select **Open**.
   - Click **Open** on the prompt. (Or run `xattr -cr /Applications/BatteryAlert.app` in Terminal).

---

## 💻 Building from Source

### Requirements
- Python 3.9+
- macOS 11+ or Windows 10/11
- Inno Setup 6 (for Windows `.exe` installer compilation)

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

### Packaging Executables & Installers

- **Windows Setup Installer (`BatteryAlertSetup.exe`)**:
  ```cmd
  pyinstaller --noconfirm --onedir --windowed --name "BatteryAlert" --icon "icon/app.ico" --add-data "assets;assets" --add-data "config;config" --add-data "icon;icon" app.py
  iscc installer.iss
  ```

- **macOS Disk Image (`BatteryAlert-macOS-Intel.dmg` or `BatteryAlert-macOS-AppleSilicon.dmg`)**:
  ```bash
  pyinstaller --noconfirm --onedir --windowed --name "BatteryAlert" --icon "icon/app.icns" --add-data "assets:assets" --add-data "config:config" --add-data "icon:icon" --hidden-import "AppKit" --hidden-import "objc" app.py
  hdiutil create -volname "BatteryAlert" -srcfolder "dist/BatteryAlert.app" -ov -format UDZO "dist/BatteryAlert-<suffix>.dmg"
  ```

---

## 🚀 Release Process & GitHub Actions

The repository has an automated CI/CD pipeline configured with GitHub Actions:
- **Trigger**: Every time a git tag starting with `v` (e.g. `v1.1.0`) is pushed to the repository.
- **Workflow Steps**:
  1. Runs `build-windows` on `windows-latest` to compile `BatteryAlertSetup.exe`.
  2. Runs `build-macos` on `macos-15-intel` to build the Intel image `BatteryAlert-macOS-Intel.dmg`.
  3. Runs `build-macos` on `macos-latest` (Apple Silicon runner) to build `BatteryAlert-macOS-AppleSilicon.dmg`.
  4. Runs `release` on `ubuntu-latest` to download all three built assets, calculate their SHA-256 checksums, and publish them to a new GitHub Release with the checksum details appended to the release description.

---

## 📜 Version History

- **`v1.1.0`**: Split macOS packaging into distinct `BatteryAlert-macOS-Intel.dmg` and `BatteryAlert-macOS-AppleSilicon.dmg` packages to fix Intel compatibility. Configured AppKit Cocoa thread handling on macOS main thread. Added auto-update setting preparation structure.
- **`v1.0.2`**: Introduced official Windows Inno Setup installer with Microsoft Store silent switches, Start Menu shortcuts, clean uninstaller, and GitHub Release automation.
- **`v1.0.0`**: Initial release with native macOS Cocoa dialogs, Windows system tray, voice selection, customizable alert thresholds, and automated GitHub Release CI pipeline.

---

## 🗺️ Roadmap

- [ ] Microsoft Store App package submission.
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
