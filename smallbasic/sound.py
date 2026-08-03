# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Sound object - system sounds, beep tunes and WAV playback control.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

import winsound
import threading
import time
import os
import wave
import tempfile
from smallbasic._utils import classproperty, _PropSetMeta


class Sound(metaclass=_PropSetMeta):
    """
    Provides playback of sounds using the Windows sound system.
    
    Usage:
        Sound.PlayClick()
        Sound.PlayBellRing()
        Sound.PlayMusic("O5 C8 C8 G8 G8 A8 A8 G4")
        Sound.Play("C:/music/track.mp3")
        
    WAV playback:
        Sound.WavFile = "C:/audio/sample.wav"
        print(Sound.WavDuration)
        Sound.WavPlay()
        Sound.WavPause()
        Sound.WavStop()
    """

    _current_file: str = ""
    _pause_event: threading.Event = threading.Event()
    _pause_event.set()

    _wav_file: str = ""
    _wav_duration: float = 0.0
    _wav_framerate: int = 44100
    _wav_nframes: int = 0
    _wav_position: float = 0.0
    _wav_start_time: float = 0.0
    _wav_playing: bool = False
    _wav_tmp: str = os.path.join(tempfile.gettempdir(), "_sb_wav_temp.wav")

    @classmethod
    def PlayClick(cls) -> None:
        """Plays the Click sound."""
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

    @classmethod
    def PlayClickAndWait(cls) -> None:
        """Plays the Click sound and waits for it to finish."""
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | 0)

    @classmethod
    def PlayChime(cls) -> None:
        """Plays the Chime sound."""
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)

    @classmethod
    def PlayChimeAndWait(cls) -> None:
        """Plays the Chime sound and waits for it to finish."""
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | 0)

    @classmethod
    def PlayChimes(cls) -> None:
        """Plays the Chimes sound."""
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS | winsound.SND_ASYNC)

    @classmethod
    def PlayChimesAndWait(cls) -> None:
        """Plays the Chimes sound and waits for it to finish."""
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS | 0)

    @classmethod
    def PlayBellRing(cls) -> None:
        """Plays the Bell Ring sound."""
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)

    @classmethod
    def PlayBellRingAndWait(cls) -> None:
        """Plays the Bell Ring sound and waits for it to finish."""
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | 0)

    @classmethod
    def PlayMusic(cls, notes: str) -> None:
        """
        Plays musical notes using the system beep.
        Note format is a simplified subset of Music Macro Language.
        
        Args:
            notes: A string of musical notes.
        """
        def _play():
            parts = notes.split()
            i = 0
            while i < len(parts):
                note = parts[i]
                duration = 200
                freq = 440
                if i + 1 < len(parts) and parts[i + 1].isdigit():
                    octave = int(parts[i + 1])
                    duration = max(50, 600 // octave)
                    i += 1
                note_map = {
                    'C': 262, 'D': 294, 'E': 330, 'F': 349,
                    'G': 392, 'A': 440, 'B': 494,
                    'c': 523, 'd': 587, 'e': 659, 'f': 698,
                    'g': 784, 'a': 880, 'b': 988
                }
                base = note[0]
                if base in note_map:
                    freq = note_map[base]
                winsound.Beep(freq, duration)
                i += 1
        threading.Thread(target=_play, daemon=True).start()

    @classmethod
    def Play(cls, file_path: str) -> None:
        """
        Plays an audio file (async).
        
        Args:
            file_path: Path to audio file (wav, mp3, wma).
        """
        cls._current_file = file_path
        cls._pause_event.set()
        if file_path.lower().endswith('.wav'):
            winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            if os.path.exists(file_path):
                os.startfile(file_path)

    @classmethod
    def PlayAndWait(cls, file_path: str) -> None:
        """
        Plays an audio file and waits for it to finish.
        
        Args:
            file_path: Path to audio file.
        """
        cls._current_file = file_path
        cls._pause_event.set()
        if file_path.lower().endswith('.wav'):
            winsound.PlaySound(file_path, winsound.SND_FILENAME | 0)
        else:
            cls.Play(file_path)
            if os.path.exists(file_path):
                try:
                    size = os.path.getsize(file_path)
                    estimated_duration = max(1, size / 16000)
                    time.sleep(min(estimated_duration, 30))
                except Exception:
                    time.sleep(5)

    @classmethod
    def Pause(cls) -> None:
        """
        Pauses playback of the current audio.
        Call Play() or PlayAndWait() to resume.
        """
        cls._pause_event.clear()
        winsound.PlaySound(None, winsound.SND_PURGE)

    @classmethod
    def Resume(cls) -> None:
        """
        Resumes playback from a paused state.
        """
        if not cls._pause_event.is_set():
            cls._pause_event.set()
            if cls._current_file:
                cls.Play(cls._current_file)

    @classmethod
    def Stop(cls) -> None:
        """
        Stops playback of the current audio.
        """
        cls._pause_event.set()
        cls._current_file = ""
        winsound.PlaySound(None, winsound.SND_PURGE)

    # ------------------------------------------------------------------ #
    #  WAV playback (position-tracked pause/resume via temp sub-wav)     #
    # ------------------------------------------------------------------ #

    @classproperty
    def WavFile(cls) -> str:
        """Gets or sets the WAV file path.  Setting loads header metadata."""
        return cls._wav_file

    @WavFile.setter
    def WavFile(cls, path: str) -> None:
        cls._wav_file = path
        cls._wav_position = 0.0
        cls._wav_playing = False
        if path and os.path.exists(path):
            try:
                with wave.open(path) as w:
                    cls._wav_framerate = w.getframerate()
                    cls._wav_nframes = w.getnframes()
                    cls._wav_duration = cls._wav_nframes / cls._wav_framerate
            except Exception:
                cls._wav_duration = 0.0
                cls._wav_framerate = 44100
                cls._wav_nframes = 0
        else:
            cls._wav_duration = 0.0

    @classproperty
    def WavDuration(cls) -> float:
        """Total duration of the loaded WAV file in seconds (read-only)."""
        return cls._wav_duration

    @classproperty
    def PlayPosition(cls) -> float:
        """Current playback position in seconds (read-only)."""
        if not cls._wav_playing:
            return min(cls._wav_position, cls._wav_duration)
        elapsed = time.time() - cls._wav_start_time
        return min(cls._wav_position + elapsed, cls._wav_duration)

    @classproperty
    def WavPlaying(cls) -> bool:
        """True while WAV audio is currently playing (read-only)."""
        return cls._wav_playing

    @classmethod
    def _write_subwav(cls, start_sec: float) -> bool:
        remaining = cls._wav_nframes - int(start_sec * cls._wav_framerate)
        if remaining <= 0:
            return False
        with wave.open(cls._wav_file) as src:
            src.setpos(int(start_sec * cls._wav_framerate))
            frames = src.readframes(remaining)
        with wave.open(cls._wav_tmp, "wb") as dst:
            dst.setnchannels(1)
            dst.setsampwidth(2)
            dst.setframerate(cls._wav_framerate)
            dst.writeframes(frames)
        return True

    @classmethod
    def WavPlay(cls) -> None:
        """
        Plays the WAV file from the beginning, or resumes from pause.
        Requires WavFile to be set first.
        """
        if not cls._wav_file or not os.path.exists(cls._wav_file):
            return
        ok = cls._write_subwav(cls._wav_position)
        if not ok:
            return
        cls._wav_start_time = time.time()
        cls._wav_playing = True
        winsound.PlaySound(cls._wav_tmp, winsound.SND_FILENAME | winsound.SND_ASYNC)

    @classmethod
    def WavPause(cls) -> None:
        """
        Pauses WAV playback and saves the current position.
        Call WavPlay() or WavResume() to continue.
        """
        if not cls._wav_playing:
            return
        elapsed = time.time() - cls._wav_start_time
        cls._wav_position += elapsed
        if cls._wav_position >= cls._wav_duration:
            cls._wav_position = cls._wav_duration
        cls._wav_playing = False
        winsound.PlaySound(None, winsound.SND_PURGE)

    @classmethod
    def WavStop(cls) -> None:
        """
        Stops WAV playback and resets the position to the beginning.
        """
        cls._wav_position = 0.0
        cls._wav_playing = False
        winsound.PlaySound(None, winsound.SND_PURGE)

    @classmethod
    def WavPlayAndWait(cls) -> None:
        """
        Plays the WAV file and blocks until playback finishes.
        Requires WavFile to be set first.
        """
        if not cls._wav_file or not os.path.exists(cls._wav_file):
            return
        cls._wav_position = 0.0
        cls._wav_playing = True
        winsound.PlaySound(cls._wav_file, winsound.SND_FILENAME | 0)
        cls._wav_position = cls._wav_duration
        cls._wav_playing = False
