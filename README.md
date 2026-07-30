# Battery Alert (Windows + macOS)

A lightweight, production-ready background utility that monitors laptop battery status and notifies you with native notifications and voice alerts when your battery reaches your target charge level while plugged in.

---

## Features

- **Silent Background Operation**: Runs quietly in system tray (Windows) or menu bar (macOS).
- **Customizable Alert Levels**: 80%, 90%, 95%, or 100%.
- **Voice Selection**: Choose between Female and Male voice alerts.
- **Alert Types**: Voice Only, Notification Only, or Voice + Notification.
- **Smart Reminders**: Remind every 5, 10, or 15 minutes (up to 3 alerts max per charging session).
- **Launch on Startup**: Optional auto-start on system login.
- **Zero Heavy Frameworks**: Ultra-low CPU and RAM footprint.

---

## Directory Structure

```text
BatteryAlert/
    app.py                  # Main entry point & background loop controller
    battery.py              # Battery status reader using psutil
    notifier.py             # Native macOS / Windows notification integration
    audio.py                # Asynchronous voice alert player
    settings.py             # JSON config persistence manager
    startup.py              # Launch-on-startup system configuration
    tray.py                 # System tray (Windows) / Menu bar (macOS) manager
    gui/
        settings_window.py  # Tkinter Settings UI
    assets/
        female.wav          # Female voice wave file
        male.wav            # Male voice wave file
    config/
        settings.json       # Persistent user settings
    icon/
        app.png             # Application icon
        app.ico             # Windows executable icon
        app.icns            # macOS app bundle icon
    requirements.txt        # Lightweight dependencies
    README.md               # Documentation
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- macOS or Windows 10/11

### Installation

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run application:
   ```bash
   python app.py
   ```

---

## Building Executables

### Packaging for Windows (.exe)

Using PyInstaller on Windows:

```cmd
pyinstaller --noconfirm --onedir --windowed --name "BatteryAlert" ^
    --icon "icon/app.ico" ^
    --add-data "assets;assets" ^
    --add-data "config;config" ^
    --add-data "icon;icon" ^
    app.py
```

The resulting `BatteryAlert.exe` will be located inside the `dist/BatteryAlert` directory.

### Packaging for macOS (.dmg)

1. Package `.app` bundle using PyInstaller on macOS:
   ```bash
   pyinstaller --noconfirm --onedir --windowed --name "BatteryAlert" \
       --icon "icon/app.icns" \
       --add-data "assets:assets" \
       --add-data "config:config" \
       --add-data "icon:icon" \
       app.py
   ```

2. Create `.dmg` disk image using `create-dmg`:
   ```bash
   create-dmg \
     --volname "BatteryAlert Installer" \
     --volicon "icon/app.icns" \
     --window-pos 200 120 \
     --window-size 800 400 \
     --icon-size 100 \
     --icon "BatteryAlert.app" 200 190 \
     --hide-extension "BatteryAlert.app" \
     --app-drop-link 600 190 \
     "dist/BatteryAlert.dmg" \
     "dist/"
   ```

---

## License

MIT License.
