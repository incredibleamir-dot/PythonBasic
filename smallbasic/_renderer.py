# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Renderer facade - batching, display updates and all high-level drawing operations.
# Version : 1.7.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

"""
Internal Renderer — facade over the active graphics backend.

The Renderer owns the batch/update machinery and the drawing
high-level operations.  All backend-specific window and canvas
interaction is delegated to the tkinter backend
(see ``smallbasic._backends``).

No other module should call backend/Canvas methods directly; use the
Renderer methods (including ``create_*``/``coords``/``itemconfig``).
"""

import random
import time
from typing import Optional, Any
from smallbasic._state import GraphicsState
from smallbasic._backends import create_backend, Backend


class Renderer:
    """Singleton-style renderer facade that owns the graphics window."""

    _backend: Optional[Backend] = None
    _root: Any = None
    _canvas: Any = None
    _resized_images: dict = {}
    _pixels: dict = {}
    # Image placements in canvas coordinates: (name, x, y, w, h).  Kept so
    # GetPixel can read the colour of a drawn image from its PIL source.
    _image_placements: list = []
    _shown: bool = False
    _batch_count: int = 0
    _batch_dirty: bool = False

    # ── Backend selection ────────────────────────────────────────

    @classmethod
    def backend(cls) -> Backend:
        if cls._backend is None:
            cls._backend = create_backend()
            cls._backend.ensure()
            cls._sync_handles()
        return cls._backend

    @classmethod
    def reset_backend(cls) -> None:
        """Forget the active backend (used by tests)."""
        cls._backend = None
        cls._root = None
        cls._canvas = None
        cls._shown = False
        cls._pixels.clear()
        cls._resized_images.clear()
        cls._image_placements.clear()

    @classmethod
    def _sync_handles(cls) -> None:
        """Mirror backend window/canvas handles for backward compat."""
        b = cls._backend
        if b is not None:
            cls._root = getattr(b, "_root", None) or getattr(b, "_window", None)
            cls._canvas = getattr(b, "_canvas", None)

    # ── Window management ──────────────────────────────────────────

    @classmethod
    def ensure(cls) -> Any:
        return cls.backend() or getattr(cls, "_root", None)

    @classmethod
    def _on_close(cls):
        if cls._backend:
            cls._backend._on_close()
            cls._sync_handles()

    @classmethod
    def show(cls):
        cls.backend().show()
        cls._sync_handles()
        cls._shown = True

    @classmethod
    def hide(cls):
        if cls._backend:
            cls._backend.hide()
            cls._shown = False

    @classmethod
    def wait_for_close(cls):
        if cls._backend:
            cls._backend.wait_for_close()

    @classmethod
    def destroy(cls):
        if cls._backend:
            cls._backend.destroy()
        cls._root = None
        cls._canvas = None
        cls._pixels.clear()
        cls._resized_images.clear()
        cls._image_placements.clear()
        cls._shown = False

    # ── Batch support ──────────────────────────────────────────────

    @classmethod
    def begin_batch(cls):
        cls._batch_count += 1

    @classmethod
    def end_batch(cls):
        if cls._batch_count > 0:
            cls._batch_count -= 1
        if cls._batch_count == 0 and cls._batch_dirty:
            cls._batch_dirty = False
            cls._do_update()

    @classmethod
    def _do_update(cls):
        if cls._backend:
            cls._backend.update()

    # ── Display update ─────────────────────────────────────────────

    @classmethod
    def update(cls):
        if cls._batch_count > 0:
            cls._batch_dirty = True
            return
        cls._do_update()

    @classmethod
    def flush(cls):
        cls._batch_count = 0
        cls._batch_dirty = False
        if cls._backend:
            cls._backend.flush()

    # ── Drawing operations ─────────────────────────────────────────

    @classmethod
    def _style(cls):
        s = GraphicsState
        return {
            "outline": s.pen_color,
            "width": s.pen_width,
            "fill": s.brush_color,
        }

    @classmethod
    def draw_rectangle(cls, x: int, y: int, w: int, h: int) -> Optional[int]:
        s = GraphicsState
        cid = cls.backend().create_rectangle(
            x, y, w, h, outline=s.pen_color, width=s.pen_width, fill="")
        cls.update()
        return cid

    @classmethod
    def fill_rectangle(cls, x: int, y: int, w: int, h: int) -> Optional[int]:
        cid = cls.backend().create_rectangle(x, y, w, h, **cls._style())
        cls.update()
        return cid

    @classmethod
    def draw_ellipse(cls, x: int, y: int, w: int, h: int) -> Optional[int]:
        s = GraphicsState
        cid = cls.backend().create_oval(x, y, w, h, outline=s.pen_color,
                                        width=s.pen_width, fill="")
        cls.update()
        return cid

    @classmethod
    def fill_ellipse(cls, x: int, y: int, w: int, h: int) -> Optional[int]:
        cid = cls.backend().create_oval(x, y, w, h, **cls._style())
        cls.update()
        return cid

    @classmethod
    def draw_triangle(cls, x1: int, y1: int, x2: int, y2: int,
                      x3: int, y3: int) -> Optional[int]:
        s = GraphicsState
        cid = cls.backend().create_polygon(
            (x1, y1, x2, y2, x3, y3), outline=s.pen_color,
            width=s.pen_width, fill="")
        cls.update()
        return cid

    @classmethod
    def fill_triangle(cls, x1: int, y1: int, x2: int, y2: int,
                      x3: int, y3: int) -> Optional[int]:
        cid = cls.backend().create_polygon(
            (x1, y1, x2, y2, x3, y3), **cls._style())
        cls.update()
        return cid

    @classmethod
    def draw_line(cls, x1: int, y1: int, x2: int, y2: int) -> Optional[int]:
        s = GraphicsState
        cid = cls.backend().create_line(
            (x1, y1, x2, y2), fill=s.pen_color, width=s.pen_width)
        cls.update()
        return cid

    @classmethod
    def draw_text(cls, x: int, y: int, text: str,
                  anchor: str = "nw", width: Optional[int] = None) -> Optional[int]:
        s = GraphicsState
        weight = "bold" if s.font_bold else "normal"
        slant = "italic" if s.font_italic else "roman"
        font = (s.font_name, s.font_size, weight, slant)
        cid = cls.backend().create_text(
            x, y, text, anchor=anchor, font=font, fill=s.pen_color, width=width)
        cls.update()
        return cid

    @classmethod
    def draw_image(cls, image_name: str, x: int, y: int) -> Optional[int]:
        from smallbasic.imagelist import ImageList
        img = ImageList._backend_images.get(image_name)
        if img is None:
            return None
        cls._image_placements.append(
            (image_name, int(x), int(y),
             ImageList.GetWidthOfImage(image_name),
             ImageList.GetHeightOfImage(image_name)))
        cid = cls.backend().create_image(x, y, img, anchor="nw")
        cls.update()
        return cid

    @classmethod
    def draw_resized_image(cls, image_name: str, x: int, y: int,
                           width: int, height: int) -> Optional[int]:
        from smallbasic.imagelist import ImageList
        img = ImageList._backend_images.get(image_name)
        if img is None:
            return None
        resized = ImageList._resize(image_name, img, width, height)
        if resized is None:
            return None
        key = f"{image_name}_{width}x{height}"
        cls._resized_images[key] = resized
        cls._image_placements.append(
            (image_name, int(x), int(y), int(width), int(height)))
        cid = cls.backend().create_image(x, y, resized, anchor="nw")
        cls.update()
        return cid

    @classmethod
    def set_pixel(cls, x: int, y: int, color: str) -> None:
        cls._pixels[(int(x), int(y))] = color
        cls.backend().create_pixel(x, y, color)
        cls.update()

    @classmethod
    def get_pixel(cls, x: int, y: int) -> str:
        color = cls._pixels.get((int(x), int(y)))
        if color is not None:
            return color
        # Reading a drawn image: locate the top-most placement covering the
        # point and sample its PIL source (scaled for resized images).
        from smallbasic.imagelist import ImageList
        for name, ix, iy, iw, ih in reversed(cls._image_placements):
            if iw and ih and ix <= int(x) < ix + iw and iy <= int(y) < iy + ih:
                src = ImageList._images.get(name)
                if src is not None:
                    try:
                        sx = max(0, min(src.width - 1,
                                        int((x - ix) / iw * src.width)))
                        sy = max(0, min(src.height - 1,
                                        int((y - iy) / ih * src.height)))
                        pixel = src.getpixel((sx, sy))
                        if isinstance(pixel, (tuple, list)):
                            r, g, b = pixel[0], pixel[1], pixel[2]
                        else:
                            r = g = b = int(pixel)
                        return f"#{r:02X}{g:02X}{b:02X}"
                    except Exception:
                        pass
                break
        return cls.backend().get_pixel(x, y)

    # ── Canvas operations (used by Shapes / Turtle) ────────────────

    @classmethod
    def clear(cls):
        if cls._backend:
            cls._backend.clear()
        cls._pixels.clear()
        cls._resized_images.clear()
        cls._image_placements.clear()

    @classmethod
    def delete(cls, cid: int) -> None:
        if cls._backend:
            cls._backend.delete(cid)

    @classmethod
    def coords(cls, cid: int, *args) -> Any:
        return cls.backend().coords(cid, *args)

    @classmethod
    def itemconfig(cls, cid: int, **kwargs):
        cls.backend().itemconfig(cid, **kwargs)

    @classmethod
    def itemcget(cls, cid: int, option: str) -> str:
        return cls.backend().itemcget(cid, option)

    @classmethod
    def find_closest(cls, x: int, y: int) -> tuple:
        return cls.backend().find_closest(x, y)

    @classmethod
    def scale(cls, cid: int, x: float, y: float, sx: float, sy: float):
        cls.backend().scale(cid, x, y, sx, sy)

    @classmethod
    def get_bbox(cls, cid: int) -> Optional[tuple]:
        return cls.backend().bbox(cid)

    # Low-level item creation used by Shapes / Turtle.
    @classmethod
    def create_oval(cls, x0, y0, x1, y1, fill="Red", outline="Black", width=2):
        return cls.backend().create_oval(x0, y0, x1 - x0, y1 - y0,
                                         outline=outline, width=width, fill=fill)

    @classmethod
    def create_polygon(cls, points, outline="", width=0, fill=""):
        return cls.backend().create_polygon(tuple(points), outline=outline,
                                            width=width, fill=fill)

    @classmethod
    def create_line(cls, x1, y1, x2, y2, fill="Black", width=2):
        return cls.backend().create_line((x1, y1, x2, y2), fill=fill,
                                         width=width)

    @classmethod
    def create_text(cls, x, y, text, anchor="nw", font=None, fill="",
                    width=None):
        return cls.backend().create_text(x, y, text, anchor=anchor, font=font,
                                         fill=fill, width=width)

    @classmethod
    def create_image(cls, x, y, image, anchor="nw"):
        return cls.backend().create_image(x, y, image, anchor=anchor)

    @classmethod
    def pump_wait(cls, delay_ms: int) -> None:
        """Block for ``delay_ms`` while keeping the event loop alive.

        Replaces bare ``time.sleep`` in animation loops: pumps Tcl
        events during the wait (so a window drag keeps the animation
        advancing).  Preserves blocking semantics and total duration.
        Stops pumping early if the window has been destroyed.
        """
        if cls._backend is None or not getattr(cls._backend, "_root", None):
            time.sleep(delay_ms / 1000.0)
            return
        end = time.time() + delay_ms / 1000.0
        while time.time() < end:
            try:
                cls._backend.update()
            except Exception:
                break  # window was closed -> stop pumping
            time.sleep(0.005)

    # ── Utility ────────────────────────────────────────────────────

    @classmethod
    def get_random_color(cls) -> str:
        return f"#{random.randint(0, 255):02X}" \
               f"{random.randint(0, 255):02X}" \
               f"{random.randint(0, 255):02X}"

    @classmethod
    def get_color_from_rgb(cls, red: int, green: int, blue: int) -> str:
        return f"#{max(0, min(255, red)):02X}" \
               f"{max(0, min(255, green)):02X}" \
               f"{max(0, min(255, blue)):02X}"
