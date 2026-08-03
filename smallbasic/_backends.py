# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : tkinter graphics backend - window, canvas, drawing and control primitives.
# Version : 1.7.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

"""
Backend for the graphics engine.

``TkBackend`` is the single tkinter implementation of the internal
surface operations.  ``smallbasic._renderer.Renderer`` is a thin facade
that delegates to it.  The public Small Basic API (GraphicsWindow /
Turtle / Shapes / Controls) does not depend on backend internals.

Widget construction lives in ``smallbasic._widgets.TkWidgets``; the
backend only manages the window/canvas surface and drawing primitives.
"""

import sys
from typing import Optional, Any


class Backend:
    """Common interface implemented by the renderer backend."""

    name = "abstract"

    # ── Window lifecycle ─────────────────────────────────────────
    def ensure(self) -> Any: ...
    def show(self) -> None: ...
    def hide(self) -> None: ...
    def destroy(self) -> None: ...
    def wait_for_close(self) -> None: ...
    def update(self) -> None: ...
    def flush(self) -> None: ...

    # ── Live property application ────────────────────────────────
    def set_bg(self, color: str) -> None: ...
    def set_title(self, title: str) -> None: ...
    def set_geometry(self, w: int, h: int, l: int, t: int) -> None: ...
    def set_resizable(self, flag: bool) -> None: ...

    # ── Drawing primitives (return a canvas-item id) ─────────────
    def create_rectangle(self, x, y, w, h, outline="", width=0, fill=""): ...
    def create_oval(self, x, y, w, h, outline="", width=0, fill=""): ...
    def create_polygon(self, points, outline="", width=0, fill=""): ...
    def create_line(self, points, fill="", width=0): ...
    def create_text(self, x, y, text, anchor="nw", font=None, fill="",
                    width=None): ...
    def create_image(self, x, y, image, anchor="nw"): ...
    def create_pixel(self, x, y, color): ...
    def clear(self) -> None: ...

    # ── Images ─────────────────────────────────────────────────────
    def load_image(self, pil_image): ...
    def resize_image(self, handle, width, height): ...

    # ── Canvas item operations ───────────────────────────────────
    def coords(self, cid, *args): ...
    def itemconfig(self, cid, **kwargs): ...
    def itemcget(self, cid, option): ...
    def delete(self, cid) -> None: ...
    def scale(self, cid, x, y, sx, sy) -> None: ...
    def find_closest(self, x, y): ...
    def bbox(self, cid): ...
    def get_pixel(self, x, y) -> str: ...

    # ── Controls ─────────────────────────────────────────────────
    def add_button(self, caption, left, top, callback=None): ...
    def add_textbox(self, left, top, callback=None, multiline=False): ...
    def button_caption(self, handle, value=None): ...
    def textbox_text(self, handle, value=None): ...
    def control_move(self, handle, x, y): ...
    def control_size(self, handle, w, h): ...
    def control_visible(self, handle, visible): ...
    def control_destroy(self, handle): ...

    # ── Extended controls ────────────────────────────────────────
    def add_dropdown(self, items, left, top, callback=None): ...
    def dropdown_selected(self, handle): ...
    def dropdown_set(self, handle, index): ...
    def dropdown_count(self, handle): ...
    def dropdown_items(self, handle): ...
    def add_slider(self, minimum, maximum, left, top, callback=None): ...
    def slider_get(self, handle): ...
    def slider_set(self, handle, value): ...
    def add_progressbar(self, left, top): ...
    def progress_get(self, handle): ...
    def progress_set(self, handle, value): ...
    def add_table(self, data, left, top, callback=None): ...
    def table_set_data(self, handle, data): ...
    def table_selected_row(self, handle): ...

    # ── Misc ─────────────────────────────────────────────────────
    def show_message(self, title, text) -> None: ...


# ── Tkinter backend ────────────────────────────────────────────────

