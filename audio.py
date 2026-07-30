"""Audio module for playing voice alert files cross-platform."""

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
        """Resolve voice name (e.g. 'Female', 'Male') to asset file path."""
        filename = f"{voice_name.lower().strip()}.wav"
        filepath = os.path.join(self._assets_dir, filename)
        if os.path.exists(filepath):
            return filepath
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

    def play(self, voice_name: str) -> bool:
        """Play the specified voice file asynchronously, stopping any ongoing playback."""
        filepath = self.get_voice_path(voice_name)
        if not filepath:
            print(f"Audio file for voice '{voice_name}' not found at {filepath}")
            return False

        # Stop previous voice playback so two voices never play at the same time
        self.stop()

        thread = threading.Thread(target=self._play_file_sync, args=(filepath,), daemon=True)
        thread.start()
        return True

    def _play_file_sync(self, filepath: str) -> None:
        """Synchronous file playback runner according to operating system."""
        try:
            if sys.platform == "darwin":
                # macOS: built-in command line audio player afplay
                with self._lock:
                    proc = subprocess.Popen(["afplay", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    self._current_process = proc
                proc.wait()
                with self._lock:
                    if self._current_process == proc:
                        self._current_process = None
            elif sys.platform == "win32":
                import winsound
                winsound.PlaySound(filepath, winsound.SND_FILENAME)
            else:
                if subprocess.call(["which", "aplay"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                    with self._lock:
                        proc = subprocess.Popen(["aplay", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        self._current_process = proc
                    proc.wait()
                    with self._lock:
                        if self._current_process == proc:
                            self._current_process = None
                elif subprocess.call(["which", "paplay"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                    with self._lock:
                        proc = subprocess.Popen(["paplay", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        self._current_process = proc
                    proc.wait()
                    with self._lock:
                        if self._current_process == proc:
                            self._current_process = None
        except Exception as e:
            print(f"Failed to play audio file {filepath}: {e}")
