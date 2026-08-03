# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Sound object - system sounds, beep tunes and audio file playback.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

import ctypes
from ctypes import wintypes
import winsound
import threading
import time
import os
from smallbasic._utils import classproperty, _PropSetMeta


_winmm = ctypes.windll.winmm
_mciSendString = _winmm.mciSendStringW
_mciSendString.argtypes = (
    wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.UINT, wintypes.HWND)
_mciSendString.restype = wintypes.UINT


class Sound(metaclass=_PropSetMeta):
    """
    Provides playback of sounds using the Windows sound system.

    System sounds and beep tunes use winsound. Audio files - both WAV and
    MP3 - are played through the Windows Media Control Interface (MCI),
    using only the standard library (ctypes + winmm).

    Playback position is tracked with a monotonic wall-clock, so it is safe
    to read `PlayPosition` / `IsPlaying` from Timer callbacks (which run on a
    background thread); MCI itself reports position 0 from non-main threads.

    Usage:
        Sound.PlayClick()
        Sound.PlayBellRing()
        Sound.PlayMusic("O5 C8 C8 G8 G8 A8 A8 G4")

        Sound.Play("C:/music/track.mp3")     # one-liner playback
        Sound.PlayAndWait("C:/music/track.wav")

        Sound.Open("C:/audio/sample.wav")    # optional: load and inspect
        print(Sound.Duration)                # total seconds
        Sound.Play()
        Sound.Pause()
        Sound.Resume()
        Sound.Seek(10.5)
        print(Sound.PlayPosition, Sound.IsPlaying)
        Sound.Stop()
    """

    _alias: str = "sbmedia"
    _current_file: str = ""
    _duration: float = 0.0
    _pos_offset: float = 0.0
    _play_start: float = 0.0
    _playing: bool = False

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

    # ------------------------------------------------------------------ #
    #  Audio file playback (WAV & MP3 via Windows MCI, stdlib only)      #
    # ------------------------------------------------------------------ #

    @classmethod
    def _mci(cls, command: str):
        """Sends an MCI command; returns (errorcode, return-value)."""
        buf = ctypes.create_unicode_buffer(512)
        code = _mciSendString(command, buf, len(buf), None)
        return int(code), buf.value

    @classmethod
    def Open(cls, path: str) -> bool:
        """
        Opens a WAV or MP3 file and makes it ready for playback.
        Returns True on success. Any previously open file is closed first.
        """
        cls._close()
        if not path or not os.path.exists(path):
            return False
        ftype = "waveaudio" if str(path).lower().endswith(".wav") else "mpegvideo"
        code, _ = cls._mci(
            'open "{}" type {} alias {}'.format(path, ftype, cls._alias))
        if code != 0:
            return False
        cls._mci("set {} time format milliseconds".format(cls._alias))
        _, value = cls._mci("status {} length".format(cls._alias))
        try:
            cls._duration = float(value) / 1000.0
        except (TypeError, ValueError):
            cls._duration = 0.0
        cls._current_file = path
        cls._playing = False
        cls._pos_offset = 0.0
        return True

    @classmethod
    def Play(cls, path: str = None) -> None:
        """
        Plays an audio file (WAV or MP3) without blocking.

        Args:
            path: File path. If omitted, the currently open file is played
                  (or playback resumes after a pause).
        """
        if path is not None:
            if not cls.Open(path):
                return
        if not cls._current_file:
            return
        cls._mci("play {}".format(cls._alias))
        cls._playing = True
        cls._play_start = time.time()

    @classmethod
    def PlayAndWait(cls, path: str = None) -> None:
        """
        Plays an audio file and blocks until playback finishes.
        """
        cls.Play(path)
        while cls._playing and time.time() - cls._play_start < cls._duration:
            time.sleep(0.05)
        cls.Stop()

    @classmethod
    def Pause(cls) -> None:
        """
        Pauses playback. Call Resume() (or Play()) to continue.
        """
        if not cls._playing:
            return
        cls._mci("pause {}".format(cls._alias))
        cls._pos_offset = cls.PlayPosition
        cls._playing = False

    @classmethod
    def Resume(cls) -> None:
        """
        Resumes a paused audio file from where it stopped.
        """
        if cls._current_file and not cls._playing:
            cls._mci("play {}".format(cls._alias))
            cls._playing = True
            cls._play_start = time.time()

    @classmethod
    def Stop(cls) -> None:
        """
        Stops playback and rewinds to the start of the file.
        The file stays open so it can be played again.
        """
        if cls._current_file:
            cls._mci("stop {}".format(cls._alias))
            cls._mci("seek {} to start".format(cls._alias))
        cls._playing = False
        cls._pos_offset = 0.0

    @classmethod
    def Seek(cls, seconds: float) -> None:
        """
        Jumps to a position (in seconds) within the open file.
        If audio is playing, playback continues from the new position.
        """
        if not cls._current_file:
            return
        ms = max(0, int(seconds * 1000))
        cls._mci("seek {} to {}".format(cls._alias, ms))
        cls._pos_offset = max(0.0, min(float(seconds), cls._duration))
        cls._play_start = time.time()
        if cls._playing:
            cls._mci("play {}".format(cls._alias))

    @classmethod
    def _close(cls) -> None:
        if cls._current_file:
            cls._mci("close {}".format(cls._alias))
        cls._current_file = ""
        cls._duration = 0.0
        cls._pos_offset = 0.0
        cls._playing = False

    @classproperty
    def CurrentFile(cls) -> str:
        """Path of the currently open audio file (read-only)."""
        return cls._current_file

    @classproperty
    def Duration(cls) -> float:
        """Total duration of the open file in seconds (read-only)."""
        return cls._duration

    @classproperty
    def PlayPosition(cls) -> float:
        """Current playback position in seconds (read-only)."""
        if not cls._current_file:
            return 0.0
        if cls._playing:
            return min(cls._pos_offset + (time.time() - cls._play_start),
                       cls._duration)
        return min(cls._pos_offset, cls._duration)

    @classproperty
    def IsPlaying(cls) -> bool:
        """True while audio is currently playing (read-only)."""
        return cls._playing
