# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Central GraphicsState singleton holding all shared window/pen/brush/font state.
# Version : 1.7.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

"""
Centralized graphics state for Python Small Basic.

GraphicsState is the single owner of all shared state for the graphics
subsystem.  Every graphics module reads pen/brush/font/window state from
here, so there is no duplicated mirror state to keep in sync.
"""

from typing import Optional, Callable


class GraphicsState:
    """Holds all mutable state for the graphics subsystem."""

    # Window
    width: int = 640
    height: int = 480
    left: int = 100
    top: int = 100
    title: str = "Small Basic Graphics Window"
    bg_color: str = "White"
    can_resize: bool = True

    # Pen
    pen_color: str = "Black"
    pen_width: int = 2

    # Brush
    brush_color: str = "Gray"

    # Font
    font_name: str = "Consolas"
    font_size: int = 12
    font_bold: bool = False
    font_italic: bool = False

    # Event state
    last_key: str = ""
    last_text: str = ""
    mouse_x: int = 0
    mouse_y: int = 0

    # Event callbacks
    KeyDown: Optional[Callable] = None
    KeyUp: Optional[Callable] = None
    MouseDown: Optional[Callable] = None
    MouseUp: Optional[Callable] = None
    MouseMove: Optional[Callable] = None
    TextInput: Optional[Callable] = None
