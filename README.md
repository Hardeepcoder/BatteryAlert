# Battery Alert 🔋

[![Continuous Integration](https://github.com/Hardeepcoder/BatteryAlert/actions/workflows/build.yml/badge.svg)](https://github.com/Hardeepcoder/BatteryAlert/actions/workflows/build.yml)
[![Google Play](https://img.shields.io/badge/Google_Play-Battery_Alarm_Hindi_Voice-4285F4?style=flat-square&logo=google-play&logoColor=white)](https://play.google.com/store/apps/details?id=com.hardeepcoder.batteryalert)
[![Latest Release](https://img.shields.io/github/v/release/Hardeepcoder/BatteryAlert?style=flat-square&color=10b981)](https://github.com/Hardeepcoder/BatteryAlert/releases/latest)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?style=flat-square)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Zero Telemetry](https://img.shields.io/badge/telemetry-0%25%20(100%25%20offline)-success?style=flat-square)](SECURITY.md)

An open-source, production-ready, cross-platform battery telemetry utility and mobile app for **Android**, **macOS**, and **Windows**.

Published on the Google Play Store as **[Battery Alarm Hindi Voice](https://play.google.com/store/apps/details?id=com.hardeepcoder.batteryalert)**, Battery Alert continuously monitors battery charging telemetry in real-time. When your device reaches a designated charging limit (such as 80%, 90%, or 100%) while plugged in, or drops to a critical low percentage, it delivers **native system notifications** and **multilingual voice alerts** (Hindi, Punjabi, English) so you can unplug your charger, prevent thermal buildup, and significantly extend lithium-ion battery lifespan.

---

## 📱 Google Play Store Release

The official Android edition is published and maintained on the Google Play Store:

👉 **[Download "Battery Alarm Hindi Voice" on Google Play](https://play.google.com/store/apps/details?id=com.hardeepcoder.batteryalert)**

* **Package ID**: `com.hardeepcoder.batteryalert`
* **Supported OS**: Android 8.0 (Oreo) through Android 15
* **Zero Telemetry**: No third-party ad networks, no analytics tracking, no internet permissions required.

---

## 🎯 Why Battery Alert?

Modern lithium-ion laptop and smartphone batteries experience maximum electrochemical stress when held at **100% state of charge (SoC)** while plugged into continuous wall power. Academic battery research demonstrates that limiting charging cycles to **80%–90%** can double or triple long-term battery cell health and usable cycle count.

Battery Alert operates with a **zero-telemetry, local-first philosophy**:
- **0% Background CPU**: Event-driven polling avoids draining the battery while monitoring it.
- **100% Offline**: No network tracking, no account registration, no analytics.
- **Multilingual Native Audio**: Human voice alerts recorded in Hindi (हिंदी), Punjabi (ਪੰਜਾਬੀ), and English.

---

## 🏗️ Architecture & Permissions Breakdown

### 🤖 Android Architecture
The Android edition is built around an efficient, event-driven foreground architecture:

1. **Telemetry Receiver (`ACTION_BATTERY_CHANGED`)**:
   - Listens to Android OS battery broadcast intents (`Intent.ACTION_BATTERY_CHANGED`, `ACTION_POWER_CONNECTED`, `ACTION_POWER_DISCONNECTED`).
   - Dynamically evaluates battery percentage, charging current, voltage, and battery temperature without wake-lock battery drain.

2. **Android Permissions**:
   - `android.permission.FOREGROUND_SERVICE` & `FOREGROUND_SERVICE_SPECIAL_USE`: Ensures the battery monitoring loop remains active while plugged in, preventing premature termination by Android Doze mode or OEM aggressive task killers.
   - `android.permission.POST_NOTIFICATIONS`: Android 13+ (API 33) runtime permission for heads-up charging alerts.
   - `android.permission.RECEIVE_BOOT_COMPLETED`: Restores background protection automatically whenever your device restarts.
   - `android.permission.VIBRATE`: Provides haptic feedback alongside audio alerts.

### 💻 Desktop Engine (macOS & Windows)
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

- 🎯 **Configurable Alert Thresholds**: Trigger alerts at **70%**, **75%**, **80%**, **85%**, **90%**, **95%**, or **100%**.
- 🗣️ **Multilingual Voice Selection**:
  - **Hindi (हिंदी)** (Female / Male)
  - **Punjabi (ਪੰਜਾਬੀ)** (Female / Male)
  - **English** (Female / Male)
- 🔊 **Three-Stage Loudness Booster**: Normal, High, and Maximum audio amplification to guarantee you hear alerts even in noisy environments.
- ⏱️ **Smart Anti-Spam Reminders**: Configurable repeat intervals (**Alert Once**, **2 Min**, **5 Min**, **10 Min**, **15 Min**, **30 Min**) capped at 3 alerts per charging session.
- 🤫 **Silent Tray / Menu Bar Operation**: Runs quietly in the macOS menu bar or Windows system tray with zero desktop clutter.
- 🚀 **Auto-Launch on Startup**: Native macOS `LaunchAgent` and Windows Registry startup hook.
- 🛡️ **Subprocess Isolation**: Audio playback and notifications run in detached worker threads to prevent UI freezes.

---

## 📥 Downloads & Ecosystem Packages

Download pre-compiled packages directly from [GitHub Releases](https://github.com/Hardeepcoder/BatteryAlert/releases/latest).

| Platform | Format / Type | Direct Download Link |
| :--- | :--- | :--- |
| 🤖 **Android (Google Play)** | Official Play Store Release | [📱 Install from Google Play](https://play.google.com/store/apps/details?id=com.hardeepcoder.batteryalert) |
| 🤖 **Android (APK Direct)** | APK Package (Android 8.0+) | [📥 Download BatteryAlert-Android-v1.0.0.apk](https://github.com/Hardeepcoder/BatteryAlert/releases/latest) |
| 🍏 **macOS (Apple Silicon)** | M1/M2/M3/M4 Disk Image | [📥 Download BatteryAlert-macOS-AppleSilicon.dmg](https://github.com/Hardeepcoder/BatteryAlert/releases/latest) |
| 🍏 **macOS (Intel)** | Intel x86_64 Disk Image | [📥 Download BatteryAlert-macOS-Intel.dmg](https://github.com/Hardeepcoder/BatteryAlert/releases/latest) |
| 🪟 **Windows** | Setup Installer (`.exe`) | [📥 Download BatteryAlertSetup.exe](https://github.com/Hardeepcoder/BatteryAlert/releases/latest) |

---

## 💻 Local Build & Developer Setup

### 🤖 Android (Gradle Build)
To build the Android companion app locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Hardeepcoder/BatteryAlert.git
   cd BatteryAlert
   ```

2. **Build Debug APK via Gradle:**
   ```bash
   ./gradlew assembleDebug
   ```

3. **Run Unit Tests:**
   ```bash
   ./gradlew test
   ```

4. **Generate Release Bundle (AAB for Google Play):**
   ```bash
   ./gradlew bundleRelease
   ```
*(You can also open the project directory directly in **Android Studio** and click **Run**).*

### 💻 Desktop (Python Engine)

#### Quickstart Setup
```bash
# 1. Create isolated virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Run unit test suite
python3 -m unittest discover tests -v

# 4. Launch desktop application
python3 app.py
```

#### Packaging Desktop Binaries

* **Windows Setup Installer**:
  ```cmd
  pyinstaller --noconfirm --onedir --windowed --name "BatteryAlert" ^
    --icon "icon/app.ico" ^
    --add-data "assets;assets" ^
    --add-data "config;config" ^
    --add-data "icon;icon" ^
    app.py

  iscc installer.iss
  ```

* **macOS DMG (Apple Silicon & Intel)**:
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

Battery Alert runs automated matrix testing across **Ubuntu, macOS, and Windows** across Python 3.9–3.12 on every push and pull request via [GitHub Actions](.github/workflows/build.yml).

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

- **`v1.4.1`**: Enhanced open-source maintainer readiness: added cross-platform unit test suite, `SECURITY.md`, `CONTRIBUTING.md`, issue triage templates, and expanded Google Play documentation.
- **`v1.4.0`**: Added macOS AppKit NSPanel native settings modal, drag-and-drop Applications DMG layout, and Android APK companion release integration.
- **`v1.1.0`**: Split macOS builds into independent Intel and Apple Silicon native DMGs; introduced thread-safe Cocoa loop handling.
- **`v1.0.2`**: Full Windows Inno Setup installer integration with Microsoft Store `/VERYSILENT` switches.
- **`v1.0.0`**: Initial release with voice selection, customizable alert thresholds, and automated CI build pipeline.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

Developed with ❤️ by **Coding's Art - HardeepCoder** • [codingsart.com](https://codingsart.com)
