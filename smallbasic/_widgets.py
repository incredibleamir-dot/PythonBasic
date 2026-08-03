# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : tkinter widget helpers - buttons, text boxes and extended widgets.
# Version : 1.7.0
# --------------------------------------------------------------------------

"""
Internal widget factory used by ``smallbasic._backends.TkBackend``.

Keeping all control-construction code in one place lets the backend focus on
the window / canvas surface while this module owns the widgets that are placed
on top of it.  ``TkWidgets`` holds a reference to its backend so it can read
the root window handle (``backend._root``) after ``backend.ensure()`` has run.
"""

class TkWidgets:
    """Builds and manipulates tkinter widgets on the graphics window."""

    def __init__(self, backend):
        self._backend = backend

    # -- backend accessors -------------------------------------------
    @property
    def _tk(self):
        return self._backend._tk

    @property
    def _root(self):
        return self._backend._root

    # -- basic widgets -----------------------------------------------
    def add_button(self, caption, left, top, callback=None):
        self._backend.ensure()
        btn = self._tk.Button(self._root, text=caption,
                              relief=self._tk.RAISED, bd=2)
        if callback:
            btn.config(command=callback)
        btn.place(x=left, y=top)
        return btn

    def add_textbox(self, left, top, callback=None, multiline=False):
        self._backend.ensure()
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

    # -- extended widgets -------------------------------------------
    def add_dropdown(self, items, left, top, callback=None):
        self._backend.ensure()
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
        self._backend.ensure()
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
        self._backend.ensure()
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
        self._backend.ensure()
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

    # -- misc -------------------------------------------------------
    def show_message(self, title, text):
        self._backend.ensure()
        self._tk.messagebox.showinfo(title, text)