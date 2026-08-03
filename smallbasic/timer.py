# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Timer object - repeating Tick callbacks driven by the Tk event
#           loop when a window is open, or a background thread otherwise.
# Version : 1.7.0
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

    When a graphics window (Tk root) is open, Tick callbacks run on the
    window's event loop (the main thread), so they may safely touch
    GraphicsWindow / Shapes / Controls widgets.  When no window exists the
    timer falls back to a background thread so it also works from pure
    console programs.

    Usage:
        Timer.Interval = 1000  # 1 second

        def on_tick():
            TextWindow.WriteLine("Tick!")

        Timer.Tick = on_tick  # Auto-starts the timer
        Timer.Stop()          # Stops the timer (also clears the handler)
    """

    Interval: int = 1000

    _min_interval_ms: int = 10

    _tick: Optional[Callable] = None
    _thread: Optional[threading.Thread] = None
    _stop_event: threading.Event = threading.Event()
    _after_id: Optional[str] = None
    _paused: bool = False

    # -- helpers ----------------------------------------------------------

    @classmethod
    def _get_root(cls):
        """Return the live tkinter root (if any) without creating one."""
        from smallbasic._renderer import Renderer
        backend = Renderer._backend
        if backend is None:
            return None
        root = getattr(backend, "_root", None)
        if root is None:
            return None
        try:
            root.winfo_exists()  # raises if the window was destroyed
            return root
        except Exception:
            return None

    @classmethod
    def _call_tick(cls):
        """Invoke the current handler, logging (not swallowing) errors."""
        if cls._tick is not None:
            try:
                cls._tick()
            except Exception as e:
                logger.error("Timer tick callback raised an exception: %s", e)

    # -- event-loop mode (main thread, GUI-safe) --------------------------

    @classmethod
    def _schedule_after(cls):
        if cls._after_id is not None:
            return  # a callback is already pending
        root = cls._get_root()
        if root is None:
            return
        try:
            cls._after_id = root.after(
                max(cls._min_interval_ms, int(cls.Interval)),
                cls._loop_after)
        except Exception:
            cls._after_id = None

    @classmethod
    def _loop_after(cls):
        """Tick handler driven by ``root.after`` on the main thread."""
        cls._after_id = None
        if cls._tick is None:
            return
        if not cls._paused:
            cls._call_tick()
        cls._schedule_after()

    # -- background-thread mode (console programs) ------------------------

    @classmethod
    def _run(cls):
        """Internal timer loop for when no Tk root exists."""
        while not cls._stop_event.is_set():
            if not cls._paused:
                cls._call_tick()
            wait = max(0.01, cls.Interval / 1000.0)
            cls._stop_event.wait(wait)

    # -- lifecycle --------------------------------------------------------

    @classmethod
    def _ensure_running(cls):
        """Start the timer, preferring the Tk event loop when available."""
        root = cls._get_root()
        if root is not None and threading.current_thread() is threading.main_thread():
            cls._stop_event.set()          # retire any legacy background thread
            cls._schedule_after()
        else:
            cls._stop_event.clear()
            if cls._thread is None or not cls._thread.is_alive():
                cls._thread = threading.Thread(target=cls._run, daemon=True)
                cls._thread.start()

    @classmethod
    def Pause(cls) -> None:
        """Pauses the timer. Tick events will not be raised."""
        cls._paused = True

    @classmethod
    def Resume(cls) -> None:
        """Resumes the timer from a paused state."""
        cls._paused = False
        cls._ensure_running()

    @classmethod
    def Stop(cls) -> None:
        """Stops the timer and clears the Tick handler.

        Any pending event-loop callback is cancelled and any background
        thread is woken and retired.  Set ``Timer.Tick`` to a new handler to
        start a fresh timer.
        """
        cls._tick = None
        cls._stop_event.set()
        root = cls._get_root()
        if root is not None and cls._after_id is not None:
            try:
                root.after_cancel(cls._after_id)
            except Exception:
                pass
            cls._after_id = None

    @classproperty
    def Tick(cls) -> Optional[Callable]:
        """Gets or sets the Tick event handler. Auto-starts the timer."""
        return cls._tick

    @Tick.setter
    def Tick(cls, value: Optional[Callable]) -> None:
        cls._tick = value
        if value is not None:
            cls._paused = False
            cls._ensure_running()
        else:
            cls.Stop()
