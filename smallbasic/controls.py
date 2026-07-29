import tkinter as tk
from typing import Optional
from smallbasic._utils import classproperty


class Controls:
    """
    The Controls object allows you to add, move and interact with controls
    (buttons, text boxes) on the Graphics Window.
    
    Usage:
        btn = Controls.AddButton("Click Me", 100, 50)
        Controls.ButtonClicked = lambda: TextWindow.WriteLine("Clicked!")
        tb = Controls.AddTextBox(100, 100)
        text = Controls.GetTextBoxText(tb)
    """

    _widgets: dict = {}
    _counter: int = 0
    _last_clicked_button: str = ""
    _last_typed_textbox: str = ""

    ButtonClicked = None
    TextTyped = None

    @classmethod
    def _get_parent(cls):
        """Get the tkinter parent window, importing here to avoid circular import."""
        from smallbasic.graphics_window import _TkWindow
        _TkWindow.ensure()
        return _TkWindow._root

    @classproperty
    def LastClickedButton(cls) -> str:
        """Gets the name of the last button that was clicked."""
        return cls._last_clicked_button

    @classproperty
    def LastTypedTextBox(cls) -> str:
        """Gets the name of the last TextBox text was typed into."""
        return cls._last_typed_textbox

    @classmethod
    def AddButton(cls, caption: str, left: int, top: int) -> str:
        """
        Adds a button to the graphics window at the specified position.
        
        Args:
            caption: The caption to display on the button.
            left: The x co-ordinate of the button.
            top: The y co-ordinate of the button.
            
        Returns:
            The name of the button that was added.
        """
        parent = cls._get_parent()
        cls._counter += 1
        name = f"Button{cls._counter}"

        btn = tk.Button(parent, text=caption, relief=tk.RAISED, bd=2)

        def on_click(event=None):
            cls._last_clicked_button = name
            if cls.ButtonClicked:
                cls.ButtonClicked()

        btn.config(command=on_click)
        btn.place(x=left, y=top)
        cls._widgets[name] = btn
        return name

    @classmethod
    def GetButtonCaption(cls, button_name: str) -> str:
        """
        Gets the current caption of the specified button.
        
        Args:
            button_name: The button whose caption is requested.
            
        Returns:
            The current caption of the button.
        """
        btn = cls._widgets.get(button_name)
        if btn and isinstance(btn, tk.Button):
            return btn.cget("text")
        return ""

    @classmethod
    def SetButtonCaption(cls, button_name: str, caption: str) -> None:
        """
        Sets the caption of the specified button.
        
        Args:
            button_name: The button whose caption needs to be set.
            caption: The new caption for the button.
        """
        btn = cls._widgets.get(button_name)
        if btn and isinstance(btn, tk.Button):
            btn.config(text=caption)

    @classmethod
    def AddTextBox(cls, left: int, top: int) -> str:
        """
        Adds a text input box to the graphics window.
        
        Args:
            left: The x co-ordinate of the text box.
            top: The y co-ordinate of the text box.
            
        Returns:
            The name of the text box that was added.
        """
        parent = cls._get_parent()
        cls._counter += 1
        name = f"TextBox{cls._counter}"

        entry = tk.Entry(parent, relief=tk.SUNKEN, bd=2)

        def on_keyrelease(event):
            cls._last_typed_textbox = name
            if cls.TextTyped:
                cls.TextTyped()

        entry.bind("<KeyRelease>", on_keyrelease)
        entry.place(x=left, y=top, width=120, height=25)
        cls._widgets[name] = entry
        return name

    @classmethod
    def AddMultiLineTextBox(cls, left: int, top: int) -> str:
        """
        Adds a multi-line text input box to the graphics window.
        
        Args:
            left: The x co-ordinate of the text box.
            top: The y co-ordinate of the text box.
            
        Returns:
            The name of the text box that was added.
        """
        parent = cls._get_parent()
        cls._counter += 1
        name = f"TextBox{cls._counter}"

        text_widget = tk.Text(parent, relief=tk.SUNKEN, bd=2, height=4, width=20)

        def on_keyrelease(event):
            cls._last_typed_textbox = name
            if cls.TextTyped:
                cls.TextTyped()

        text_widget.bind("<KeyRelease>", on_keyrelease)
        text_widget.place(x=left, y=top, width=200, height=80)
        cls._widgets[name] = text_widget
        return name

    @classmethod
    def AddMultiLineText(cls, left: int, top: int) -> str:
        """
        Alias for AddMultiLineTextBox.
        
        Args:
            left: The x co-ordinate of the text box.
            top: The y co-ordinate of the text box.
            
        Returns:
            The name of the text box that was added.
        """
        return cls.AddMultiLineTextBox(left, top)

    @classmethod
    def GetTextBoxText(cls, textbox_name: str) -> str:
        """
        Gets the current text of the specified TextBox.
        
        Args:
            textbox_name: The TextBox whose text is requested.
            
        Returns:
            The text in the TextBox.
        """
        widget = cls._widgets.get(textbox_name)
        if not widget:
            return ""
        if isinstance(widget, tk.Entry):
            return widget.get()
        elif isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c")
        return ""

    @classmethod
    def SetTextBoxText(cls, textbox_name: str, text: str) -> None:
        """
        Sets the text of the specified TextBox.
        
        Args:
            textbox_name: The TextBox whose text needs to be set.
            text: The new text for the TextBox.
        """
        widget = cls._widgets.get(textbox_name)
        if not widget:
            return
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
            widget.insert(0, text)
        elif isinstance(widget, tk.Text):
            widget.delete("1.0", tk.END)
            widget.insert("1.0", text)

    @classmethod
    def Remove(cls, control_name: str) -> None:
        """
        Removes a control from the Graphics Window.
        
        Args:
            control_name: The name of the control to remove.
        """
        widget = cls._widgets.pop(control_name, None)
        if widget:
            widget.destroy()

    @classmethod
    def Move(cls, control: str, x: int, y: int) -> None:
        """
        Moves the control to a new position.
        
        Args:
            control: The name of the control to move.
            x: The x co-ordinate of the new position.
            y: The y co-ordinate of the new position.
        """
        widget = cls._widgets.get(control)
        if widget:
            widget.place(x=x, y=y)

    @classmethod
    def SetSize(cls, control: str, width: int, height: int) -> None:
        """
        Sets the size of the control.
        
        Args:
            control: The name of the control to resize.
            width: The width of the control.
            height: The height of the control.
        """
        widget = cls._widgets.get(control)
        if widget:
            if isinstance(widget, tk.Text):
                widget.config(width=max(1, width // 10), height=max(1, height // 20))
            widget.place_configure(width=width, height=height)

    @classmethod
    def HideControl(cls, control_name: str) -> None:
        """
        Hides an already added control.
        
        Args:
            control_name: The name of the control.
        """
        widget = cls._widgets.get(control_name)
        if widget:
            widget.place_forget()

    @classmethod
    def ShowControl(cls, control_name: str) -> None:
        """
        Shows a previously hidden control.
        
        Args:
            control_name: The name of the control.
        """
        widget = cls._widgets.get(control_name)
        if widget:
            try:
                widget.place()
            except Exception:
                widget.place(x=0, y=0)
