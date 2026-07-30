"""Native operating system notification handler for Windows and macOS."""

import sys
import os
import subprocess
import time
from typing import Optional

HAS_APPKIT = False
if sys.platform == "darwin":
    try:
        import AppKit
        HAS_APPKIT = True
    except ImportError:
        HAS_APPKIT = False


class Notifier:
    """Delivers native system notifications with deduplication and auto-dismissal."""

    DEFAULT_TITLE = "Battery Fully Charged"
    DEFAULT_MESSAGE = "Battery fully charged.\nYou can unplug the charger now."

    def __init__(self) -> None:
        self._last_notify_time: float = 0.0
        self._min_interval_seconds: float = 3.0  # Prevent duplicate notification spam

    def notify(self, title: str = DEFAULT_TITLE, message: str = DEFAULT_MESSAGE) -> bool:
        """Send native OS notification."""
        now = time.time()
        if now - self._last_notify_time < self._min_interval_seconds:
            return False

        self._last_notify_time = now

        try:
            if sys.platform == "darwin":
                return self._notify_macos(title, message)
            elif sys.platform == "win32":
                return self._notify_windows(title, message)
            else:
                return self._notify_linux(title, message)
        except Exception as e:
            print(f"Error triggering native notification: {e}")
            return False

    def _notify_macos(self, title: str, message: str) -> bool:
        """macOS notification attributed directly to BatteryAlert app using AppKit."""
        if HAS_APPKIT:
            try:
                notification = AppKit.NSUserNotification.alloc().init()
                notification.setTitle_(title)
                notification.setInformativeText_(message)
                notification.setSoundName_(None)

                center = AppKit.NSUserNotificationCenter.defaultUserNotificationCenter()
                center.deliverNotification_(notification)
                return True
            except Exception as e:
                print(f"AppKit notification error: {e}")

        # Fallback to osascript if AppKit is unavailable
        clean_title = title.replace('"', '\\"')
        clean_msg = message.replace('"', '\\"')
        script = f'display notification "{clean_msg}" with title "{clean_title}"'
        cmd = ["osascript", "-e", script]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0

    def _notify_windows(self, title: str, message: str) -> bool:
        """Windows Toast Notification using PowerShell script."""
        clean_title = title.replace('"', '`"').replace("'", "''")
        clean_msg = message.replace('"', '`"').replace("'", "''")

        ps_script = f"""
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
        
        $template = @"
        <toast duration="short">
            <visual>
                <binding template="ToastGeneric">
                    <text>{clean_title}</text>
                    <text>{clean_msg}</text>
                </binding>
            </visual>
        </toast>
"@
        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
        $toast.ExpirationTime = [DateTimeOffset]::Now.AddSeconds(7)
        $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("BatteryAlert")
        $notifier.Show($toast)
        """

        try:
            cmd = ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return res.returncode == 0
        except Exception:
            return False

    def _notify_linux(self, title: str, message: str) -> bool:
        """Linux fallback notification via notify-send."""
        try:
            subprocess.run(["notify-send", "-t", "7000", title, message], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False
