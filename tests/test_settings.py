import unittest
import os
import shutil
import tempfile
from settings import SettingsManager, DEFAULT_SETTINGS

class TestSettingsManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.mgr = SettingsManager(config_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_default_settings(self):
        self.assertEqual(self.mgr.get("battery_level"), DEFAULT_SETTINGS["battery_level"])
        self.assertEqual(self.mgr.get("voice"), DEFAULT_SETTINGS["voice"])

    def test_save_and_load(self):
        current = self.mgr.get_all()
        current["battery_level"] = 85
        current["voice"] = "Hindi Female"
        self.mgr.save(current)

        self.assertEqual(self.mgr.get("battery_level"), 85)
        self.assertEqual(self.mgr.get("voice"), "Hindi Female")

        # Reload from fresh manager instance
        new_mgr = SettingsManager(config_dir=self.test_dir)
        self.assertEqual(new_mgr.get("battery_level"), 85)
        self.assertEqual(new_mgr.get("voice"), "Hindi Female")

    def test_callback_trigger(self):
        triggered = []
        def on_change(new_s):
            triggered.append(new_s)

        self.mgr.register_on_change(on_change)
        current = self.mgr.get_all()
        current["battery_level"] = 90
        self.mgr.save(current)

        self.assertEqual(len(triggered), 1)
        self.assertEqual(triggered[0]["battery_level"], 90)

if __name__ == "__main__":
    unittest.main()
