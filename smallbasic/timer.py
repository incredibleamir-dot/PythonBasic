# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Timer object - repeating Tick callbacks driven by a background thread.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

import logging
import threading
import time
from typing import Optional, Callable
from smallbasic._utils import classproperty, _PropSetMeta

logger = logging.getLogger(__name__)


class Timer(metaclass=_PropSetMeta):
    """
    Provides an easy way to do something repeatedly at a constant interval.
    
    Usage:
        Timer.Interval = 1000  # 1 second
        
        def on_tick():
            TextWindow.WriteLine("Tick!")
        
        Timer.Tick = on_tick  # Auto-starts the timer
    """

    Interval: int = 1000

    _timer: Optional[threading.Thread] = None
    _running: bool = False
    _paused: bool = False
    _tick: Optional[Callable] = None

    @classmethod
    def _run(cls):
        """Internal timer loop."""
        while cls._running:
            if not cls._paused and cls._tick:
                try:
                    cls._tick()
                except Exception as e:
                    logger.error("Timer tick callback raised an exception: %s", e)
            time.sleep(max(0.01, cls.Interval / 1000.0))

    @classmethod
    def _ensure_running(cls):
        """Start the background thread if not already running."""
        if cls._timer is None or not cls._timer.is_alive():
            cls._running = True
            cls._paused = False
            cls._timer = threading.Thread(target=cls._run, daemon=True)
            cls._timer.start()

    @classmethod
    def Pause(cls) -> None:
        """Pauses the timer. Tick events will not be raised."""
        cls._paused = True

    @classmethod
    def Resume(cls) -> None:
        """Resumes the timer from a paused state."""
        cls._paused = False
        cls._ensure_running()

    @classproperty
    def Tick(cls) -> Optional[Callable]:
        """Gets or sets the Tick event handler. Auto-starts the timer."""
        return cls._tick

    @Tick.setter
    def Tick(cls, value: Optional[Callable]) -> None:
        cls._tick = value
        if value is not None:
            cls._ensure_running()
