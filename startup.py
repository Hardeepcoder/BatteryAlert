"""Startup management for enabling/disabling auto-launch on system boot."""

import os
import sys
import subprocess
from typing import Optional


class StartupManager:
    """Manages system startup entries cross-platform (Windows & macOS)."""

    APP_NAME = "BatteryAlert"

    @classmethod
    def get_executable_path(cls) -> str:
        """Get absolute path to executable or Python main script."""
        if getattr(sys, 'frozen', False):
            return sys.executable
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "app.py"))

    @classmethod
    def enable(cls) -> bool:
        """Enable launch on startup."""
        if sys.platform == "win32":
            return cls._enable_windows()
        elif sys.platform == "darwin":
            return cls._enable_macos()
        return False

    @classmethod
    def disable(cls) -> bool:
        """Disable launch on startup."""
        if sys.platform == "win32":
            return cls._disable_windows()
        elif sys.platform == "darwin":
            return cls._disable_macos()
        return False

    @classmethod
    def is_enabled(cls) -> bool:
        """Check if launch on startup is currently enabled."""
        if sys.platform == "win32":
            return cls._is_enabled_windows()
        elif sys.platform == "darwin":
            return cls._is_enabled_macos()
        return False

    @classmethod
    def sync(cls, enabled: bool) -> bool:
        """Synchronize startup configuration state."""
        if enabled:
            return cls.enable()
        else:
            return cls.disable()

    # --- Windows Implementation ---

    @classmethod
    def _enable_windows(cls) -> bool:
        try:
            import winreg
            exec_path = f'"{cls.get_executable_path()}"'
            if not getattr(sys, 'frozen', False):
                exec_path = f'"{sys.executable}" "{cls.get_executable_path()}"'

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, cls.APP_NAME, 0, winreg.REG_SZ, exec_path)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Failed to enable Windows startup: {e}")
            return False

    @classmethod
    def _disable_windows(cls) -> bool:
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            try:
                winreg.DeleteValue(key, cls.APP_NAME)
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Failed to disable Windows startup: {e}")
            return False

    @classmethod
    def _is_enabled_windows(cls) -> bool:
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, cls.APP_NAME)
                enabled = True
            except FileNotFoundError:
                enabled = False
            winreg.CloseKey(key)
            return enabled
        except Exception:
            return False

    # --- macOS Implementation ---

    @classmethod
    def _get_plist_path(cls) -> str:
        home = os.path.expanduser("~")
        return os.path.join(home, "Library", "LaunchAgents", f"com.{cls.APP_NAME.lower()}.plist")

    @classmethod
    def _enable_macos(cls) -> bool:
        try:
            plist_path = cls._get_plist_path()
            os.makedirs(os.path.dirname(plist_path), exist_ok=True)
            
            exec_path = cls.get_executable_path()
            if getattr(sys, 'frozen', False):
                program_args = f"<string>{exec_path}</string>"
            else:
                program_args = f"<string>{sys.executable}</string>\n        <string>{exec_path}</string>"

            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.{cls.APP_NAME.lower()}</string>
    <key>ProgramArguments</key>
    <array>
        {program_args}
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
            with open(plist_path, "w", encoding="utf-8") as f:
                f.write(plist_content)
            return True
        except Exception as e:
            print(f"Failed to enable macOS LaunchAgent: {e}")
            return False

    @classmethod
    def _disable_macos(cls) -> bool:
        try:
            plist_path = cls._get_plist_path()
            if os.path.exists(plist_path):
                os.remove(plist_path)
            return True
        except Exception as e:
            print(f"Failed to disable macOS LaunchAgent: {e}")
            return False

    @classmethod
    def _is_enabled_macos(cls) -> bool:
        plist_path = cls._get_plist_path()
        return os.path.exists(plist_path)
