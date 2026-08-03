# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Sound object - system sounds, beep tunes and audio file playback.
# Version : 1.7.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

import ctypes
from ctypes import wintypes
import winsound
import threading
import time
import os
import re
from smallbasic._utils import classproperty, _PropSetMeta


_winmm = ctypes.windll.winmm
_mciSendString = _winmm.mciSendStringW
_mciSendString.argtypes = (
    wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.UINT, wintypes.HWND)
_mciSendString.restype = wintypes.UINT


# Frequencies (Hz) of the notes in octave 4; other octaves are reached by
# doubling/halving (2 ** (octave - 4)).
_NOTE_BASE = {
    "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13,
    "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392.00,
    "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88,
}
_NOTE_ACCIDENTAL = {"#": "#", "+": "#", "b": "b", "-": "b"}

_MML_TOKEN = re.compile(
    r"[A-Ga-g][#+b-]?\d*\.?|O\d+|L\d+|T\d+|[PpRr]\d*\.?|\.")


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
    def _parse_music(cls, notes: str) -> list:
        """
        Parses a Music Macro Language (MML) subset into ``(freq, duration_ms)``
        pairs; a frequency of ``0`` marks a rest.

        Supported directives:
          - ``O<octave>``  — set the current octave (default 4)
          - ``L<length>``  — default note length (default 4 = quarter note)
          - ``T<tempo>``   — tempo in quarter notes per minute (default 120)
          - ``P<n>`` / ``R<n>`` — rest of the given length
          - note letters ``A-G`` / ``a-g`` (lower-case plays one octave up),
            optional accidentals (``#`` ``+`` ``b`` ``-``), optional length
            digits (``4`` = quarter, ``8`` = eighth, ...) and a trailing ``.``
            for a dotted note.

        Examples:
            _parse_music("C4")                 -> [(262, 500.0)]
            _parse_music("O5 C8 C8 G8 G8")     -> Twinkle Twinkle in octave 5
            _parse_music("T120 C4 C4 G4 G4")   -> quarter notes at 120 BPM
        """
        octave, length, tempo = 4, 4, 120
        out: list = []
        for token in _MML_TOKEN.findall(str(notes)):
            if token in ("", "."):
                if token == "." and out:
                    freq, dur = out[-1]
                    out[-1] = (freq, dur * 1.5)
                continue
            if token[0] in "Oo":
                octave = int(token[1:])
                continue
            if token[0] in "Ll":
                length = int(token[1:])
                continue
            if token[0] in "Tt":
                tempo = int(token[1:])
                continue
            if token[0] in "PpRr":
                rest = int(token[1:]) if token[1:].isdigit() else length
                dur = 240000.0 / (tempo * rest)
                if token.endswith("."):
                    dur *= 1.5
                out.append((0, dur))
                continue
            # Note token: letter [accidental] [length] [dot]
            m = re.match(r"([A-Ga-g])([#+b-]?)(\d*)(\.?)", token)
            if not m:
                continue
            letter, acc, length_str, dot = m.groups()
            key = letter.upper() + _NOTE_ACCIDENTAL.get(acc, "")
            base = _NOTE_BASE.get(key, _NOTE_BASE.get(letter.upper(), 440.0))
            note_octave = octave + (1 if letter.islower() else 0)
            freq = int(round(base * (2 ** (note_octave - 4))))
            note_len = int(length_str) if length_str else length
            if note_len <= 0:
                continue
            dur = 240000.0 / (tempo * note_len)
            if dot:
                dur *= 1.5
            out.append((freq, dur))
        return out

    @classmethod
    def PlayMusic(cls, notes: str) -> None:
        """
        Plays musical notes using the system beep.
        Note format is a subset of Music Macro Language — see ``_parse_music``.

        Args:
            notes: A string of musical notes, e.g. "O5 C8 C8 G8 G8 A8 A8 G4".
        """
        def _play():
            for freq, duration in cls._parse_music(notes):
                if freq > 0:
                    winsound.Beep(freq, max(10, int(round(duration))))
                else:
                    time.sleep(max(0.005, duration / 1000.0))
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

        If the file duration could not be determined (0.0), playback is
        still awaited using a generous safety cap instead of returning
        immediately.
        """
        cls.Play(path)
        max_wait = cls._duration if cls._duration > 0 else 120.0
        while cls._playing and time.time() - cls._play_start < max_wait:
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