class TkBackend(Backend):
    """Original tkinter implementation, extracted from the Renderer."""

    name = "TKINTER"

    def __init__(self):
        import tkinter as tk
        self._tk = tk
        self._root: Optional[tk.Tk] = None
        self._canvas: Optional[tk.Canvas] = None
        self._widgets = None
        self._shown = False
        self._dispatching = False
        # event bindings must be attached before the handlers are used
        self._bound = False
        # coalesce rapid <Motion> events so the idle queue is not flooded
        self._motion_pending = False

    # -- window management ------------------------------------------
    def ensure(self):
        from smallbasic._state import GraphicsState as S
        if self._root is None:
            self._root = self._tk.Tk()
            self._root.withdraw()
            self._root.protocol("WM_DELETE_WINDOW", self._on_close)
        if self._canvas is None:
            # Create the canvas eagerly so drawing before Show() works.
            self._canvas = self._tk.Canvas(
                self._root,
                width=S.width,
                height=S.height,
                bg=S.bg_color,
                highlightthickness=0,
            )
            self._canvas.pack()
            self._bind_events()
        return self._root

    def _on_close(self):
        if self._root:
            self._root.withdraw()
            self._shown = False

    def show(self):
        from smallbasic._state import GraphicsState as S
        self.ensure()
        if not self._shown:
            self._root.deiconify()
            self._root.title(S.title)
            self._root.geometry(f"{S.width}x{S.height}+{S.left}+{S.top}")
            self._root.resizable(S.can_resize, S.can_resize)
            self.update()
            self._shown = True

    def hide(self):
        if self._root:
            self._root.withdraw()
            self._shown = False

    def destroy(self):
        if self._root:
            try:
                self._root.destroy()
            except Exception:
                pass
        self._root = None
        self._canvas = None
        self._widgets = None

    def wait_for_close(self):
        if self._root:
            self._root.mainloop()

    # -- events ------------------------------------------------------
    def _bind_events(self):
        from smallbasic._state import GraphicsState as S
        self._canvas.bind("<Key>", self._on_key)
        self._canvas.bind("<KeyRelease>", self._on_key_up)
        for b in ("1", "2", "3"):
            self._canvas.bind(f"<Button-{b}>", self._on_mouse_down)
            self._canvas.bind(f"<ButtonRelease-{b}>", self._on_mouse_up)
        self._canvas.bind("<Motion>", self._on_mouse_move)
        self._canvas.focus_set()
        self._bound = True

    def _dispatch(self, cb):
        """Run a user event handler without passing the tk event object.

        Small Basic event handlers take no arguments.  Passing the tk
        event used to raise TypeError on every click, which is the
        reported 'clicking the canvas crashes it' bug.
        """
        if cb is None or self._root is None:
            return
        self._dispatching = True
        try:
            cb()
        finally:
            self._dispatching = False

    def _on_key(self, event):
        from smallbasic._state import GraphicsState as S
        S.last_key = event.keysym
        S.last_text = event.char
        if self._root:
            self._root.after_idle(lambda: self._dispatch(S.KeyDown))
            self._root.after_idle(lambda: self._dispatch(S.TextInput))

    def _on_key_up(self, event):
        from smallbasic._state import GraphicsState as S
        S.last_key = event.keysym
        if S.KeyUp and self._root:
            self._root.after_idle(lambda: self._dispatch(S.KeyUp))

    def _on_mouse_down(self, event):
        from smallbasic._state import GraphicsState as S
        S.mouse_x = event.x
        S.mouse_y = event.y
        if S.MouseDown and self._root:
            self._root.after_idle(lambda: self._dispatch(S.MouseDown))

    def _on_mouse_up(self, event):
        from smallbasic._state import GraphicsState as S
        S.mouse_x = event.x
        S.mouse_y = event.y
        if S.MouseUp and self._root:
            self._root.after_idle(lambda: self._dispatch(S.MouseUp))

    def _on_mouse_move(self, event):
        from smallbasic._state import GraphicsState as S
        S.mouse_x = event.x
        S.mouse_y = event.y
        if S.MouseMove and self._root and not self._motion_pending:
            self._motion_pending = True
            self._root.after_idle(self._dispatch_motion)

    def _dispatch_motion(self):
        from smallbasic._state import GraphicsState as S
        self._motion_pending = False
        self._dispatch(S.MouseMove)

    # -- display update ----------------------------------------------
    def update(self):
        if self._dispatching and self._root:
            # never call update() from inside an event callback
            self._root.after_idle(lambda: self._root.update())
            return
        if self._root:
            self._root.update()

    def flush(self):
        if not self._root:
            return
        if self._dispatching:
            self._root.after_idle(lambda: self._root.update())
            return
        try:
            self._root.update_idletasks()
            if sys.platform == "win32":
                import ctypes.wintypes
                hwnd = ctypes.wintypes.HWND(self._root.winfo_id())
                ctypes.windll.user32.UpdateWindow(hwnd)
            else:
                self._root.update()
        except Exception:
            pass

    # -- live property application ------------------------------------
    def set_bg(self, color):
        if self._canvas:
            self._canvas.config(bg=color)

    def set_title(self, title):
        if self._root:
            self._root.title(title)

    def set_geometry(self, w, h, l, t):
        if self._root:
            self._root.geometry(f"{w}x{h}+{l}+{t}")

    def set_resizable(self, flag):
        if self._root:
            self._root.resizable(flag, flag)

    # -- drawing primitives ------------------------------------------
    def create_rectangle(self, x, y, w, h, outline="", width=0, fill=""):
        self.ensure()
        if not self._canvas:
            return None
        return self._canvas.create_rectangle(
            x, y, x + w, y + h, outline=outline, width=width,
            fill=fill if fill else "")

    def create_oval(self, x, y, w, h, outline="", width=0, fill=""):
        self.ensure()
        if not self._canvas:
            return None
        if fill:
            return self._canvas.create_oval(
                x, y, x + w, y + h, fill=fill, outline=outline, width=width)
        return self._canvas.create_oval(
            x, y, x + w, y + h, outline=outline, width=width)

    def create_polygon(self, points, outline="", width=0, fill=""):
        self.ensure()
        if not self._canvas:
            return None
        return self._canvas.create_polygon(
            *points, outline=outline, width=width, fill=fill if fill else "")

    def create_line(self, points, fill="", width=0):
        self.ensure()
        if not self._canvas:
            return None
        return self._canvas.create_line(*points, fill=fill, width=width)

    def create_text(self, x, y, text, anchor="nw", font=None, fill="",
                    width=None):
        self.ensure()
        if not self._canvas:
            return None
        if font is None:
            font = ("Consolas", 12)
        kw = dict(text=text, anchor=anchor, font=font, fill=fill)
        if width is not None:
            kw["width"] = width
        return self._canvas.create_text(x, y, **kw)

    def create_image(self, x, y, image, anchor="nw"):
        self.ensure()
        if not self._canvas:
            return None
        return self._canvas.create_image(x, y, image=image, anchor=anchor)

    def create_pixel(self, x, y, color):
        self.ensure()
        if self._canvas:
            self._canvas.create_line(x, y, x + 1, y, fill=color, width=1)

    # -- images -------------------------------------------------------
    def load_image(self, pil_image):
        from PIL import ImageTk
        return ImageTk.PhotoImage(pil_image)

    def resize_image(self, handle, width, height):
        src_w = max(handle.width(), 1)
        src_h = max(handle.height(), 1)
        tw = max(1, int(width))
        th = max(1, int(height))
        if tw <= src_w and th <= src_h:
            # shrink: downsample by an integer factor via subsample
            return handle.subsample(max(1, src_w // tw), max(1, src_h // th))
        # grow: upscale by an integer factor via zoom
        return handle.zoom(max(1, tw // src_w), max(1, th // src_h))

    def clear(self):
        if self._canvas:
            self._canvas.delete("all")

    # -- item operations ----------------------------------------------
    def coords(self, cid, *args):
        if self._canvas:
            return self._canvas.coords(cid, *args)
        return None

    def itemconfig(self, cid, **kwargs):
        if self._canvas:
            self._canvas.itemconfig(cid, **kwargs)

    def itemcget(self, cid, option):
        if self._canvas:
            return self._canvas.itemcget(cid, option)
        return ""

    def delete(self, cid):
        if self._canvas:
            self._canvas.delete(cid)

    def scale(self, cid, x, y, sx, sy):
        if self._canvas:
            self._canvas.scale(cid, x, y, sx, sy)

    def find_closest(self, x, y):
        if self._canvas:
            return self._canvas.find_closest(x, y)
        return ()

    def bbox(self, cid):
        if self._canvas:
            return self._canvas.bbox(cid)
        return None

    def get_pixel(self, x, y):
        from smallbasic._state import GraphicsState as S
        self.ensure()
        if self._canvas:
            items = self._canvas.find_closest(x, y)
            if items:
                cid = items[0]
                try:
                    color = self._canvas.itemcget(cid, "fill")
                    if color and color != "":
                        return color
                except Exception:
                    pass
        return S.bg_color

    # -- controls (delegated to TkWidgets) ----------------------------
    def _widget_helpers(self):
        if self._widgets is None:
            from smallbasic._widgets import TkWidgets
            self._widgets = TkWidgets(self)
        return self._widgets

    def add_button(self, caption, left, top, callback=None):
        self.ensure()
        return self._widget_helpers().add_button(caption, left, top, callback=callback)

    def add_textbox(self, left, top, callback=None, multiline=False):
        self.ensure()
        return self._widget_helpers().add_textbox(left, top, callback=callback,
                                           multiline=multiline)

    def button_caption(self, handle, value=None):
        return self._widget_helpers().button_caption(handle, value)

    def textbox_text(self, handle, value=None):
        return self._widget_helpers().textbox_text(handle, value)

    def control_move(self, handle, x, y):
        self._widget_helpers().control_move(handle, x, y)

    def control_size(self, handle, w, h):
        self._widget_helpers().control_size(handle, w, h)

    def control_visible(self, handle, visible):
        self._widget_helpers().control_visible(handle, visible)

    def control_destroy(self, handle):
        self._widget_helpers().control_destroy(handle)

    def add_dropdown(self, items, left, top, callback=None):
        self.ensure()
        return self._widget_helpers().add_dropdown(items, left, top, callback=callback)

    def dropdown_selected(self, handle):
        return self._widget_helpers().dropdown_selected(handle)

    def dropdown_set(self, handle, index):
        self._widget_helpers().dropdown_set(handle, index)

    def dropdown_count(self, handle):
        return self._widget_helpers().dropdown_count(handle)

    def dropdown_items(self, handle):
        return self._widget_helpers().dropdown_items(handle)

    def add_slider(self, minimum, maximum, left, top, callback=None):
        self.ensure()
        return self._widget_helpers().add_slider(minimum, maximum, left, top,
                                          callback=callback)

    def slider_get(self, handle):
        return self._widget_helpers().slider_get(handle)

    def slider_set(self, handle, value):
        self._widget_helpers().slider_set(handle, value)

    def add_progressbar(self, left, top):
        self.ensure()
        return self._widget_helpers().add_progressbar(left, top)

    def progress_get(self, handle):
        return self._widget_helpers().progress_get(handle)

    def progress_set(self, handle, value):
        self._widget_helpers().progress_set(handle, value)

    def add_table(self, data, left, top, callback=None):
        self.ensure()
        return self._widget_helpers().add_table(data, left, top, callback=callback)

    def table_set_data(self, handle, data):
        self._widget_helpers().table_set_data(handle, data)

    def table_selected_row(self, handle):
        return self._widget_helpers().table_selected_row(handle)

    def show_message(self, title, text):
        self.ensure()
        self._widget_helpers().show_message(title, text)


def create_backend() -> TkBackend:
    """Instantiate the tkinter backend."""
    return TkBackend()
