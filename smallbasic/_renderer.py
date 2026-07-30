"""
Internal Renderer — owns every interaction with the tkinter Canvas.

No other module should call Canvas methods directly.
All drawing, object management, and display updates go through here.
"""

import tkinter as tk
import math
import random
import sys
import time
from typing import Optional, Any
from smallbasic._state import GraphicsState


class Renderer:
    """Singleton-style renderer that owns the tkinter window and canvas."""

    _root: Optional[tk.Tk] = None
    _canvas: Optional[tk.Canvas] = None
    _objects: dict = {}        # canvas id -> metadata dict
    _resized_images: dict = {}
    _shown: bool = False
    _batch_count: int = 0      # > 0 when inside begin_batch / end_batch
    _batch_dirty: bool = False # True if update was called while batching

    # ── Window management ──────────────────────────────────────────

    @classmethod
    def ensure(cls) -> tk.Tk:
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
            s = GraphicsState
            cls._canvas = tk.Canvas(
                cls._root,
                width=s.width,
                height=s.height,
                bg=s.bg_color,
                highlightthickness=0
            )
            cls._canvas.pack()
            cls._canvas.bind("<KeyPress>", cls._on_key_down)
            cls._canvas.bind("<KeyRelease>", cls._on_key_up)
            cls._canvas.bind("<Key>", cls._on_key_press)
            for b in ("1", "2", "3"):
                cls._canvas.bind(f"<Button-{b}>", cls._on_mouse_down)
                cls._canvas.bind(f"<ButtonRelease-{b}>", cls._on_mouse_up)
            cls._canvas.bind("<Motion>", cls._on_mouse_move)
            cls._canvas.focus_set()
        if not cls._shown:
            s = GraphicsState
            cls._root.deiconify()
            cls._root.title(s.title)
            cls._root.geometry(f"{s.width}x{s.height}+{s.left}+{s.top}")
            cls._root.resizable(s.can_resize, s.can_resize)
            cls._do_update()
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
    def destroy(cls):
        if cls._root:
            cls._root.destroy()
            cls._root = None
            cls._canvas = None
            cls._objects.clear()

    # ── Event handlers ─────────────────────────────────────────────

    @classmethod
    def _on_key_down(cls, event):
        GraphicsState.last_key = event.keysym
        if GraphicsState.KeyDown and cls._root:
            cls._root.after_idle(lambda e=event: GraphicsState.KeyDown(e))

    @classmethod
    def _on_key_up(cls, event):
        GraphicsState.last_key = event.keysym
        if GraphicsState.KeyUp and cls._root:
            cls._root.after_idle(lambda e=event: GraphicsState.KeyUp(e))

    @classmethod
    def _on_key_press(cls, event):
        GraphicsState.last_text = event.char
        if GraphicsState.TextInput and cls._root:
            cls._root.after_idle(lambda e=event: GraphicsState.TextInput(e))

    @classmethod
    def _on_mouse_down(cls, event):
        GraphicsState.mouse_x = event.x
        GraphicsState.mouse_y = event.y
        if GraphicsState.MouseDown and cls._root:
            cls._root.after_idle(lambda e=event: GraphicsState.MouseDown(e))

    @classmethod
    def _on_mouse_up(cls, event):
        GraphicsState.mouse_x = event.x
        GraphicsState.mouse_y = event.y
        if GraphicsState.MouseUp and cls._root:
            cls._root.after_idle(lambda e=event: GraphicsState.MouseUp(e))

    @classmethod
    def _on_mouse_move(cls, event):
        GraphicsState.mouse_x = event.x
        GraphicsState.mouse_y = event.y
        if GraphicsState.MouseMove and cls._root:
            cls._root.after_idle(lambda e=event: GraphicsState.MouseMove(e))

    # ── Batch support ──────────────────────────────────────────────

    @classmethod
    def begin_batch(cls):
        """Begin a batch scope.  Calls to update() inside the scope
        are deferred until end_batch() is called."""
        cls._batch_count += 1

    @classmethod
    def end_batch(cls):
        """End a batch scope.  If this was the outermost scope and
        updates were deferred, a single update is fired now."""
        if cls._batch_count > 0:
            cls._batch_count -= 1
        if cls._batch_count == 0 and cls._batch_dirty:
            cls._batch_dirty = False
            cls._do_update()

    @classmethod
    def _do_update(cls):
        """Internal — unconditionally calls root.update()."""
        if cls._root:
            cls._root.update()

    # ── Display update ─────────────────────────────────────────────

    @classmethod
    def update(cls):
        """Request a display update.  If inside a batch scope the
        update is deferred until the batch ends."""
        if cls._batch_count > 0:
            cls._batch_dirty = True
            return
        cls._do_update()

    @classmethod
    def flush(cls):
        """Force an immediate full display flush (used by Turtle).
        Ends any active batch scope."""
        cls._batch_count = 0
        cls._batch_dirty = False
        if not cls._root:
            return
        cls._root.update_idletasks()
        if sys.platform == 'win32':
            import ctypes.wintypes
            hwnd = ctypes.wintypes.HWND(cls._root.winfo_id())
            ctypes.windll.user32.UpdateWindow(hwnd)
        else:
            cls._root.update()

    # ── Drawing operations ─────────────────────────────────────────

    @classmethod
    def draw_rectangle(cls, x: int, y: int, w: int, h: int,
                       fill: str = "") -> Optional[int]:
        cls.ensure()
        if not cls._canvas:
            return None
        s = GraphicsState
        cid = cls._canvas.create_rectangle(
            x, y, x + w, y + h,
            outline=s.pen_color,
            width=s.pen_width,
            fill=fill if fill else ""
        )
        cls._register(cid, "rectangle")
        cls.update()
        return cid

    @classmethod
    def fill_rectangle(cls, x: int, y: int, w: int, h: int) -> Optional[int]:
        cls.ensure()
        if not cls._canvas:
            return None
        s = GraphicsState
        cid = cls._canvas.create_rectangle(
            x, y, x + w, y + h,
            fill=s.brush_color,
            outline=s.pen_color,
            width=s.pen_width
        )
        cls._register(cid, "rectangle")
        cls.update()
        return cid

    @classmethod
    def draw_ellipse(cls, x: int, y: int, w: int, h: int) -> Optional[int]:
        cls.ensure()
        if not cls._canvas:
            return None
        s = GraphicsState
        cid = cls._canvas.create_oval(
            x, y, x + w, y + h,
            outline=s.pen_color,
            width=s.pen_width
        )
        cls._register(cid, "ellipse")
        cls.update()
        return cid

    @classmethod
    def fill_ellipse(cls, x: int, y: int, w: int, h: int) -> Optional[int]:
        cls.ensure()
        if not cls._canvas:
            return None
        s = GraphicsState
        cid = cls._canvas.create_oval(
            x, y, x + w, y + h,
            fill=s.brush_color,
            outline=s.pen_color,
            width=s.pen_width
        )
        cls._register(cid, "ellipse")
        cls.update()
        return cid

    @classmethod
    def draw_triangle(cls, x1: int, y1: int, x2: int, y2: int,
                      x3: int, y3: int) -> Optional[int]:
        cls.ensure()
        if not cls._canvas:
            return None
        s = GraphicsState
        cid = cls._canvas.create_polygon(
            x1, y1, x2, y2, x3, y3,
            outline=s.pen_color,
            width=s.pen_width,
            fill=""
        )
        cls._register(cid, "polygon")
        cls.update()
        return cid

    @classmethod
    def fill_triangle(cls, x1: int, y1: int, x2: int, y2: int,
                      x3: int, y3: int) -> Optional[int]:
        cls.ensure()
        if not cls._canvas:
            return None
        s = GraphicsState
        cid = cls._canvas.create_polygon(
            x1, y1, x2, y2, x3, y3,
            fill=s.brush_color,
            outline=s.pen_color,
            width=s.pen_width
        )
        cls._register(cid, "polygon")
        cls.update()
        return cid

    @classmethod
    def draw_line(cls, x1: int, y1: int, x2: int, y2: int) -> Optional[int]:
        cls.ensure()
        if not cls._canvas:
            return None
        s = GraphicsState
        cid = cls._canvas.create_line(
            x1, y1, x2, y2,
            fill=s.pen_color,
            width=s.pen_width
        )
        cls._register(cid, "line")
        cls.update()
        return cid

    @classmethod
    def draw_text(cls, x: int, y: int, text: str,
                  anchor: str = "nw", width: Optional[int] = None) -> Optional[int]:
        cls.ensure()
        if not cls._canvas:
            return None
        s = GraphicsState
        weight = "bold" if s.font_bold else "normal"
        slant = "italic" if s.font_italic else "roman"
        kwargs = dict(
            text=text, anchor=anchor,
            font=(s.font_name, s.font_size, weight, slant),
            fill=s.pen_color
        )
        if width is not None:
            kwargs["width"] = width
        cid = cls._canvas.create_text(x, y, **kwargs)
        cls._register(cid, "text")
        cls.update()
        return cid

    @classmethod
    def draw_image(cls, image_name: str, x: int, y: int) -> Optional[int]:
        cls.ensure()
        if not cls._canvas:
            return None
        from smallbasic.imagelist import ImageList
        img = ImageList._tk_images.get(image_name)
        if img:
            cid = cls._canvas.create_image(x, y, image=img, anchor="nw")
            cls._register(cid, "image")
            cls.update()
            return cid
        return None

    @classmethod
    def draw_resized_image(cls, image_name: str, x: int, y: int,
                           width: int, height: int) -> Optional[int]:
        cls.ensure()
        if not cls._canvas:
            return None
        from smallbasic.imagelist import ImageList
        img = ImageList._tk_images.get(image_name)
        if img:
            resized = img.zoom(
                max(1, width // max(img.width(), 1)),
                max(1, height // max(img.height(), 1))
            )
            key = f"{image_name}_{width}x{height}"
            cls._resized_images[key] = resized
            cid = cls._canvas.create_image(x, y, image=resized, anchor="nw")
            cls._register(cid, "image")
            cls.update()
            return cid
        return None

    @classmethod
    def set_pixel(cls, x: int, y: int, color: str) -> None:
        cls.ensure()
        if cls._canvas:
            cls._canvas.create_line(x, y, x + 1, y, fill=color, width=1)
            cls.update()

    @classmethod
    def get_pixel(cls, x: int, y: int) -> str:
        cls.ensure()
        if cls._canvas:
            items = cls._canvas.find_closest(x, y)
            if items:
                cid = items[0]
                try:
                    color = cls._canvas.itemcget(cid, "fill")
                    if color and color != "":
                        return color
                except Exception:
                    pass
        return GraphicsState.bg_color

    # ── Canvas operations ──────────────────────────────────────────

    @classmethod
    def clear(cls):
        if cls._canvas:
            cls._canvas.delete("all")
            cls._objects.clear()

    @classmethod
    def delete(cls, cid: int) -> None:
        if cls._canvas:
            cls._canvas.delete(cid)
            cls._objects.pop(cid, None)

    @classmethod
    def coords(cls, cid: int, *args) -> Any:
        if cls._canvas:
            return cls._canvas.coords(cid, *args)
        return None

    @classmethod
    def itemconfig(cls, cid: int, **kwargs):
        if cls._canvas:
            cls._canvas.itemconfig(cid, **kwargs)

    @classmethod
    def find_closest(cls, x: int, y: int) -> tuple:
        if cls._canvas:
            return cls._canvas.find_closest(x, y)
        return ()

    @classmethod
    def scale(cls, cid: int, x: float, y: float, sx: float, sy: float):
        if cls._canvas:
            cls._canvas.scale(cid, x, y, sx, sy)

    @classmethod
    def get_bbox(cls, cid: int) -> Optional[tuple]:
        if cls._canvas:
            return cls._canvas.bbox(cid)
        return None

    # ── Object Registry ────────────────────────────────────────────

    @classmethod
    def _register(cls, cid: int, kind: str = "", **extra):
        if cid is not None:
            cls._objects[cid] = {"type": kind, **extra}

    @classmethod
    def get_metadata(cls, cid: int) -> dict:
        return cls._objects.get(cid, {})

    @classmethod
    def get_all_objects(cls) -> dict:
        return cls._objects

    # ── Utility ────────────────────────────────────────────────────

    @classmethod
    def get_random_color(cls) -> str:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"#{r:02X}{g:02X}{b:02X}"

    @classmethod
    def get_color_from_rgb(cls, red: int, green: int, blue: int) -> str:
        return f"#{max(0, min(255, red)):02X}" \
               f"{max(0, min(255, green)):02X}" \
               f"{max(0, min(255, blue)):02X}"
