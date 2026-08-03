# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Turtle object - Logo-style turtle graphics on the graphics window.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

"""
Turtle — Logo-style turtle graphics.

Draws on the GraphicsWindow canvas through the internal Renderer.
"""

import math
from smallbasic._utils import classproperty, _PropSetMeta
from smallbasic._state import GraphicsState
from smallbasic._renderer import Renderer
from smallbasic.graphics_window import GraphicsWindow


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
        if Renderer._canvas is None:
            GraphicsWindow.Show()
        if cls._turtle_dot_id is None:
            cls._turtle_dot_id = Renderer.create_oval(
                cls._x - 5, cls._y - 5, cls._x + 5, cls._y + 5,
                fill="Red", outline="Black", width=2
            )
            cls._arrow_line_id = Renderer.create_line(
                cls._x, cls._y, cls._x, cls._y,
                fill="Red", width=2
            )
            cls._draw_arrow()

    @classmethod
    def _draw_arrow(cls):
        if cls._turtle_dot_id is None:
            return
        angle_rad = math.radians(cls._angle)
        length = 15
        ex = cls._x + length * math.cos(angle_rad)
        ey = cls._y - length * math.sin(angle_rad)
        if cls._turtle_dot_id is not None:
            Renderer.coords(cls._turtle_dot_id,
                             cls._x - 5, cls._y - 5,
                             cls._x + 5, cls._y + 5)
        if cls._arrow_line_id:
            Renderer.coords(cls._arrow_line_id,
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
            cls._draw_arrow()

    @classproperty
    def Y(cls) -> float:
        return cls._y

    @Y.setter
    def Y(cls, value: float) -> None:
        cls._y = float(value)
        if cls._visible:
            cls._ensure_window()
            cls._draw_arrow()

    @classmethod
    def Show(cls) -> None:
        cls._visible = True
        cls._ensure_window()

    @classmethod
    def Hide(cls) -> None:
        cls._visible = False
        if cls._turtle_dot_id is not None:
            Renderer.delete(cls._turtle_dot_id)
            cls._turtle_dot_id = None
        if cls._arrow_line_id is not None:
            Renderer.delete(cls._arrow_line_id)
            cls._arrow_line_id = None
        Renderer.flush()

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

        if cls._pen_down:
            Renderer.create_line(
                start_x, start_y, cls._x, cls._y,
                fill=GraphicsState.pen_color,
                width=GraphicsState.pen_width
            )
        cls._draw_arrow()
        Renderer.flush()
        if cls._speed < 10:
            delay_ms = max(5, (10 - cls._speed) * 10)
            Renderer.pump_wait(delay_ms)

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
