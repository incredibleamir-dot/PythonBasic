import ctypes
from smallbasic._utils import classproperty


class Mouse:
    """
    Provides access to get or set mouse properties like cursor position.
    
    Usage:
        x = Mouse.MouseX
        y = Mouse.MouseY
        Mouse.HideCursor()
    """

    _x: int = 0
    _y: int = 0

    @classproperty
    def MouseX(cls) -> int:
        """Gets or sets the mouse cursor's x co-ordinate."""
        try:
            point = ctypes.wintypes.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
            cls._x = point.x
            return point.x
        except Exception:
            return cls._x

    @MouseX.setter
    def MouseX(cls, value: int) -> None:
        try:
            y = cls.MouseY
            ctypes.windll.user32.SetCursorPos(int(value), y)
            cls._x = int(value)
        except Exception:
            cls._x = int(value)

    @classproperty
    def MouseY(cls) -> int:
        """Gets or sets the mouse cursor's y co-ordinate."""
        try:
            point = ctypes.wintypes.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
            cls._y = point.y
            return point.y
        except Exception:
            return cls._y

    @MouseY.setter
    def MouseY(cls, value: int) -> None:
        try:
            x = cls.MouseX
            ctypes.windll.user32.SetCursorPos(x, int(value))
            cls._y = int(value)
        except Exception:
            cls._y = int(value)

    @classproperty
    def IsLeftButtonDown(cls) -> bool:
        """Gets whether the left mouse button is pressed."""
        try:
            return (ctypes.windll.user32.GetAsyncKeyState(0x01) & 0x8000) != 0
        except Exception:
            return False

    @classproperty
    def IsRightButtonDown(cls) -> bool:
        """Gets whether the right mouse button is pressed."""
        try:
            return (ctypes.windll.user32.GetAsyncKeyState(0x02) & 0x8000) != 0
        except Exception:
            return False

    @classmethod
    def HideCursor(cls) -> None:
        """Hides the mouse cursor on the screen."""
        try:
            ctypes.windll.user32.ShowCursor(False)
        except Exception:
            pass

    @classmethod
    def ShowCursor(cls) -> None:
        """Shows the mouse cursor on the screen."""
        try:
            ctypes.windll.user32.ShowCursor(True)
        except Exception:
            pass
