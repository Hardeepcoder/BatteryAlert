"""Audio module for playing voice alert files cross-platform with loudness boost."""

import os
import sys
import subprocess
import threading
from typing import Optional


class AudioPlayer:
    """Handles audio playback of WAV voice files without heavy dependencies."""

    def __init__(self, assets_dir: Optional[str] = None) -> None:
        if assets_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            assets_dir = os.path.join(base_dir, "assets")
        self._assets_dir = assets_dir
        self._current_process: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()

    def get_voice_path(self, voice_name: str) -> Optional[str]:
        """Resolve voice name (e.g. 'English Female', 'Hindi Male', 'Female') to asset file path."""
        v = voice_name.strip().lower()

        if "hindi female" in v or ("hindi" in v and "female" in v):
            filename = "female_hi.wav"
        elif "hindi male" in v or ("hindi" in v and "male" in v):
            filename = "male_hi.wav"
        elif "punjabi female" in v or ("punjabi" in v and "female" in v):
            filename = "female_pa.wav"
        elif "punjabi male" in v or ("punjabi" in v and "male" in v):
            filename = "male_pa.wav"
        elif "english male" in v or ("male" in v and "female" not in v):
            filename = "male.wav"
        else:
            filename = "female.wav"

        filepath = os.path.join(self._assets_dir, filename)
        if os.path.exists(filepath):
            return filepath

        # Fallback check
        fallback = os.path.join(self._assets_dir, f"{v}.wav")
        if os.path.exists(fallback):
            return fallback

        return None

    def stop(self) -> None:
        """Stop any currently playing audio."""
        with self._lock:
            if self._current_process is not None:
                try:
                    self._current_process.terminate()
                except Exception:
                    pass
                self._current_process = None

            if sys.platform == "win32":
                try:
                    import winsound
                    winsound.PlaySound(None, winsound.SND_PURGE)
                except Exception:
                    pass

    def play(self, voice_name: str, loudness_level: str = "Normal") -> bool:
        """Play the specified voice file asynchronously with optional volume boost."""
        filepath = self.get_voice_path(voice_name)
        if not filepath:
            print(f"Audio file for voice '{voice_name}' not found at assets path.")
            return False

        # Stop previous voice playback so two voices never overlap
        self.stop()

        thread = threading.Thread(
            target=self._play_file_sync,
            args=(filepath, loudness_level),
            daemon=True
        )
        thread.start()
        return True

    def _play_file_sync(self, filepath: str, loudness_level: str = "Normal") -> None:
        """Synchronous file playback runner according to operating system."""
        volume_factor = 1.0
        lvl = loudness_level.lower()
        if "150" in lvl or "high" in lvl:
            volume_factor = 1.5
        elif "200" in lvl or "max" in lvl:
            volume_factor = 2.0

        try:
            if sys.platform == "darwin":
                # macOS: built-in afplay supports -v volume multiplier
                cmd = ["afplay", "-v", str(volume_factor), filepath]
                with self._lock:
                    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    self._current_process = proc
                proc.wait()
                with self._lock:
                    if self._current_process == proc:
                        self._current_process = None

            elif sys.platform == "win32":
                import winsound
                winsound.PlaySound(filepath, winsound.SND_FILENAME)

            else:
                if subprocess.call(["which", "paplay"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                    # Linux PulseAudio paplay supports --volume (65536 = 100%)
                    vol_int = int(65536 * volume_factor)
                    cmd = ["paplay", "--volume", str(vol_int), filepath]
                    with self._lock:
                        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        self._current_process = proc
                    proc.wait()
                    with self._lock:
                        if self._current_process == proc:
                            self._current_process = None
                else:
                    with self._lock:
                        proc = subprocess.Popen(["aplay", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        self._current_process = proc
                    proc.wait()
                    with self._lock:
                        if self._current_process == proc:
                            self._current_process = None
        except Exception as e:
            print(f"Failed to play audio file {filepath}: {e}")
