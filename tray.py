"""System tray (Windows) and Menu bar (macOS) integration using pystray."""

import os
import sys
import threading
from typing import Callable, Optional
from PIL import Image
import pystray
from pystray import MenuItem as item, Menu


class SystemTray:
    """Manages the system tray / menu bar icon and context menu."""

    def __init__(
        self,
        on_open_settings: Callable[[], None],
        on_check_battery: Callable[[], None],
        on_show_about: Callable[[], None],
        on_exit: Callable[[], None],
    ) -> None:
        self._on_open_settings = on_open_settings
        self._on_check_battery = on_check_battery
        self._on_show_about = on_show_about
        self._on_exit = on_exit
        self._icon: Optional[pystray.Icon] = None
        self._thread: Optional[threading.Thread] = None

    def _create_icon_image(self) -> Image.Image:
        """Load or create default tray icon image."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        png_path = os.path.join(base_dir, "icon", "app.png")
        if os.path.exists(png_path):
            try:
                return Image.open(png_path)
            except Exception as e:
                print(f"Failed to load icon PNG: {e}")

        # Fallback 64x64 solid icon
        image = Image.new("RGBA", (64, 64), (16, 185, 129, 255))
        return image

    def run(self) -> None:
        """Start the system tray icon loop."""
        menu = Menu(
            item("Settings", lambda: self._on_open_settings()),
            item("Check Battery Now", lambda: self._on_check_battery()),
            Menu.SEPARATOR,
            item("About", lambda: self._on_show_about()),
            Menu.SEPARATOR,
            item("Exit", lambda: self._stop_and_exit()),
        )

        image = self._create_icon_image()
        self._icon = pystray.Icon("BatteryAlert", image, "Battery Alert", menu)
        self._icon.run()

    def run_detached(self) -> None:
        """Run system tray in a background thread."""
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def _stop_and_exit(self) -> None:
        """Cleanly stop tray icon and trigger exit handler."""
        if self._icon is not None:
            self._icon.stop()
        self._on_exit()

    def stop(self) -> None:
        """Stop tray icon programmatically."""
        if self._icon is not None:
            self._icon.stop()
