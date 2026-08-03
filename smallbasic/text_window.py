# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : TextWindow object - console text input and output.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

import sys
import ctypes
from smallbasic._utils import classproperty, _PropSetMeta


class _COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]


class _SMALL_RECT(ctypes.Structure):
    _fields_ = [
        ("Left", ctypes.c_short), ("Top", ctypes.c_short),
        ("Right", ctypes.c_short), ("Bottom", ctypes.c_short),
    ]


class _CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", _COORD),
        ("dwCursorPosition", _COORD),
        ("wAttributes", ctypes.c_ushort),
        ("srWindow", _SMALL_RECT),
        ("dwMaximumWindowSize", _COORD),
    ]


def _get_cursor_position():
    """Return the console cursor (column, row) or (0, 0) on failure."""
    try:
        std_handle = ctypes.windll.kernel32.GetStdHandle(-11)
        buf = _CONSOLE_SCREEN_BUFFER_INFO()
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(
            std_handle, ctypes.byref(buf))
        return int(buf.dwCursorPosition.X), int(buf.dwCursorPosition.Y)
    except Exception:
        return 0, 0


def _set_cursor_position(x, y):
    """Position the console cursor at (column, row); no-op on failure."""
    try:
        std_handle = ctypes.windll.kernel32.GetStdHandle(-11)
        coord = (int(x) & 0xFFFF) | ((int(y) & 0xFFFF) << 16)
        ctypes.windll.kernel32.SetConsoleCursorPosition(std_handle, coord)
    except Exception:
        pass


class _ConsoleWindow:
    """Manages the text console window."""
    _foreground: str = "White"
    _background: str = "Black"
    _title: str = "Small Basic Text Window"
    _left: int = 100
    _top: int = 100
    _visible: bool = False

    @classmethod
    def apply_colors(cls):
        if sys.stdout.isatty():
            try:
                import ctypes
                std_handle = ctypes.windll.kernel32.GetStdHandle(-11)
                colors = {
                    "Black": 0, "DarkBlue": 1, "DarkGreen": 2,
                    "DarkCyan": 3, "DarkRed": 4, "DarkMagenta": 5,
                    "DarkYellow": 6, "Gray": 7, "DarkGray": 8,
                    "Blue": 9, "Green": 10, "Cyan": 11, "Red": 12,
                    "Magenta": 13, "Yellow": 14, "White": 15,
                }
                fg = colors.get(cls._foreground, 7)
                bg = colors.get(cls._background, 0)
                ctypes.windll.kernel32.SetConsoleTextAttribute(std_handle, fg | (bg << 4))
            except Exception:
                pass

    @classmethod
    def set_title(cls, title: str):
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        except Exception:
            pass


class TextWindow(metaclass=_PropSetMeta):
    """
    Provides text input and output in the console.
    
    Usage:
        TextWindow.Show()
        TextWindow.WriteLine("Hello, World!")
        name = TextWindow.Read()
        number = TextWindow.ReadNumber()
    """

    @classmethod
    def Show(cls) -> None:
        _ConsoleWindow._visible = True
        _ConsoleWindow.apply_colors()
        _ConsoleWindow.set_title(_ConsoleWindow._title)
        print()

    @classmethod
    def Hide(cls) -> None:
        _ConsoleWindow._visible = False
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass

    @classmethod
    def Clear(cls) -> None:
        try:
            import os
            os.system("cls" if os.name == "nt" else "clear")
        except Exception:
            print("\n" * 50)

    @classmethod
    def Pause(cls) -> None:
        if _ConsoleWindow._visible:
            input("Press ENTER to continue...")

    @classmethod
    def PauseIfVisible(cls) -> None:
        if _ConsoleWindow._visible:
            cls.Pause()

    @classmethod
    def PauseWithoutMessage(cls) -> None:
        input()

    @classmethod
    def Read(cls) -> str:
        return input()

    @classmethod
    def ReadKey(cls) -> str:
        try:
            import msvcrt
            return msvcrt.getch().decode("utf-8", errors="replace")
        except Exception:
            return input()[:1]

    @classmethod
    def ReadNumber(cls) -> float:
        while True:
            try:
                return float(input())
            except ValueError:
                print("Please enter a valid number:")

    @classmethod
    def WriteLine(cls, *args) -> None:
        _ConsoleWindow.apply_colors()
        print(" ".join(str(a) for a in args))

    @classmethod
    def Write(cls, *args) -> None:
        _ConsoleWindow.apply_colors()
        print(" ".join(str(a) for a in args), end="", flush=True)

    @classproperty
    def ForegroundColor(cls) -> str:
        """Gets or sets the foreground color of text."""
        return _ConsoleWindow._foreground

    @ForegroundColor.setter
    def ForegroundColor(cls, value: str) -> None:
        _ConsoleWindow._foreground = value
        _ConsoleWindow.apply_colors()

    @classproperty
    def BackgroundColor(cls) -> str:
        """Gets or sets the background color of text."""
        return _ConsoleWindow._background

    @BackgroundColor.setter
    def BackgroundColor(cls, value: str) -> None:
        _ConsoleWindow._background = value
        _ConsoleWindow.apply_colors()

    @classproperty
    def CursorLeft(cls) -> int:
        """Gets or sets the cursor's column position."""
        x, _ = _get_cursor_position()
        return x

    @CursorLeft.setter
    def CursorLeft(cls, value: int) -> None:
        x, y = _get_cursor_position()
        _set_cursor_position(value, y)

    @classproperty
    def CursorTop(cls) -> int:
        """Gets or sets the cursor's row position."""
        _, y = _get_cursor_position()
        return y

    @CursorTop.setter
    def CursorTop(cls, value: int) -> None:
        x, y = _get_cursor_position()
        _set_cursor_position(x, value)

    @classproperty
    def Left(cls) -> int:
        """Gets or sets the left position of the Text Window."""
        return _ConsoleWindow._left

    @Left.setter
    def Left(cls, value: int) -> None:
        _ConsoleWindow._left = int(value)

    @classproperty
    def Top(cls) -> int:
        """Gets or sets the top position of the Text Window."""
        return _ConsoleWindow._top

    @Top.setter
    def Top(cls, value: int) -> None:
        _ConsoleWindow._top = int(value)

    @classproperty
    def Title(cls) -> str:
        """Gets or sets the title for the text window."""
        return _ConsoleWindow._title

    @Title.setter
    def Title(cls, value: str) -> None:
        _ConsoleWindow._title = value
        _ConsoleWindow.set_title(value)

    @classmethod
    def VerifyAccess(cls) -> None:
        pass
