# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : GraphicsWindow object - public drawing API, properties and events.
# Version : 1.7.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

"""
GraphicsWindow — public API for 2D drawing and events.

Drawing operations are delegated to ``smallbasic._renderer.Renderer``.
All property/event state is owned by ``smallbasic._state.GraphicsState``;
this module only forwards public property assignments to it.
"""

from smallbasic._state import GraphicsState
from smallbasic._renderer import Renderer


# ── Event names & property map ─────────────────────────────────────

_EVENT_NAMES = {'KeyDown', 'KeyUp', 'MouseDown', 'MouseUp', 'MouseMove', 'TextInput'}

# Public property name -> GraphicsState attribute
_PROP_MAP = {
    'BackgroundColor': 'bg_color',
    'BrushColor': 'brush_color',
    'PenColor': 'pen_color',
    'PenWidth': 'pen_width',
    'FontName': 'font_name',
    'FontSize': 'font_size',
    'FontBold': 'font_bold',
    'FontItalic': 'font_italic',
    'Title': 'title',
    'Width': 'width',
    'Height': 'height',
    'Left': 'left',
    'Top': 'top',
    'CanResize': 'can_resize',
    'LastKey': 'last_key',
    'LastText': 'last_text',
    'MouseX': 'mouse_x',
    'MouseY': 'mouse_y',
}


class _GWMeta(type):
    """Metaclass that forwards property / event assignments to GraphicsState."""

    def __setattr__(cls, name, value):
        if name in _EVENT_NAMES:
            setattr(GraphicsState, name, value)
            return
        if name in _PROP_MAP:
            setattr(GraphicsState, _PROP_MAP[name], value)
            _apply_setting(name)
            return
        super().__setattr__(name, value)

    def __getattr__(cls, name):
        if name in _EVENT_NAMES:
            return getattr(GraphicsState, name)
        if name in _PROP_MAP:
            return getattr(GraphicsState, _PROP_MAP[name])
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
