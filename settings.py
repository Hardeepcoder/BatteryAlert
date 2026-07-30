"""Settings manager for loading and saving user preferences."""

import json
import os
import threading
from typing import Any, Dict, Optional, Callable


DEFAULT_SETTINGS: Dict[str, Any] = {
    "battery_level": 100,
    "voice": "Female",
    "alert_type": "Voice + Notification",
    "reminder": "Alert Once",
    "startup": False,
}

VALID_BATTERY_LEVELS = [80, 90, 95, 100]
VALID_VOICES = ["Female", "Male"]
VALID_ALERT_TYPES = ["Voice Only", "Notification Only", "Voice + Notification"]
VALID_REMINDERS = ["Alert Once", "5 Minutes", "10 Minutes", "15 Minutes"]


class SettingsManager:
    """Handles persistent JSON settings with thread-safety."""

    def __init__(self, config_dir: Optional[str] = None) -> None:
        if config_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = os.path.join(base_dir, "config")

        self._config_dir = config_dir
        self._config_file = os.path.join(self._config_dir, "settings.json")
        self._lock = threading.Lock()
        self._on_change_callbacks = []
        self._settings: Dict[str, Any] = DEFAULT_SETTINGS.copy()
        self.load()

    def register_on_change(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback function to be called when settings change."""
        self._on_change_callbacks.append(callback)

    def load(self) -> Dict[str, Any]:
        """Load settings from JSON file, using defaults for missing or invalid values."""
        with self._lock:
            if not os.path.exists(self._config_file):
                self._settings = DEFAULT_SETTINGS.copy()
                self._save_unlocked()
                return self._settings.copy()

            try:
                with open(self._config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Sanitize and validate loaded fields
                self._settings = {
                    "battery_level": data.get("battery_level", DEFAULT_SETTINGS["battery_level"]),
                    "voice": data.get("voice", DEFAULT_SETTINGS["voice"]),
                    "alert_type": data.get("alert_type", DEFAULT_SETTINGS["alert_type"]),
                    "reminder": data.get("reminder", DEFAULT_SETTINGS["reminder"]),
                    "startup": bool(data.get("startup", DEFAULT_SETTINGS["startup"])),
                }

                # Validate ranges
                if self._settings["battery_level"] not in VALID_BATTERY_LEVELS:
                    self._settings["battery_level"] = DEFAULT_SETTINGS["battery_level"]
                if self._settings["voice"] not in VALID_VOICES:
                    self._settings["voice"] = DEFAULT_SETTINGS["voice"]
                if self._settings["alert_type"] not in VALID_ALERT_TYPES:
                    self._settings["alert_type"] = DEFAULT_SETTINGS["alert_type"]
                if self._settings["reminder"] not in VALID_REMINDERS:
                    self._settings["reminder"] = DEFAULT_SETTINGS["reminder"]

            except Exception:
                self._settings = DEFAULT_SETTINGS.copy()

            return self._settings.copy()

    def _save_unlocked(self) -> None:
        """Helper to save settings assuming lock is held."""
        try:
            os.makedirs(self._config_dir, exist_ok=True)
            with open(self._config_file, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def save(self, new_settings: Dict[str, Any]) -> None:
        """Save settings dictionary to file and notify listeners."""
        with self._lock:
            self._settings.update(new_settings)
            self._save_unlocked()
            updated = self._settings.copy()

        for callback in self._on_change_callbacks:
            try:
                callback(updated)
            except Exception as e:
                print(f"Error in settings callback: {e}")

    def get_all(self) -> Dict[str, Any]:
        """Get copy of all settings."""
        with self._lock:
            return self._settings.copy()

    def get(self, key: str, default: Any = None) -> Any:
        """Get single setting value."""
        with self._lock:
            return self._settings.get(key, default)
