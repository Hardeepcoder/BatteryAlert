"""Native settings UI module for macOS (AppKit) and Windows (Tkinter)."""

import os
import sys
import webbrowser
from typing import Callable, Optional, Dict, Any

from settings import (
    SettingsManager,
    VALID_BATTERY_LEVELS,
    VALID_VOICES,
    VALID_LOUDNESS_LEVELS,
    VALID_ALERT_TYPES,
    VALID_REMINDERS,
)
from audio import AudioPlayer
from startup import StartupManager

# Try AppKit for native macOS UI
HAS_APPKIT = False
if sys.platform == "darwin":
    try:
        import AppKit
        from Foundation import NSObject
        import objc
        HAS_APPKIT = True

        class MacSettingsPanel(NSObject):
            """Native Cocoa NSPanel for macOS settings without NSAlert modal closure issues."""

            def initWithManager_player_callback_(self, settings_manager, audio_player, on_save_callback):
                self = objc.super(MacSettingsPanel, self).init()
                if self is not None:
                    self.settings_manager = settings_manager
                    self.audio_player = audio_player
                    self.on_save_callback = on_save_callback
                    self.panel = None
                return self

            @objc.signature(b'v@:@')
            def testVoice_(self, sender):
                try:
                    v_name = str(self.pop_voice.titleOfSelectedItem())
                    v_loud = str(self.pop_loudness.titleOfSelectedItem())
                    self.audio_player.play(v_name, v_loud)
                except Exception as e:
                    print(f"Test voice error: {e}")

            @objc.signature(b'v@:@')
            def saveSettings_(self, sender):
                try:
                    raw_bat = str(self.pop_battery.titleOfSelectedItem()).replace("%", "").strip()
                    bat = int(raw_bat)
                    voice = str(self.pop_voice.titleOfSelectedItem())
                    loudness = str(self.pop_loudness.titleOfSelectedItem())
                    alert_type = str(self.pop_alert_type.titleOfSelectedItem())
                    reminder = str(self.pop_reminder.titleOfSelectedItem())
                    startup = (self.chk_startup.state() == AppKit.NSControlStateValueOn)

                    new_config = {
                        "battery_level": bat,
                        "voice": voice,
                        "loudness": loudness,
                        "alert_type": alert_type,
                        "reminder": reminder,
                        "startup": startup,
                    }
                    self.settings_manager.save(new_config)
                    StartupManager.sync(startup)

                    if self.on_save_callback:
                        self.on_save_callback()

                    if self.panel:
                        self.panel.close()
                except Exception as e:
                    print(f"Save settings error: {e}")

            @objc.signature(b'v@:@')
            def cancelSettings_(self, sender):
                if self.panel:
                    self.panel.close()

            @objc.signature(b'v@:@')
            def openWebsite_(self, sender):
                webbrowser.open("https://codingsart.com")

    except Exception as e:
        print(f"AppKit initialization error: {e}")
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


_active_mac_panel_controller = None


