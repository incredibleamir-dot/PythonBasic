# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : GraphicsWindow object - public drawing API, properties and events.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

"""
GraphicsWindow — public API for 2D drawing and events.

This module provides the GraphicsWindow class (the public API)
and the _TkWindow class (internal singleton that other modules
such as Controls import for the tkinter root window).

Drawing operations are delegated to smallbasic._renderer.Renderer.
Shared state lives in smallbasic._state.GraphicsState.
"""

import tkinter as tk
import tkinter.messagebox
from typing import Optional, Callable
from smallbasic._utils import classproperty
from smallbasic._state import GraphicsState
from smallbasic._renderer import Renderer


# ── Backward-compatible window handle for Controls & ImageList ─────

class _TkWindow:
    """Internal singleton — wraps Renderer for backward compatibility.

    Controls and ImageList import this class to access the tkinter
    root window.  New code should use GraphicsState / Renderer directly.
    """
    _instance = None
    _root: Optional[tk.Tk] = None
    _canvas: Optional[tk.Canvas] = None
    _width: int = 640
    _height: int = 480
    _left: int = 100
    _top: int = 100
    _title: str = "Small Basic Graphics Window"
    _bg_color: str = "White"
    _pen_color: str = "Black"
    _pen_width: int = 2
    _brush_color: str = "Gray"
    _font_name: str = "Consolas"
    _font_size: int = 12
    _font_bold: bool = False
    _font_italic: bool = False
    _can_resize: bool = True
    _last_key: str = ""
    _last_text: str = ""
    _mouse_x: int = 0
    _mouse_y: int = 0
    _shown: bool = False

    KeyDown: Optional[Callable] = None
    KeyUp: Optional[Callable] = None
    MouseDown: Optional[Callable] = None
    MouseUp: Optional[Callable] = None
    MouseMove: Optional[Callable] = None
    TextInput: Optional[Callable] = None
    ButtonClicked: Optional[Callable] = None
    TextTyped: Optional[Callable] = None

    @classmethod
    def ensure(cls):
        root = Renderer.ensure()
        cls._root = root
        cls._canvas = Renderer._canvas
        return root

    @classmethod
    def _on_close(cls):
        Renderer._on_close()

    @classmethod
    def show(cls):
        Renderer.show()
        cls._root = Renderer._root
        cls._canvas = Renderer._canvas

    @classmethod
    def hide(cls):
        Renderer.hide()

    @classmethod
    def wait_for_close(cls):
        Renderer.wait_for_close()

    @classmethod
    def update(cls):
        Renderer.update()

    @classmethod
    def destroy(cls):
        Renderer.destroy()
        cls._root = None
        cls._canvas = None


# ── Event names & property map ─────────────────────────────────────

_EVENT_NAMES = {'KeyDown', 'KeyUp', 'MouseDown', 'MouseUp', 'MouseMove', 'TextInput'}

_PROP_MAP = {
    'BackgroundColor': '_bg_color',
    'BrushColor': '_brush_color',
    'PenColor': '_pen_color',
    'PenWidth': '_pen_width',
    'FontName': '_font_name',
    'FontSize': '_font_size',
    'FontBold': '_font_bold',
    'FontItalic': '_font_italic',
    'Title': '_title',
    'Width': '_width',
    'Height': '_height',
    'Left': '_left',
    'Top': '_top',
    'CanResize': '_can_resize',
    'LastKey': '_last_key',
    'LastText': '_last_text',
    'MouseX': '_mouse_x',
    'MouseY': '_mouse_y',
}

# Mirror mapping: GraphicsState attribute -> _TkWindow attribute
_STATE_ATTR = {
    '_bg_color': 'bg_color',
    '_brush_color': 'brush_color',
    '_pen_color': 'pen_color',
    '_pen_width': 'pen_width',
    '_font_name': 'font_name',
    '_font_size': 'font_size',
    '_font_bold': 'font_bold',
    '_font_italic': 'font_italic',
    '_title': 'title',
    '_width': 'width',
    '_height': 'height',
    '_left': 'left',
    '_top': 'top',
    '_can_resize': 'can_resize',
    '_last_key': 'last_key',
    '_last_text': 'last_text',
    '_mouse_x': 'mouse_x',
    '_mouse_y': 'mouse_y',
}


class _GWMeta(type):
    """Metaclass that forwards property / event assignments to both
    GraphicsState (canonical) and _TkWindow (backward compat)."""

    def __setattr__(cls, name, value):
        if name in _EVENT_NAMES:
            setattr(GraphicsState, name, value)
            setattr(_TkWindow, name, value)
            return
        if name in _PROP_MAP:
            tk_attr = _PROP_MAP[name]
            setattr(_TkWindow, tk_attr, value)
            state_attr = _STATE_ATTR.get(tk_attr)
            if state_attr:
                setattr(GraphicsState, state_attr, value)
            _apply_setting(name)
            return
        super().__setattr__(name, value)

    def __getattr__(cls, name):
        if name in _EVENT_NAMES:
            return getattr(GraphicsState, name)
        if name in _PROP_MAP:
            tk_attr = _PROP_MAP[name]
            state_attr = _STATE_ATTR.get(tk_attr)
            if state_attr:
                return getattr(GraphicsState, state_attr)
            return getattr(_TkWindow, tk_attr)
        raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")


