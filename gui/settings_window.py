"""Native settings UI module for macOS (AppKit) and Windows (Tkinter)."""

import os
import sys
import webbrowser
from typing import Callable, Optional, Dict, Any

from settings import (
    SettingsManager,
    VALID_BATTERY_LEVELS,
    VALID_VOICES,
    VALID_ALERT_TYPES,
    VALID_REMINDERS,
)
from startup import StartupManager

# Try AppKit for native macOS UI
HAS_APPKIT = False
if sys.platform == "darwin":
    try:
        import AppKit
        import objc
        HAS_APPKIT = True
    except ImportError:
        HAS_APPKIT = False

# Try Tkinter for Windows UI
HAS_TKINTER = False
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    HAS_TKINTER = True
except ImportError:
    tk = None
    ttk = None
    messagebox = None


def show_mac_native_settings(settings_manager: SettingsManager, on_save_callback: Optional[Callable[[], None]] = None) -> None:
    """Display native macOS AppKit Cocoa settings popup dialog."""
    if not HAS_APPKIT:
        return

    current = settings_manager.get_all()

    alert = AppKit.NSAlert.alloc().init()
    alert.setMessageText_("Battery Alert Settings")
    alert.setInformativeText_(
        "A Lightweight utility for Apple mac\n\n"
        "Developed by: Coding's Art - HardeepCoder\n"
        "Website: https://codingsart.com"
    )

    accessory = AppKit.NSView.alloc().initWithFrame_(AppKit.NSMakeRect(0, 0, 320, 200))

    # 1. Battery Alert Level
    lbl1 = AppKit.NSTextField.labelWithString_("Battery Alert Level:")
    lbl1.setFrame_(AppKit.NSMakeRect(0, 160, 140, 24))
    pop1 = AppKit.NSPopUpButton.alloc().initWithFrame_pullsDown_(AppKit.NSMakeRect(150, 158, 160, 26), False)
    pop1.addItemsWithTitles_([f"{v}%" for v in VALID_BATTERY_LEVELS])
    pop1.selectItemWithTitle_(f"{current.get('battery_level', 100)}%")

    # 2. Voice Selection
    lbl2 = AppKit.NSTextField.labelWithString_("Alert Voice:")
    lbl2.setFrame_(AppKit.NSMakeRect(0, 120, 140, 24))
    pop2 = AppKit.NSPopUpButton.alloc().initWithFrame_pullsDown_(AppKit.NSMakeRect(150, 118, 160, 26), False)
    pop2.addItemsWithTitles_(VALID_VOICES)
    pop2.selectItemWithTitle_(current.get("voice", "Female"))

    # 3. Alert Type
    lbl3 = AppKit.NSTextField.labelWithString_("Alert Type:")
    lbl3.setFrame_(AppKit.NSMakeRect(0, 80, 140, 24))
    pop3 = AppKit.NSPopUpButton.alloc().initWithFrame_pullsDown_(AppKit.NSMakeRect(150, 78, 160, 26), False)
    pop3.addItemsWithTitles_(VALID_ALERT_TYPES)
    pop3.selectItemWithTitle_(current.get("alert_type", "Voice + Notification"))

    # 4. Reminder Frequency
    lbl4 = AppKit.NSTextField.labelWithString_("Reminder Interval:")
    lbl4.setFrame_(AppKit.NSMakeRect(0, 40, 140, 24))
    pop4 = AppKit.NSPopUpButton.alloc().initWithFrame_pullsDown_(AppKit.NSMakeRect(150, 38, 160, 26), False)
    pop4.addItemsWithTitles_(VALID_REMINDERS)
    pop4.selectItemWithTitle_(current.get("reminder", "5 Minutes"))

    # 5. Launch on Startup
    chk5 = AppKit.NSButton.alloc().initWithFrame_(AppKit.NSMakeRect(0, 5, 300, 24))
    chk5.setButtonType_(AppKit.NSButtonTypeSwitch)
    chk5.setTitle_("Launch on Startup")
    chk5.setState_(AppKit.NSControlStateValueOn if current.get("startup", False) else AppKit.NSControlStateValueOff)

    accessory.addSubview_(lbl1)
    accessory.addSubview_(pop1)
    accessory.addSubview_(lbl2)
    accessory.addSubview_(pop2)
    accessory.addSubview_(lbl3)
    accessory.addSubview_(pop3)
    accessory.addSubview_(lbl4)
    accessory.addSubview_(pop4)
    accessory.addSubview_(chk5)

    alert.setAccessoryView_(accessory)
    alert.addButtonWithTitle_("Save Settings")
    alert.addButtonWithTitle_("Cancel")
    alert.addButtonWithTitle_("🌐 codingsart.com")

    # Make application frontmost for dialog popup
    AppKit.NSApp.activateIgnoringOtherApps_(True)
    res = alert.runModal()

    if res == AppKit.NSAlertFirstButtonReturn:
        # Save Settings clicked
        selected_bat = int(pop1.titleOfSelectedItem().replace("%", "").strip())
        selected_voice = pop2.titleOfSelectedItem()
        selected_type = pop3.titleOfSelectedItem()
        selected_rem = pop4.titleOfSelectedItem()
        selected_start = (chk5.state() == AppKit.NSControlStateValueOn)

        new_config = {
            "battery_level": selected_bat,
            "voice": selected_voice,
            "alert_type": selected_type,
            "reminder": selected_rem,
            "startup": selected_start,
        }
        settings_manager.save(new_config)
        StartupManager.sync(selected_start)
        if on_save_callback:
            on_save_callback()

    elif res == AppKit.NSAlertThirdButtonReturn:
        # Visit Website clicked
        webbrowser.open("https://codingsart.com")