def show_mac_native_settings(settings_manager: SettingsManager, on_save_callback: Optional[Callable[[], None]] = None) -> None:
    """Display native macOS AppKit Cocoa settings window."""
    global _active_mac_panel_controller

    if not HAS_APPKIT:
        return

    # If window is already open, bring it to front
    if _active_mac_panel_controller and _active_mac_panel_controller.panel:
        try:
            _active_mac_panel_controller.panel.makeKeyAndOrderFront_(None)
            AppKit.NSApp.activateIgnoringOtherApps_(True)
            return
        except Exception:
            _active_mac_panel_controller = None

    audio_player = AudioPlayer()
    current = settings_manager.get_all()

    controller = MacSettingsPanel.alloc().initWithManager_player_callback_(
        settings_manager, audio_player, on_save_callback
    )
    _active_mac_panel_controller = controller

    style = AppKit.NSWindowStyleMaskTitled | AppKit.NSWindowStyleMaskClosable
    rect = AppKit.NSMakeRect(0, 0, 360, 340)
    panel = AppKit.NSPanel.alloc().initWithContentRect_styleMask_backing_defer_(
        rect, style, AppKit.NSBackingStoreBuffered, False
    )
    panel.setTitle_("Battery Alert Settings")
    panel.setFloatingPanel_(True)
    panel.setBecomesKeyOnlyIfNeeded_(False)
    panel.setHidesOnDeactivate_(False)

    controller.panel = panel

    content_view = panel.contentView()

    # Title label
    lbl_title = AppKit.NSTextField.labelWithString_("Battery Alert Settings")
    lbl_title.setFrame_(AppKit.NSMakeRect(20, 295, 320, 24))
    lbl_title.setFont_(AppKit.NSFont.boldSystemFontOfSize_(15))

    lbl_sub = AppKit.NSTextField.labelWithString_("Coding's Art - HardeepCoder")
    lbl_sub.setFrame_(AppKit.NSMakeRect(20, 275, 320, 18))
    lbl_sub.setFont_(AppKit.NSFont.systemFontOfSize_weight_(11, AppKit.NSFontWeightLight))

    # 1. Battery Alert Level
    lbl1 = AppKit.NSTextField.labelWithString_("Battery Alert Level:")
    lbl1.setFrame_(AppKit.NSMakeRect(20, 230, 140, 24))
    pop1 = AppKit.NSPopUpButton.alloc().initWithFrame_pullsDown_(AppKit.NSMakeRect(160, 228, 180, 26), False)
    pop1.addItemsWithTitles_([f"{v}%" for v in VALID_BATTERY_LEVELS])
    pop1.selectItemWithTitle_(f"{current.get('battery_level', 100)}%")
    controller.pop_battery = pop1

    # 2. Voice Selection (6 Voices)
    lbl2 = AppKit.NSTextField.labelWithString_("Alert Voice Pack:")
    lbl2.setFrame_(AppKit.NSMakeRect(20, 190, 140, 24))
    pop2 = AppKit.NSPopUpButton.alloc().initWithFrame_pullsDown_(AppKit.NSMakeRect(160, 188, 180, 26), False)
    pop2.addItemsWithTitles_(VALID_VOICES)
    pop2.selectItemWithTitle_(current.get("voice", "English Female"))
    controller.pop_voice = pop2

    # 3. Alert Loudness
    lbl3_v = AppKit.NSTextField.labelWithString_("Alert Loudness:")
    lbl3_v.setFrame_(AppKit.NSMakeRect(20, 150, 140, 24))
    pop3_v = AppKit.NSPopUpButton.alloc().initWithFrame_pullsDown_(AppKit.NSMakeRect(160, 148, 180, 26), False)
    pop3_v.addItemsWithTitles_(VALID_LOUDNESS_LEVELS)
    pop3_v.selectItemWithTitle_(current.get("loudness", "Normal"))
    controller.pop_loudness = pop3_v

    # 4. Alert Type
    lbl3 = AppKit.NSTextField.labelWithString_("Alert Type:")
    lbl3.setFrame_(AppKit.NSMakeRect(20, 110, 140, 24))
    pop3 = AppKit.NSPopUpButton.alloc().initWithFrame_pullsDown_(AppKit.NSMakeRect(160, 108, 180, 26), False)
    pop3.addItemsWithTitles_(VALID_ALERT_TYPES)
    pop3.selectItemWithTitle_(current.get("alert_type", "Voice + Notification"))
    controller.pop_alert_type = pop3

    # 5. Reminder Frequency
    lbl4 = AppKit.NSTextField.labelWithString_("Reminder Interval:")
    lbl4.setFrame_(AppKit.NSMakeRect(20, 70, 140, 24))
    pop4 = AppKit.NSPopUpButton.alloc().initWithFrame_pullsDown_(AppKit.NSMakeRect(160, 68, 180, 26), False)
    pop4.addItemsWithTitles_(VALID_REMINDERS)
    pop4.selectItemWithTitle_(current.get("reminder", "5 Minutes"))
    controller.pop_reminder = pop4

    # 6. Launch on Startup
    chk5 = AppKit.NSButton.alloc().initWithFrame_(AppKit.NSMakeRect(20, 35, 160, 24))
    chk5.setButtonType_(AppKit.NSButtonTypeSwitch)
    chk5.setTitle_("Launch on Startup")
    chk5.setState_(AppKit.NSControlStateValueOn if current.get("startup", False) else AppKit.NSControlStateValueOff)
    controller.chk_startup = chk5

    # 7. Test Voice Button
    btn_test = AppKit.NSButton.alloc().initWithFrame_(AppKit.NSMakeRect(180, 32, 160, 28))
    btn_test.setTitle_("▶ Test Voice")
    btn_test.setBezelStyle_(AppKit.NSBezelStyleRounded)
    btn_test.setTarget_(controller)
    btn_test.setAction_("testVoice:")

    # 8. Bottom Buttons (Save / Cancel)
    btn_cancel = AppKit.NSButton.alloc().initWithFrame_(AppKit.NSMakeRect(170, 5, 80, 26))
    btn_cancel.setTitle_("Cancel")
    btn_cancel.setBezelStyle_(AppKit.NSBezelStyleRounded)
    btn_cancel.setTarget_(controller)
    btn_cancel.setAction_("cancelSettings:")

    btn_save = AppKit.NSButton.alloc().initWithFrame_(AppKit.NSMakeRect(255, 5, 85, 26))
    btn_save.setTitle_("Save")
    btn_save.setBezelStyle_(AppKit.NSBezelStyleRounded)
    btn_save.setTarget_(controller)
    btn_save.setAction_("saveSettings:")

    btn_web = AppKit.NSButton.alloc().initWithFrame_(AppKit.NSMakeRect(20, 5, 140, 26))
    btn_web.setTitle_("🌐 codingsart.com")
    btn_web.setBezelStyle_(AppKit.NSBezelStyleRounded)
    btn_web.setTarget_(controller)
    btn_web.setAction_("openWebsite:")

    content_view.addSubview_(lbl_title)
    content_view.addSubview_(lbl_sub)
    content_view.addSubview_(lbl1)
    content_view.addSubview_(pop1)
    content_view.addSubview_(lbl2)
    content_view.addSubview_(pop2)
    content_view.addSubview_(lbl3_v)
    content_view.addSubview_(pop3_v)
    content_view.addSubview_(lbl3)
    content_view.addSubview_(pop3)
    content_view.addSubview_(lbl4)
    content_view.addSubview_(pop4)
    content_view.addSubview_(chk5)
    content_view.addSubview_(btn_test)
    content_view.addSubview_(btn_web)
    content_view.addSubview_(btn_cancel)
    content_view.addSubview_(btn_save)

    panel.setLevel_(AppKit.NSFloatingWindowLevel)
    panel.center()
    panel.makeKeyAndOrderFront_(None)
    AppKit.NSApp.activateIgnoringOtherApps_(True)