def _apply_setting(name):
    """Apply a property change to the live window/canvas."""
    b = Renderer._backend
    if b is None:
        return  # window not created yet; settings are applied on Show()
    s = GraphicsState
    if name == 'BackgroundColor':
        b.set_bg(s.bg_color)
    elif name == 'Title':
        b.set_title(s.title)
    elif name in ('Width', 'Height', 'Left', 'Top'):
        b.set_geometry(s.width, s.height, s.left, s.top)
    elif name == 'CanResize':
        b.set_resizable(s.can_resize)


# ── Public API ─────────────────────────────────────────────────────

class GraphicsWindow(metaclass=_GWMeta):
    """
    Provides graphics input and output functionality.

    You can draw and fill shapes, display text, show images,
    and handle mouse/keyboard events.

    Usage:
        GraphicsWindow.Show()
        GraphicsWindow.Title = "My Drawing"
        GraphicsWindow.DrawRectangle(10, 10, 100, 50)
        GraphicsWindow.DrawEllipse(50, 50, 80, 80)
    """

    @classmethod
    def Show(cls) -> None:
        Renderer.show()

    @classmethod
    def Hide(cls) -> None:
        Renderer.hide()

    @classmethod
    def Wait(cls) -> None:
        Renderer.wait_for_close()

    @classmethod
    def Clear(cls) -> None:
        Renderer.clear()

    @classmethod
    def BeginBatch(cls) -> None:
        """Begin a batch rendering scope.

        Calls to drawing methods inside a batch are rendered
        immediately to the internal canvas but the display is
        not updated until EndBatch() is called.  Use this when
        drawing many objects at once to avoid redundant refreshes.

        Batches can be nested.  Each BeginBatch() must be paired
        with a matching EndBatch().
        """
        Renderer.begin_batch()

    @classmethod
    def EndBatch(cls) -> None:
        """End a batch rendering scope and flush deferred updates."""
        Renderer.end_batch()

    @classmethod
    def ShowMessage(cls, text: str, title: str) -> None:
        Renderer.backend().show_message(title, text)

    @classmethod
    def DrawRectangle(cls, x: int, y: int, width: int, height: int) -> None:
        Renderer.draw_rectangle(x, y, width, height)

    @classmethod
    def FillRectangle(cls, x: int, y: int, width: int, height: int) -> None:
        Renderer.fill_rectangle(x, y, width, height)

    @classmethod
    def DrawEllipse(cls, x: int, y: int, width: int, height: int) -> None:
        Renderer.draw_ellipse(x, y, width, height)

    @classmethod
    def FillEllipse(cls, x: int, y: int, width: int, height: int) -> None:
        Renderer.fill_ellipse(x, y, width, height)

    @classmethod
    def DrawTriangle(cls, x1: int, y1: int, x2: int, y2: int,
                     x3: int, y3: int) -> None:
        Renderer.draw_triangle(x1, y1, x2, y2, x3, y3)

    @classmethod
    def FillTriangle(cls, x1: int, y1: int, x2: int, y2: int,
                     x3: int, y3: int) -> None:
        Renderer.fill_triangle(x1, y1, x2, y2, x3, y3)

    @classmethod
    def DrawLine(cls, x1: int, y1: int, x2: int, y2: int) -> None:
        Renderer.draw_line(x1, y1, x2, y2)

    @classmethod
    def DrawText(cls, x: int, y: int, text: str) -> None:
        Renderer.draw_text(x, y, text)

    @classmethod
    def DrawBoundText(cls, x: int, y: int, width: int, text: str) -> None:
        Renderer.draw_text(x, y, text, width=width)

    @classmethod
    def DrawImage(cls, image_name: str, x: int, y: int) -> None:
        Renderer.draw_image(image_name, x, y)

    _resized_images: dict = {}

    @classmethod
    def DrawResizedImage(cls, image_name: str, x: int, y: int,
                         width: int, height: int) -> None:
        Renderer.draw_resized_image(image_name, x, y, width, height)

    @classmethod
    def SetPixel(cls, x: int, y: int, color: str) -> None:
        Renderer.set_pixel(x, y, color)

    @classmethod
    def GetPixel(cls, x: int, y: int) -> str:
        return Renderer.get_pixel(x, y)

    @classmethod
    def GetRandomColor(cls) -> str:
        return Renderer.get_random_color()

    @classmethod
    def GetColorFromRGB(cls, red: int, green: int, blue: int) -> str:
        return Renderer.get_color_from_rgb(red, green, blue)