class SettingsWindow:
    """Settings launcher using native AppKit Cocoa on macOS or Tkinter on Windows."""

    def __init__(self, parent_root: Optional[Any], settings_manager: SettingsManager, on_save_callback: Optional[Callable[[], None]] = None) -> None:
        self._parent = parent_root
        self._settings_manager = settings_manager
        self._on_save_callback = on_save_callback
        self._window: Optional[Any] = None

    def show(self) -> None:
        """Bring up native settings popup dialog."""
        if sys.platform == "darwin" and HAS_APPKIT:
            show_mac_native_settings(self._settings_manager, self._on_save_callback)
            return

        if HAS_TKINTER:
            try:
                if self._window is not None:
                    self._window.deiconify()
                    self._window.lift()
                    self._window.focus_force()
                    return
                self._create_tkinter_window()
                return
            except Exception as e:
                print(f"Tkinter launch failed: {e}")

    def _create_tkinter_window(self) -> None:
        """Construct Tkinter window for Windows/Linux."""
        if self._parent is not None:
            window = tk.Toplevel(self._parent)
        else:
            window = tk.Tk()

        self._window = window
        window.title("Battery Alert Settings")
        window.resizable(False, False)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_png = os.path.join(base_dir, "icon", "app.png")
        if os.path.exists(icon_png):
            try:
                icon_img = tk.PhotoImage(file=icon_png)
                window.iconphoto(False, icon_img)
            except Exception:
                pass

        window.protocol("WM_DELETE_WINDOW", self._on_close)

        current_settings = self._settings_manager.get_all()

        container = ttk.Frame(window, padding="20 20 20 20")
        container.grid(row=0, column=0, sticky="NSEW")

        title_label = ttk.Label(
            container,
            text="Battery Alert Settings",
            font=("Helvetica", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 2), sticky="W")

        tagline = "A Lightweight utility for Windows"
        sub_label = ttk.Label(
            container,
            text=tagline,
            font=("Helvetica", 9, "italic")
        )
        sub_label.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky="W")

        # 1. Battery Alert Level
        ttk.Label(container, text="Battery Alert Level:", font=("Helvetica", 10)).grid(
            row=2, column=0, sticky="W", pady=8
        )
        self._battery_var = tk.IntVar(value=current_settings.get("battery_level", 100))
        battery_combo = ttk.Combobox(
            container,
            textvariable=self._battery_var,
            values=[f"{val}%" for val in VALID_BATTERY_LEVELS],
            state="readonly",
            width=20,
        )
        battery_combo.set(f"{current_settings.get('battery_level', 100)}%")
        battery_combo.grid(row=2, column=1, sticky="E", pady=8, padx=(10, 0))

        # 2. Voice Selection
        ttk.Label(container, text="Alert Voice:", font=("Helvetica", 10)).grid(
            row=3, column=0, sticky="W", pady=8
        )
        self._voice_var = tk.StringVar(value=current_settings.get("voice", "Female"))
        voice_combo = ttk.Combobox(
            container,
            textvariable=self._voice_var,
            values=VALID_VOICES,
            state="readonly",
            width=20,
        )
        voice_combo.grid(row=3, column=1, sticky="E", pady=8, padx=(10, 0))

        # 3. Alert Type
        ttk.Label(container, text="Alert Type:", font=("Helvetica", 10)).grid(
            row=4, column=0, sticky="W", pady=8
        )
        self._alert_type_var = tk.StringVar(value=current_settings.get("alert_type", "Voice + Notification"))
        alert_combo = ttk.Combobox(
            container,
            textvariable=self._alert_type_var,
            values=VALID_ALERT_TYPES,
            state="readonly",
            width=20,
        )
        alert_combo.grid(row=4, column=1, sticky="E", pady=8, padx=(10, 0))

        # 4. Reminder Frequency
        ttk.Label(container, text="Reminder Interval:", font=("Helvetica", 10)).grid(
            row=5, column=0, sticky="W", pady=8
        )
        self._reminder_var = tk.StringVar(value=current_settings.get("reminder", "5 Minutes"))
        reminder_combo = ttk.Combobox(
            container,
            textvariable=self._reminder_var,
            values=VALID_REMINDERS,
            state="readonly",
            width=20,
        )
        reminder_combo.grid(row=5, column=1, sticky="E", pady=8, padx=(10, 0))

        # 5. Launch on Startup
        ttk.Label(container, text="Launch on Startup:", font=("Helvetica", 10)).grid(
            row=6, column=0, sticky="W", pady=8
        )
        self._startup_var = tk.BooleanVar(value=current_settings.get("startup", False))
        startup_check = ttk.Checkbutton(
            container,
            text="Enabled" if self._startup_var.get() else "Disabled",
            variable=self._startup_var,
            command=self._toggle_startup_label,
        )
        self._startup_check = startup_check
        startup_check.grid(row=6, column=1, sticky="E", pady=8, padx=(10, 0))

        # Separator
        ttk.Separator(container, orient="horizontal").grid(
            row=7, column=0, columnspan=2, sticky="EW", pady=15
        )

        # Action Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=8, column=0, columnspan=2, sticky="E")

        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self._on_close)
        cancel_btn.pack(side="right", padx=(5, 0))

        save_btn = ttk.Button(btn_frame, text="Save Settings", command=self._save_settings)
        save_btn.pack(side="right")

        window.update_idletasks()
        w = window.winfo_width()
        h = window.winfo_height()
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        window.geometry(f"+{x}+{y}")
        window.lift()
        window.focus_force()

        if self._parent is None:
            window.mainloop()

    def _toggle_startup_label(self) -> None:
        if hasattr(self, "_startup_check"):
            self._startup_check.config(text="Enabled" if self._startup_var.get() else "Disabled")

    def _save_settings(self) -> None:
        try:
            raw_battery = str(self._battery_var.get()).replace("%", "").strip()
            battery_level = int(raw_battery)

            new_config = {
                "battery_level": battery_level,
                "voice": self._voice_var.get(),
                "alert_type": self._alert_type_var.get(),
                "reminder": self._reminder_var.get(),
                "startup": bool(self._startup_var.get()),
            }

            self._settings_manager.save(new_config)
            StartupManager.sync(new_config["startup"])

            if self._on_save_callback:
                self._on_save_callback()

            self._on_close()

        except Exception as e:
            if messagebox:
                messagebox.showerror("Error", f"Failed to save settings: {e}")

    def _on_close(self) -> None:
        if self._window is not None:
            try:
                self._window.destroy()
            except Exception:
                pass
            self._window = None
