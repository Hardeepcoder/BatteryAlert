import unittest
from unittest.mock import patch, MagicMock
from battery import BatteryMonitor, BatteryStatus

class TestBatteryMonitor(unittest.TestCase):
    @patch("psutil.sensors_battery")
    def test_get_status_charging(self, mock_sensors):
        mock_battery = MagicMock()
        mock_battery.percent = 84.7
        mock_battery.power_plugged = True
        mock_battery.secsleft = -1
        mock_sensors.return_value = mock_battery

        status = BatteryMonitor.get_status()
        self.assertIsNotNone(status)
        self.assertEqual(status.percent, 84.7)
        self.assertTrue(status.is_charging)
        self.assertTrue(status.power_plugged)

    @patch("psutil.sensors_battery")
    def test_get_status_none(self, mock_sensors):
        mock_sensors.return_value = None
        status = BatteryMonitor.get_status()
        self.assertIsNone(status)

if __name__ == "__main__":
    unittest.main()
