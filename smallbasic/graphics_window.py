import tkinter as tk
import tkinter.messagebox
import random
from typing import Optional, Callable
from smallbasic._utils import classproperty


class _TkWindow:
    """Singleton wrapper for the tkinter Graphics Window."""
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
        if cls._root is None:
            cls._root = tk.Tk()
            cls._root.withdraw()
            cls._root.protocol("WM_DELETE_WINDOW", cls._on_close)
        return cls._root

    @classmethod
    def _on_close(cls):
        if cls._root:
            cls._root.withdraw()

    @classmethod
    def show(cls):
        cls.ensure()
        if cls._canvas is None:
            cls._canvas = tk.Canvas(
                cls._root,
                width=cls._width,
                height=cls._height,
                bg=cls._bg_color,
                highlightthickness=0
            )
            cls._canvas.pack()
            cls._canvas.bind("<KeyPress>", cls._on_key_down)
            cls._canvas.bind("<KeyRelease>", cls._on_key_up)
            cls._canvas.bind("<Key>", cls._on_key_press)
            cls._canvas.bind("<Button-1>", cls._on_mouse_down)
            cls._canvas.bind("<ButtonRelease-1>", cls._on_mouse_up)
            cls._canvas.bind("<Motion>", cls._on_mouse_move)
            cls._canvas.focus_set()
        if not cls._shown:
            cls._root.deiconify()
            cls._root.title(cls._title)
            cls._root.geometry(f"{cls._width}x{cls._height}+{cls._left}+{cls._top}")
            cls._root.resizable(cls._can_resize, cls._can_resize)
            cls._root.update()
            cls._shown = True

    @classmethod
    def hide(cls):
        if cls._root:
            cls._root.withdraw()
            cls._shown = False

    @classmethod
    def wait_for_close(cls):
        if cls._root:
            cls._root.mainloop()

    @classmethod
    def _on_key_down(cls, event):
        cls._last_key = event.keysym
        if cls.KeyDown and cls._root:
            cls._root.after_idle(cls.KeyDown)

    @classmethod
    def _on_key_up(cls, event):
        cls._last_key = event.keysym
        if cls.KeyUp and cls._root:
            cls._root.after_idle(cls.KeyUp)

    @classmethod
    def _on_key_press(cls, event):
        cls._last_text = event.char
        if cls.TextInput and cls._root:
            cls._root.after_idle(cls.TextInput)

    @classmethod
    def _on_mouse_down(cls, event):
        cls._mouse_x = event.x
        cls._mouse_y = event.y
        if cls.MouseDown and cls._root:
            cls._root.after_idle(cls.MouseDown)

    @classmethod
    def _on_mouse_up(cls, event):
        cls._mouse_x = event.x
        cls._mouse_y = event.y
        if cls.MouseUp and cls._root:
            cls._root.after_idle(cls.MouseUp)

    @classmethod
    def _on_mouse_move(cls, event):
        cls._mouse_x = event.x
        cls._mouse_y = event.y
        if cls.MouseMove and cls._root:
            cls._root.after_idle(cls.MouseMove)

    @classmethod
    def update(cls):
        if cls._root:
            cls._root.update()

    @classmethod
    def destroy(cls):
        if cls._root:
            cls._root.destroy()
            cls._root = None
            cls._canvas = None


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

class _GWMeta(type):
    """Metaclass that forwards event handler assignments to _TkWindow."""

    def __setattr__(cls, name, value):
        if name in _EVENT_NAMES:
            setattr(_TkWindow, name, value)
            return
        if name in _PROP_MAP:
            setattr(_TkWindow, _PROP_MAP[name], value)
            _apply_setting(name)
            return
        super().__setattr__(name, value)

    def __getattr__(cls, name):
        if name in _EVENT_NAMES:
            return getattr(_TkWindow, name)
        if name in _PROP_MAP:
            return getattr(_TkWindow, _PROP_MAP[name])
        raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")


