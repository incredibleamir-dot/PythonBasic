import math
import sys
import time
from smallbasic._utils import classproperty, _PropSetMeta
from smallbasic.graphics_window import _TkWindow, GraphicsWindow


def _flush_display():
    if not _TkWindow._root:
        return
    _TkWindow._root.update_idletasks()
    if sys.platform == 'win32':
        import ctypes.wintypes
        hwnd = ctypes.wintypes.HWND(_TkWindow._root.winfo_id())
        ctypes.windll.user32.UpdateWindow(hwnd)
    else:
        _TkWindow._root.update()


class Turtle(metaclass=_PropSetMeta):
    _speed: int = 5
    _angle: float = 0.0
    _x: float = 320.0
    _y: float = 240.0
    _pen_down: bool = True
    _visible: bool = False
    _turtle_dot_id = None
    _arrow_line_id = None

    @classmethod
    def _ensure_window(cls):
        if _TkWindow._canvas is None:
            GraphicsWindow.Show()
        if cls._turtle_dot_id is None and _TkWindow._canvas:
            r = 5
            cls._turtle_dot_id = _TkWindow._canvas.create_oval(
                cls._x - r, cls._y - r, cls._x + r, cls._y + r,
                fill="Red", outline="Black", width=2
            )
            cls._arrow_line_id = _TkWindow._canvas.create_line(
                cls._x, cls._y, cls._x, cls._y,
                fill="Red", width=2
            )
            cls._draw_arrow()

    @classmethod
    def _draw_arrow(cls):
        if not _TkWindow._canvas or cls._turtle_dot_id is None:
            return
        angle_rad = math.radians(cls._angle)
        length = 15
        ex = cls._x + length * math.cos(angle_rad)
        ey = cls._y - length * math.sin(angle_rad)
        _TkWindow._canvas.coords(cls._turtle_dot_id,
                                  cls._x - 5, cls._y - 5,
                                  cls._x + 5, cls._y + 5)
        if cls._arrow_line_id:
            _TkWindow._canvas.coords(cls._arrow_line_id,
                                      cls._x, cls._y, ex, ey)

    @classproperty
    def Speed(cls) -> int:
        return cls._speed

    @Speed.setter
    def Speed(cls, value: int) -> None:
        cls._speed = max(1, min(10, int(value)))

    @classproperty
    def Angle(cls) -> float:
        return cls._angle

    @Angle.setter
    def Angle(cls, value: float) -> None:
        cls._angle = float(value)
        cls._draw_arrow()

    @classproperty
    def X(cls) -> float:
        return cls._x

    @X.setter
    def X(cls, value: float) -> None:
        cls._x = float(value)
        if cls._visible:
            cls._ensure_window()

    @classproperty
    def Y(cls) -> float:
        return cls._y

    @Y.setter
    def Y(cls, value: float) -> None:
        cls._y = float(value)
        if cls._visible:
            cls._ensure_window()

    @classmethod
    def Show(cls) -> None:
        cls._visible = True
        cls._ensure_window()

    @classmethod
    def Hide(cls) -> None:
        cls._visible = False
        if cls._turtle_dot_id and _TkWindow._canvas:
            _TkWindow._canvas.delete(cls._turtle_dot_id)
            cls._turtle_dot_id = None
        if cls._arrow_line_id and _TkWindow._canvas:
            _TkWindow._canvas.delete(cls._arrow_line_id)
            cls._arrow_line_id = None
        _flush_display()

    @classmethod
    def PenDown(cls) -> None:
        cls._pen_down = True

    @classmethod
    def PenUp(cls) -> None:
        cls._pen_down = False

    @classmethod
    def Move(cls, distance: float) -> None:
        cls._ensure_window()
        start_x, start_y = cls._x, cls._y
        angle_rad = math.radians(cls._angle)
        cls._x += distance * math.cos(angle_rad)
        cls._y -= distance * math.sin(angle_rad)

        canvas = _TkWindow._canvas
        if canvas:
            if cls._pen_down:
                canvas.create_line(
                    start_x, start_y, cls._x, cls._y,
                    fill=_TkWindow._pen_color,
                    width=_TkWindow._pen_width
                )
            cls._draw_arrow()
            _flush_display()
            if cls._speed < 10:
                delay_ms = max(5, (10 - cls._speed) * 10)
                time.sleep(delay_ms / 1000.0)

    @classmethod
    def MoveTo(cls, x: float, y: float) -> None:
        dx = x - cls._x
        dy = cls._y - y
        if dx != 0 or dy != 0:
            cls._angle = math.degrees(math.atan2(-dy, dx))
        cls.Move(math.sqrt(dx * dx + dy * dy))

    @classmethod
    def Turn(cls, angle: float) -> None:
        cls._angle = (cls._angle + angle) % 360
        cls._draw_arrow()

    @classmethod
    def TurnRight(cls) -> None:
        cls.Turn(-90)

    @classmethod
    def TurnLeft(cls) -> None:
        cls.Turn(90)
