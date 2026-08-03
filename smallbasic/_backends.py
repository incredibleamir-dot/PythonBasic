# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : tkinter graphics backend - window, canvas, drawing and control primitives.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

"""
Backend for the graphics engine.

``TkBackend`` is the single tkinter implementation of the internal
surface operations.  ``smallbasic._renderer.Renderer`` is a thin facade
that delegates to it.  The public Small Basic API (GraphicsWindow /
Turtle / Shapes / Controls) does not depend on backend internals.
"""

import sys
import time
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
    def add_button(self, caption, left, top): ...
    def add_textbox(self, left, top): ...
    def add_multi_textbox(self, left, top): ...
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
        self._shown = False
        self._dispatching = False
        # event bindings must be attached before the handlers are used
        self._bound = False

    # -- window management ------------------------------------------
    def ensure(self):
        from smallbasic._state import GraphicsState as S
        if self._root is None:
            self._root = self._tk.Tk()
            self._root.withdraw()
            self._root.protocol("WM_DELETE_WINDOW", self._on_close)
        return self._root

    def _on_close(self):
        if self._root:
            self._root.withdraw()
            self._shown = False

    def show(self):
        from smallbasic._state import GraphicsState as S
        self.ensure()
        if self._canvas is None:
            self._canvas = self._tk.Canvas(
                self._root,
                width=S.width,
                height=S.height,
                bg=S.bg_color,
                highlightthickness=0,
            )
            self._canvas.pack()
            self._bind_events()
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
        if S.MouseMove and self._root:
            self._root.after_idle(lambda: self._dispatch(S.MouseMove))

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
        return handle.zoom(
            max(1, width // max(handle.width(), 1)),
            max(1, height // max(handle.height(), 1)),
        )

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

    # -- controls ------------------------------------------------------
    def add_button(self, caption, left, top, callback=None):
        self.ensure()
        btn = self._tk.Button(self._root, text=caption,
                              relief=self._tk.RAISED, bd=2)
        if callback:
            btn.config(command=callback)
        btn.place(x=left, y=top)
        return btn

    def add_textbox(self, left, top, callback=None, multiline=False):
        self.ensure()
        if multiline:
            w = self._tk.Text(self._root, relief=self._tk.SUNKEN, bd=2,
                              height=4, width=20)
            w.place(x=left, y=top, width=200, height=80)
        else:
            w = self._tk.Entry(self._root, relief=self._tk.SUNKEN, bd=2)
            w.place(x=left, y=top, width=120, height=25)
        if callback:
            w.bind("<KeyRelease>", lambda e: callback())
        return w

    def button_caption(self, handle, value=None):
        if value is None:
            return handle.cget("text")
        handle.config(text=value)

    def textbox_text(self, handle, value=None):
        if value is None:
            if isinstance(handle, self._tk.Entry):
                return handle.get()
            return handle.get("1.0", "end-1c")
        if isinstance(handle, self._tk.Entry):
            handle.delete(0, "end")
            handle.insert(0, value)
        else:
            handle.delete("1.0", "end")
            handle.insert("1.0", value)

    def control_move(self, handle, x, y):
        handle.place(x=x, y=y)

    def control_size(self, handle, w, h):
        if isinstance(handle, self._tk.Text):
            handle.config(width=max(1, w // 10), height=max(1, h // 20))
        handle.place_configure(width=w, height=h)

    def control_visible(self, handle, visible):
        if visible:
            try:
                handle.place()
            except Exception:
                handle.place(x=0, y=0)
        else:
            handle.place_forget()

    def control_destroy(self, handle):
        handle.destroy()

    # -- extended controls -------------------------------------------
    def add_dropdown(self, items, left, top, callback=None):
        self.ensure()
        from tkinter import ttk
        combo = ttk.Combobox(self._root, values=list(items),
                             state="readonly")
        combo.place(x=left, y=top, width=140, height=25)
        if callback:
            combo.bind("<<ComboboxSelected>>", lambda e: callback())
        return combo

    def dropdown_selected(self, handle):
        return handle.get()

    def dropdown_set(self, handle, index):
        try:
            handle.current(int(index))
        except Exception:
            pass

    def dropdown_count(self, handle):
        try:
            return len(handle.cget("values"))
        except Exception:
            return 0

    def dropdown_items(self, handle):
        try:
            return list(handle.cget("values"))
        except Exception:
            return []

    def add_slider(self, minimum, maximum, left, top, callback=None):
        self.ensure()
        var = self._tk.DoubleVar(value=int(minimum))
        s = self._tk.Scale(self._root, from_=minimum, to=maximum,
                           variable=var, orient="horizontal", showvalue=True)
        s.place(x=left, y=top, width=140)
        s._sb_var = var
        if callback:
            var.trace_add("write", lambda *a: callback())
        return s

    def slider_get(self, handle):
        try:
            return int(float(handle.get()))
        except Exception:
            return 0

    def slider_set(self, handle, value):
        # use the widget-level set (like a user drag) so the SliderChanged
        # callback observes the NEW value; var.set() fires the trace before
        # the variable reflects the new value.
        handle.set(value)

    def add_progressbar(self, left, top):
        self.ensure()
        from tkinter import ttk
        p = ttk.Progressbar(self._root, maximum=100, mode="determinate")
        p.place(x=left, y=top, width=160, height=22)
        return p

    def progress_get(self, handle):
        try:
            return int(handle["value"])
        except Exception:
            return 0

    def progress_set(self, handle, value):
        handle["value"] = max(0, min(100, int(value)))

    def _populate_table(self, tree, data):
        for item in tree.get_children():
            tree.delete(item)
        rows = [list(r) for r in data]
        if not rows:
            return
        headers = [str(c) for c in rows[0]]
        tree.configure(columns=headers)
        for h in headers:
            tree.heading(h, text=h)
            tree.column(h, width=100, anchor="w")
        for row in rows[1:]:
            tree.insert("", "end", values=[str(c) for c in row])

    def add_table(self, data, left, top, callback=None):
        self.ensure()
        from tkinter import ttk
        rows = [list(r) for r in data]
        headers = [str(c) for c in rows[0]] if rows else []
        tree = ttk.Treeview(self._root, columns=headers, show="headings")
        tree.column("#0", width=0, stretch=False)
        self._populate_table(tree, data)
        tree.place(x=left, y=top, width=620, height=220)
        if callback:
            tree.bind("<<TreeviewSelect>>", lambda e: callback())
        return tree

    def table_set_data(self, handle, data):
        self._populate_table(handle, data)

    def table_selected_row(self, handle):
        try:
            sel = handle.selection()
            if sel:
                return int(handle.index(sel[0])) + 1
        except Exception:
            pass
        return 0

    # -- misc ----------------------------------------------------------
    def show_message(self, title, text):
        self.ensure()
        self._tk.messagebox.showinfo(title, text)


def create_backend() -> TkBackend:
    """Instantiate the tkinter backend."""
    return TkBackend()