def _apply_setting(name):
    root, canvas = _TkWindow._root, _TkWindow._canvas
    if name == 'BackgroundColor' and canvas:
        canvas.config(bg=_TkWindow._bg_color)
    elif name == 'Title' and root:
        root.title(_TkWindow._title)
    elif name in ('Width', 'Height', 'Left', 'Top') and root:
        root.geometry(f"{_TkWindow._width}x{_TkWindow._height}"
                       f"+{_TkWindow._left}+{_TkWindow._top}")
    elif name == 'CanResize' and root:
        root.resizable(_TkWindow._can_resize, _TkWindow._can_resize)


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



    # --- Methods ---

    @classmethod
    def Show(cls) -> None:
        _TkWindow.show()

    @classmethod
    def Hide(cls) -> None:
        _TkWindow.hide()

    @classmethod
    def Wait(cls) -> None:
        _TkWindow.wait_for_close()

    @classmethod
    def Clear(cls) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            _TkWindow._canvas.delete("all")

    @classmethod
    def ShowMessage(cls, text: str, title: str) -> None:
        _TkWindow.ensure()
        tk.messagebox.showinfo(title, text)

    @classmethod
    def DrawRectangle(cls, x: int, y: int, width: int, height: int) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            _TkWindow._canvas.create_rectangle(
                x, y, x + width, y + height,
                outline=_TkWindow._pen_color,
                width=_TkWindow._pen_width
            )
            _TkWindow.update()

    @classmethod
    def FillRectangle(cls, x: int, y: int, width: int, height: int) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            _TkWindow._canvas.create_rectangle(
                x, y, x + width, y + height,
                fill=_TkWindow._brush_color,
                outline=_TkWindow._pen_color,
                width=_TkWindow._pen_width
            )
            _TkWindow.update()

    @classmethod
    def DrawEllipse(cls, x: int, y: int, width: int, height: int) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            _TkWindow._canvas.create_oval(
                x, y, x + width, y + height,
                outline=_TkWindow._pen_color,
                width=_TkWindow._pen_width
            )
            _TkWindow.update()

    @classmethod
    def FillEllipse(cls, x: int, y: int, width: int, height: int) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            _TkWindow._canvas.create_oval(
                x, y, x + width, y + height,
                fill=_TkWindow._brush_color,
                outline=_TkWindow._pen_color,
                width=_TkWindow._pen_width
            )
            _TkWindow.update()

    @classmethod
    def DrawTriangle(cls, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            _TkWindow._canvas.create_polygon(
                x1, y1, x2, y2, x3, y3,
                outline=_TkWindow._pen_color,
                width=_TkWindow._pen_width,
                fill=""
            )
            _TkWindow.update()

    @classmethod
    def FillTriangle(cls, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            _TkWindow._canvas.create_polygon(
                x1, y1, x2, y2, x3, y3,
                fill=_TkWindow._brush_color,
                outline=_TkWindow._pen_color,
                width=_TkWindow._pen_width
            )
            _TkWindow.update()

    @classmethod
    def DrawLine(cls, x1: int, y1: int, x2: int, y2: int) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            _TkWindow._canvas.create_line(
                x1, y1, x2, y2,
                fill=_TkWindow._pen_color,
                width=_TkWindow._pen_width
            )
            _TkWindow.update()

    @classmethod
    def DrawText(cls, x: int, y: int, text: str) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            weight = "bold" if _TkWindow._font_bold else "normal"
            slant = "italic" if _TkWindow._font_italic else "roman"
            _TkWindow._canvas.create_text(
                x, y, text=text, anchor="nw",
                font=(_TkWindow._font_name, _TkWindow._font_size, weight, slant),
                fill=_TkWindow._pen_color
            )
            _TkWindow.update()

    @classmethod
    def DrawBoundText(cls, x: int, y: int, width: int, text: str) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            weight = "bold" if _TkWindow._font_bold else "normal"
            slant = "italic" if _TkWindow._font_italic else "roman"
            _TkWindow._canvas.create_text(
                x, y, text=text, anchor="nw", width=width,
                font=(_TkWindow._font_name, _TkWindow._font_size, weight, slant),
                fill=_TkWindow._pen_color
            )
            _TkWindow.update()

    @classmethod
    def DrawImage(cls, image_name: str, x: int, y: int) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            from smallbasic.imagelist import ImageList
            img = ImageList._tk_images.get(image_name)
            if img:
                _TkWindow._canvas.create_image(x, y, image=img, anchor="nw")
                _TkWindow.update()

    _resized_images: dict = {}

    @classmethod
    def DrawResizedImage(cls, image_name: str, x: int, y: int, width: int, height: int) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            from smallbasic.imagelist import ImageList
            img = ImageList._tk_images.get(image_name)
            if img:
                resized = img.zoom(
                    max(1, width // max(img.width(), 1)),
                    max(1, height // max(img.height(), 1))
                )
                key = f"{image_name}_{width}x{height}"
                cls._resized_images[key] = resized
                _TkWindow._canvas.create_image(x, y, image=resized, anchor="nw")
                _TkWindow.update()

    @classmethod
    def SetPixel(cls, x: int, y: int, color: str) -> None:
        _TkWindow.ensure()
        if _TkWindow._canvas:
            _TkWindow._canvas.create_line(x, y, x + 1, y, fill=color, width=1)
            _TkWindow.update()

    @classmethod
    def GetPixel(cls, x: int, y: int) -> str:
        return _TkWindow._pen_color

    @classmethod
    def GetRandomColor(cls) -> str:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"#{r:02X}{g:02X}{b:02X}"

    @classmethod
    def GetColorFromRGB(cls, red: int, green: int, blue: int) -> str:
        return f"#{max(0, min(255, red)):02X}{max(0, min(255, green)):02X}{max(0, min(255, blue)):02X}"