class SettingsWindow:
    """Settings launcher using native AppKit Cocoa on macOS or Tkinter on Windows."""

    def __init__(self, parent_root: Optional[Any], settings_manager: SettingsManager, on_save_callback: Optional[Callable[[], None]] = None) -> None:
        self._parent = parent_root
        self._settings_manager = settings_manager
        self._on_save_callback = on_save_callback
        self._window: Optional[Any] = None
        self._audio_player = AudioPlayer()

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
            row=2, column=0, sticky="W", pady=6
        )
        self._battery_var = tk.StringVar(value=f"{current_settings.get('battery_level', 100)}%")
        battery_combo = ttk.Combobox(
            container,
            textvariable=self._battery_var,
            values=[f"{val}%" for val in VALID_BATTERY_LEVELS],
            state="readonly",
            width=22,
        )
        battery_combo.grid(row=2, column=1, sticky="E", pady=6, padx=(10, 0))

        # 2. Voice Selection (6 Voices)
        ttk.Label(container, text="Alert Voice Pack:", font=("Helvetica", 10)).grid(
            row=3, column=0, sticky="W", pady=6
        )
        self._voice_var = tk.StringVar(value=current_settings.get("voice", "English Female"))
        voice_combo = ttk.Combobox(
            container,
            textvariable=self._voice_var,
            values=VALID_VOICES,
            state="readonly",
            width=22,
        )
        voice_combo.grid(row=3, column=1, sticky="E", pady=6, padx=(10, 0))

        # 3. Alert Loudness
        ttk.Label(container, text="Alert Loudness:", font=("Helvetica", 10)).grid(
            row=4, column=0, sticky="W", pady=6
        )
        self._loudness_var = tk.StringVar(value=current_settings.get("loudness", "Normal"))
        loudness_combo = ttk.Combobox(
            container,
            textvariable=self._loudness_var,
            values=VALID_LOUDNESS_LEVELS,
            state="readonly",
            width=22,
        )
        loudness_combo.grid(row=4, column=1, sticky="E", pady=6, padx=(10, 0))

        # 4. Alert Type
        ttk.Label(container, text="Alert Type:", font=("Helvetica", 10)).grid(
            row=5, column=0, sticky="W", pady=6
        )
        self._alert_type_var = tk.StringVar(value=current_settings.get("alert_type", "Voice + Notification"))
        alert_combo = ttk.Combobox(
            container,
            textvariable=self._alert_type_var,
            values=VALID_ALERT_TYPES,
            state="readonly",
            width=22,
        )
        alert_combo.grid(row=5, column=1, sticky="E", pady=6, padx=(10, 0))

        # 5. Reminder Frequency
        ttk.Label(container, text="Reminder Interval:", font=("Helvetica", 10)).grid(
            row=6, column=0, sticky="W", pady=6
        )
        self._reminder_var = tk.StringVar(value=current_settings.get("reminder", "5 Minutes"))
        reminder_combo = ttk.Combobox(
            container,
            textvariable=self._reminder_var,
            values=VALID_REMINDERS,
            state="readonly",
            width=22,
        )
        reminder_combo.grid(row=6, column=1, sticky="E", pady=6, padx=(10, 0))

        # 6. Launch on Startup
        ttk.Label(container, text="Launch on Startup:", font=("Helvetica", 10)).grid(
            row=7, column=0, sticky="W", pady=6
        )
        self._startup_var = tk.BooleanVar(value=current_settings.get("startup", False))
        startup_check = ttk.Checkbutton(
            container,
            text="Enabled" if self._startup_var.get() else "Disabled",
            variable=self._startup_var,
            command=self._toggle_startup_label,
        )
        self._startup_check = startup_check
        startup_check.grid(row=7, column=1, sticky="E", pady=6, padx=(10, 0))

        # Separator
        ttk.Separator(container, orient="horizontal").grid(
            row=8, column=0, columnspan=2, sticky="EW", pady=12
        )

        # Action Buttons Row
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=9, column=0, columnspan=2, sticky="EW")

        test_btn = ttk.Button(btn_frame, text="▶ Test Voice", command=self._test_voice)
        test_btn.pack(side="left")

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
        window.attributes('-topmost', True)
        window.lift()
        window.focus_force()

        if self._parent is None:
            window.mainloop()

    def _test_voice(self) -> None:
        v_name = self._voice_var.get()
        v_loud = self._loudness_var.get()
        self._audio_player.play(v_name, v_loud)

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
                "loudness": self._loudness_var.get(),
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
