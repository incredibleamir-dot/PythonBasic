import winsound
import threading
import time


class Sound:
    """
    Provides playback of sounds using the Windows sound system.
    
    Usage:
        Sound.PlayClick()
        Sound.PlayBellRing()
        Sound.PlayMusic("O5 C8 C8 G8 G8 A8 A8 G4")
        Sound.Play("C:/music/track.mp3")
    """

    @classmethod
    def PlayClick(cls) -> None:
        """Plays the Click sound."""
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

    @classmethod
    def PlayClickAndWait(cls) -> None:
        """Plays the Click sound and waits for it to finish."""
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_SYNC)

    @classmethod
    def PlayChime(cls) -> None:
        """Plays the Chime sound."""
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)

    @classmethod
    def PlayChimeAndWait(cls) -> None:
        """Plays the Chime sound and waits for it to finish."""
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_SYNC)

    @classmethod
    def PlayChimes(cls) -> None:
        """Plays the Chimes sound."""
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS | winsound.SND_ASYNC)

    @classmethod
    def PlayChimesAndWait(cls) -> None:
        """Plays the Chimes sound and waits for it to finish."""
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS | winsound.SND_SYNC)

    @classmethod
    def PlayBellRing(cls) -> None:
        """Plays the Bell Ring sound."""
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)

    @classmethod
    def PlayBellRingAndWait(cls) -> None:
        """Plays the Bell Ring sound and waits for it to finish."""
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_SYNC)

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
        if file_path.lower().endswith('.wav'):
            winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            import os
            if os.path.exists(file_path):
                os.startfile(file_path)

    @classmethod
    def PlayAndWait(cls, file_path: str) -> None:
        """
        Plays an audio file and waits for it to finish.
        
        Args:
            file_path: Path to audio file.
        """
        if file_path.lower().endswith('.wav'):
            winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_SYNC)
        else:
            cls.Play(file_path)
            time.sleep(2)

    @classmethod
    def Pause(cls, file_path: str) -> None:
        """
        Pauses playback of an audio file.
        
        Args:
            file_path: Path to audio file.
        """
        winsound.PlaySound(None, winsound.SND_PURGE)

    @classmethod
    def Stop(cls, file_path: str) -> None:
        """
        Stops playback of an audio file.
        
        Args:
            file_path: Path to audio file.
        """
        winsound.PlaySound(None, winsound.SND_PURGE)
