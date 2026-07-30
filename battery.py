"""Battery monitoring module using psutil."""

from dataclasses import dataclass
from typing import Optional
import psutil


@dataclass
class BatteryStatus:
    """Dataclass holding current battery telemetry."""
    percent: float
    power_plugged: Optional[bool]
    is_charging: bool
    time_left_seconds: Optional[int]


class BatteryMonitor:
    """Reads system battery status using psutil."""

    @staticmethod
    def get_status() -> Optional[BatteryStatus]:
        """Fetch current battery status from OS sensors."""
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return None

            percent = round(battery.percent, 1)
            power_plugged = battery.power_plugged

            # Charging status heuristics:
            # If plugged in and not at 100%, or power_plugged is True
            is_charging = bool(power_plugged)

            sec_left = battery.secsleft if battery.secsleft not in (psutil.POWER_TIME_UNKNOWN, psutil.POWER_TIME_UNLIMITED) else None

            return BatteryStatus(
                percent=percent,
                power_plugged=power_plugged,
                is_charging=is_charging,
                time_left_seconds=sec_left
            )
        except Exception as e:
            print(f"Error reading battery status: {e}")
            return None
