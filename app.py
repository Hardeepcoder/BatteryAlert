"""Main application loop and orchestrator for Battery Alert utility."""

import os
import sys
import time
import threading
import webbrowser
import socket
from typing import Optional, Dict, Any

if sys.platform == "darwin":
    try:
        import AppKit
        from Foundation import NSObject
        import objc

        class MainThreadScheduler(NSObject):
            @objc.signature(b'v@:@')
            def execute_(self, func):
                func()
        _scheduler = MainThreadScheduler.alloc().init()

        class AppDelegate(NSObject):
            reopen_callback = None

            @objc.signature(b'B@:@B')
            def applicationShouldHandleReopen_hasVisibleWindows_(self, sender, flag):
                if AppDelegate.reopen_callback:
                    run_on_main_thread(AppDelegate.reopen_callback)
                return True

        _app_delegate = AppDelegate.alloc().init()
        AppKit.NSApp.setDelegate_(_app_delegate)
    except Exception as e:
        print(f"AppKit setup error: {e}")
        _scheduler = None
        _app_delegate = None
else:
    _scheduler = None
    _app_delegate = None


def run_on_main_thread(func):
    """Executes a function on the macOS AppKit main thread if on darwin, otherwise runs it directly."""
    if sys.platform == "darwin" and _scheduler is not None:
        _scheduler.performSelectorOnMainThread_withObject_waitUntilDone_(
            "execute:",
            func,
            False
        )
    else:
        func()

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False
    tk = None
    ttk = None
    messagebox = None

from settings import SettingsManager
from battery import BatteryMonitor, BatteryStatus
from audio import AudioPlayer
from notifier import Notifier
from startup import StartupManager
from tray import SystemTray
from gui.settings_window import SettingsWindow


CHECK_INTERVAL_SECONDS = 30
MAX_ALERTS_PER_SESSION = 3


