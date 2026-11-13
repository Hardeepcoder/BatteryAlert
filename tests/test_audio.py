import unittest
import os
from audio import AudioPlayer

class TestAudioPlayer(unittest.TestCase):
    def setUp(self):
        self.player = AudioPlayer()

    def test_resolve_voice_paths(self):
        voices = [
            "English Female",
            "English Male",
            "Hindi Female",
            "Hindi Male",
            "Punjabi Female",
            "Punjabi Male",
        ]
        for v in voices:
            path = self.player.get_voice_path(v)
            self.assertIsNotNone(path, f"Failed to resolve path for {v}")
            self.assertTrue(os.path.exists(path), f"Voice asset does not exist: {path}")

if __name__ == "__main__":
    unittest.main()