class BatteryAlertApp:
    """Core controller for background monitoring and user notifications."""

    def __init__(self) -> None:
        self._settings_manager = SettingsManager()
        self._audio_player = AudioPlayer()
        self._notifier = Notifier()
        self._battery_monitor = BatteryMonitor()

        # Session tracking state
        self._is_running = True
        self._was_plugged_in: Optional[bool] = None
        self._alert_count = 0
        self._last_alert_time: float = 0.0
        self._charging_session_id: int = 0
        self._alert_session_active = False

        self._root = None
        if HAS_TKINTER and sys.platform != "darwin":
            try:
                self._root = tk.Tk()
                self._root.withdraw()
            except Exception as e:
                print(f"Tkinter root initialization failed: {e}")
                self._root = None

        self._lock_socket: Optional[socket.socket] = None

        self._settings_window_instance: Optional[SettingsWindow] = None
        self._tray: Optional[SystemTray] = None
        self._monitor_thread: Optional[threading.Thread] = None

        if sys.platform == "darwin" and '_app_delegate' in globals() and _app_delegate is not None:
            AppDelegate.reopen_callback = self._schedule_open_settings

    def _check_single_instance(self) -> bool:
        """Check if another instance is already running.
        If running, notifies it via socket and returns False.
        Otherwise, starts listening socket and returns True.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('127.0.0.1', 49520))
            s.listen(5)
            self._lock_socket = s
            
            # Start background thread to listen for trigger messages from subsequent instances
            def listener():
                while self._is_running:
                    try:
                        conn, addr = s.accept()
                        data = conn.recv(1024).decode('utf-8')
                        if data == "SHOW_SETTINGS":
                            run_on_main_thread(self._schedule_open_settings)
                        conn.close()
                    except Exception:
                        break
            
            t = threading.Thread(target=listener, daemon=True)
            t.start()
            return True
        except Exception:
            # Port is already bound -> Another instance is running!
            try:
                # Notify the running instance to show its settings window
                s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s2.connect(('127.0.0.1', 49520))
                s2.sendall(b"SHOW_SETTINGS")
                s2.close()
            except Exception as e:
                print(f"Failed to notify existing instance: {e}")
            return False

    def start(self) -> None:
        """Start the background application."""
        if not self._check_single_instance():
            sys.exit(0)

        startup_enabled = self._settings_manager.get("startup", False)
        StartupManager.sync(startup_enabled)

        # Start battery monitoring loop in background daemon thread
        self._monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._monitor_thread.start()

        # Send startup notification to guide the user
        try:
            self._notifier.notify(
                "Battery Alert Running",
                "The app is running in the background. Click the icon in the top Menu Bar to open settings."
            )
        except Exception as e:
            print(f"Failed to send startup notification: {e}")

        # Automatically show settings dialogue box on startup
        self._schedule_open_settings()

        # Run system tray menu
        self._tray = SystemTray(
            on_open_settings=self._schedule_open_settings,
            on_check_battery=self.check_battery_now,
            on_show_about=self._schedule_show_about,
            on_exit=self.exit_app,
        )

        if sys.platform != "darwin" and HAS_TKINTER and self._root is not None:
            # Run system tray in background thread, keep main thread for Tkinter event loop
            self._tray.run_detached()
            try:
                self._root.mainloop()
            except KeyboardInterrupt:
                self.exit_app()
        else:
            # Fallback: run tray loop on main thread if Tkinter is unavailable (or on macOS)
            self._tray.run()

    def _schedule_open_settings(self) -> None:
        """Schedule opening settings window on the main GUI thread."""
        if HAS_TKINTER and self._root is not None:
            self._root.after(0, self.open_settings)
        else:
            self.open_settings()

    def _schedule_show_about(self) -> None:
        """Schedule opening about window on the main GUI thread."""
        if HAS_TKINTER and self._root is not None:
            self._root.after(0, self.show_about)
        else:
            self.show_about()

    def open_settings(self) -> None:
        """Open settings GUI window on demand."""
        if self._settings_window_instance is None:
            self._settings_window_instance = SettingsWindow(
                self._root,
                self._settings_manager,
                on_save_callback=self._on_settings_saved
            )
        self._settings_window_instance.show()

    def _on_settings_saved(self) -> None:
        """Callback triggered when user saves new settings."""
        print("Settings saved successfully!")

    def check_battery_now(self) -> None:
        """Manual check triggered from system tray menu."""
        status = self._battery_monitor.get_status()
        if status is None:
            self._notifier.notify("Battery Alert", "Unable to read battery status.")
            return

        plugged_str = "Plugged In (Charging)" if status.power_plugged else "Discharging (On Battery)"
        msg = f"Current Level: {status.percent}%\nStatus: {plugged_str}"
        self._notifier.notify("Battery Status", msg)

    def show_about(self) -> None:
        """Display about window information."""
        tagline = "A Lightweight utility for Apple mac" if sys.platform == "darwin" else "A Lightweight utility for Windows"

        if sys.platform == "darwin":
            try:
                import AppKit
                alert = AppKit.NSAlert.alloc().init()
                alert.setMessageText_("About Battery Alert")
                alert.setInformativeText_(
                    f"{tagline}\n\n"
                    "Developed by: Coding's Art - HardeepCoder\n"
                    "Website: https://codingsart.com"
                )
                alert.addButtonWithTitle_("OK")
                alert.addButtonWithTitle_("🌐 codingsart.com")

                win = alert.window()
                if win:
                    try:
                        win.setLevel_(AppKit.NSModalPanelWindowLevel)
                        win.center()
                        win.makeKeyAndOrderFront_(None)
                    except Exception:
                        pass

                AppKit.NSApp.activateIgnoringOtherApps_(True)
                res = alert.runModal()
                if res == AppKit.NSAlertSecondButtonReturn:
                    webbrowser.open("https://codingsart.com")
                return
            except Exception as e:
                print(f"AppKit about launch error: {e}")

        if not HAS_TKINTER or self._root is None:
            self._notifier.notify(
                "About Battery Alert",
                f"{tagline}\nCoding's Art - HardeepCoder\nhttps://codingsart.com"
            )
            return

        about_win = tk.Toplevel(self._root)
        about_win.title("About Battery Alert")
        about_win.resizable(False, False)

        # Set window icon if available
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_png = os.path.join(base_dir, "icon", "app.png")
        if os.path.exists(icon_png):
            try:
                icon_img = tk.PhotoImage(file=icon_png)
                about_win.iconphoto(False, icon_img)
            except Exception:
                pass

        container = ttk.Frame(about_win, padding="25 25 25 25")
        container.grid(row=0, column=0, sticky="NSEW")

        # Application Title
        ttk.Label(
            container,
            text="Battery Alert",
            font=("Helvetica", 16, "bold")
        ).pack(anchor="w", pady=(0, 2))

        # Tagline
        ttk.Label(
            container,
            text=tagline,
            font=("Helvetica", 10, "italic"),
            foreground="#475569"
        ).pack(anchor="w", pady=(0, 12))

        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=8)

        # Developer / Credits
        ttk.Label(
            container,
            text="Developed by:",
            font=("Helvetica", 9, "bold")
        ).pack(anchor="w", pady=(4, 2))

        ttk.Label(
            container,
            text="Coding's Art - HardeepCoder",
            font=("Helvetica", 11, "bold"),
            foreground="#0f172a"
        ).pack(anchor="w", pady=(0, 10))

        # Website Link Button
        def open_website():
            webbrowser.open("https://codingsart.com")

        link_btn = ttk.Button(
            container,
            text="🌐 Visit codingsart.com",
            command=open_website
        )
        link_btn.pack(anchor="w", pady=(0, 15))

        # Close button
        close_btn = ttk.Button(
            container,
            text="Close",
            command=about_win.destroy
        )
        close_btn.pack(anchor="e")

        about_win.update_idletasks()
        w = about_win.winfo_width()
        h = about_win.winfo_height()
        ws = about_win.winfo_screenwidth()
        hs = about_win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        about_win.geometry(f"+{x}+{y}")
        about_win.lift()
        about_win.focus_force()

    def _monitoring_loop(self) -> None:
        """Background thread checking battery every 30 seconds."""
        while self._is_running:
            try:
                self._evaluate_battery_status()
            except Exception as e:
                print(f"Error in battery evaluation loop: {e}")

            for _ in range(CHECK_INTERVAL_SECONDS):
                if not self._is_running:
                    break
                time.sleep(1)

    def _evaluate_battery_status(self) -> None:
        """Core alert logic implementation according to requirements."""
        status = self._battery_monitor.get_status()
        if status is None:
            return

        is_plugged = bool(status.power_plugged)
        percent = status.percent

        if self._was_plugged_in is True and not is_plugged:
            self._reset_alert_session()

        if self._was_plugged_in is False and is_plugged:
            self._reset_alert_session()

        self._was_plugged_in = is_plugged

        target_level = int(self._settings_manager.get("battery_level", 100))
        voice = str(self._settings_manager.get("voice", "English Female"))
        loudness = str(self._settings_manager.get("loudness", "Normal"))
        alert_type = str(self._settings_manager.get("alert_type", "Voice + Notification"))
        reminder_setting = str(self._settings_manager.get("reminder", "5 Minutes"))

        if not is_plugged or percent < target_level:
            return

        if self._alert_count >= MAX_ALERTS_PER_SESSION:
            return

        now = time.time()

        if self._alert_count == 0:
            self._trigger_alert(alert_type, voice, loudness, target_level, percent)
            self._alert_count += 1
            self._last_alert_time = now
            return

        reminder_seconds = self._parse_reminder_seconds(reminder_setting)
        if reminder_seconds is None:
            return

        if (now - self._last_alert_time) >= reminder_seconds:
            self._trigger_alert(alert_type, voice, loudness, target_level, percent, is_reminder=True)
            self._alert_count += 1
            self._last_alert_time = now

    def _parse_reminder_seconds(self, reminder_str: str) -> Optional[int]:
        """Convert reminder setting string to seconds interval."""
        if reminder_str == "2 Minutes":
            return 120
        elif reminder_str == "5 Minutes":
            return 300
        elif reminder_str == "10 Minutes":
            return 600
        elif reminder_str == "15 Minutes":
            return 900
        elif reminder_str == "30 Minutes":
            return 1800
        return None

    def _reset_alert_session(self) -> None:
        """Reset session alert count and state."""
        self._alert_count = 0
        self._last_alert_time = 0.0

    def _trigger_alert(self, alert_type: str, voice: str, loudness: str, target_level: int, current_level: float, is_reminder: bool = False) -> None:
        """Execute requested alert actions (Voice, Notification, or Both)."""
        title = "Battery Fully Charged" if target_level == 100 else f"Battery Reached {target_level}%"
        if is_reminder:
            title = f"Reminder: {title}"

        message = f"Battery level is at {current_level}%.\nYou can unplug the charger now."

        play_voice = alert_type in ("Voice Only", "Voice + Notification")
        send_notify = alert_type in ("Notification Only", "Voice + Notification")

        if play_voice:
            voice_success = self._audio_player.play(voice, loudness)
            if not voice_success and not send_notify:
                send_notify = True

        if send_notify:
            self._notifier.notify(title, message)

    def exit_app(self) -> None:
        """Cleanly terminate application."""
        self._is_running = False
        if self._tray is not None:
            self._tray.stop()
        if self._root is not None:
            try:
                self._root.quit()
            except Exception:
                pass
        sys.exit(0)


if __name__ == "__main__":
    app = BatteryAlertApp()
    app.start()
