# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Controls object - buttons, text boxes and extended widgets on the graphics window.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

from typing import Optional
from smallbasic._utils import classproperty
from smallbasic._renderer import Renderer


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
    _types: dict = {}   # name -> "button" | "textbox" | "multitext"
    _counter: int = 0
    _last_clicked_button: str = ""
    _last_typed_textbox: str = ""
    _last_changed_slider: str = ""
    _last_selected_dropdown: str = ""
    _last_selected_table: str = ""

    ButtonClicked = None
    TextTyped = None
    SliderChanged = None
    DropDownSelected = None
    TableRowSelected = None

    @classmethod
    def _backend(cls):
        return Renderer.backend()

    @classmethod
    def _get_parent(cls):
        """Get the backend root window handle."""
        cls._backend().ensure()
        return Renderer._root

    @classproperty
    def LastClickedButton(cls) -> str:
        return cls._last_clicked_button

    @classproperty
    def LastTypedTextBox(cls) -> str:
        return cls._last_typed_textbox

    @classproperty
    def LastChangedSlider(cls) -> str:
        return cls._last_changed_slider

    @classproperty
    def LastSelectedDropDown(cls) -> str:
        return cls._last_selected_dropdown

    @classproperty
    def LastSelectedTable(cls) -> str:
        return cls._last_selected_table

    @classmethod
    def AddButton(cls, caption: str, left: int, top: int) -> str:
        cls._backend().ensure()
        cls._counter += 1
        name = f"Button{cls._counter}"

        def on_click():
            cls._last_clicked_button = name
            if cls.ButtonClicked:
                cls.ButtonClicked()

        handle = cls._backend().add_button(caption, left, top, callback=on_click)
        cls._widgets[name] = handle
        cls._types[name] = "button"
        return name

    @classmethod
    def GetButtonCaption(cls, button_name: str) -> str:
        handle = cls._widgets.get(button_name)
        if handle is not None and cls._types.get(button_name) == "button":
            return cls._backend().button_caption(handle)
        return ""

    @classmethod
    def SetButtonCaption(cls, button_name: str, caption: str) -> None:
        handle = cls._widgets.get(button_name)
        if handle is not None and cls._types.get(button_name) == "button":
            cls._backend().button_caption(handle, caption)

    @classmethod
    def AddTextBox(cls, left: int, top: int) -> str:
        return cls._add_textbox(left, top, multiline=False)

    @classmethod
    def AddMultiLineTextBox(cls, left: int, top: int) -> str:
        return cls._add_textbox(left, top, multiline=True)

    @classmethod
    def AddMultiLineText(cls, left: int, top: int) -> str:
        return cls.AddMultiLineTextBox(left, top)

    @classmethod
    def _add_textbox(cls, left: int, top: int, multiline: bool) -> str:
        cls._backend().ensure()
        cls._counter += 1
        name = f"TextBox{cls._counter}"

        def on_keyrelease():
            cls._last_typed_textbox = name
            if cls.TextTyped:
                cls.TextTyped()

        handle = cls._backend().add_textbox(
            left, top, callback=on_keyrelease, multiline=multiline)
        cls._widgets[name] = handle
        cls._types[name] = "multitext" if multiline else "textbox"
        return name

    @classmethod
    def GetTextBoxText(cls, textbox_name: str) -> str:
        handle = cls._widgets.get(textbox_name)
        if handle is None:
            return ""
        return cls._backend().textbox_text(handle)

    @classmethod
    def SetTextBoxText(cls, textbox_name: str, text: str) -> None:
        handle = cls._widgets.get(textbox_name)
        if handle is not None:
            cls._backend().textbox_text(handle, text)

    @classmethod
    def Remove(cls, control_name: str) -> None:
        handle = cls._widgets.pop(control_name, None)
        cls._types.pop(control_name, None)
        if handle is not None:
            cls._backend().control_destroy(handle)

    @classmethod
    def Move(cls, control: str, x: int, y: int) -> None:
        handle = cls._widgets.get(control)
        if handle is not None:
            cls._backend().control_move(handle, x, y)

    @classmethod
    def SetSize(cls, control: str, width: int, height: int) -> None:
        handle = cls._widgets.get(control)
        if handle is not None:
            cls._backend().control_size(handle, width, height)

    @classmethod
    def HideControl(cls, control_name: str) -> None:
        handle = cls._widgets.get(control_name)
        if handle is not None:
            cls._backend().control_visible(handle, False)

    @classmethod
    def ShowControl(cls, control_name: str) -> None:
        handle = cls._widgets.get(control_name)
        if handle is not None:
            cls._backend().control_visible(handle, True)

    # ── DropDown ──────────────────────────────────────────────────
    @classmethod
    def _as_list(cls, data) -> list:
        """Coerce a 1D array (list or Small Basic dictionary) to a list."""
        if isinstance(data, dict):
            return list(data.values())
        return list(data)

    @classmethod
    def AddDropDown(cls, items, left: int, top: int) -> str:
        cls._backend().ensure()
        cls._counter += 1
        name = f"DropDown{cls._counter}"

        def on_select():
            cls._last_selected_dropdown = name
            if cls.DropDownSelected:
                cls.DropDownSelected()

        handle = cls._backend().add_dropdown(
            cls._as_list(items), left, top, callback=on_select)
        cls._widgets[name] = handle
        cls._types[name] = "dropdown"
        return name

    @classmethod
    def GetSelectedDropDownItem(cls, name: str) -> str:
        handle = cls._widgets.get(name)
        if handle is not None and cls._types.get(name) == "dropdown":
            return cls._backend().dropdown_selected(handle)
        return ""

    @classmethod
    def SetSelectedDropDownItem(cls, name: str, index: int) -> None:
        handle = cls._widgets.get(name)
        if handle is not None and cls._types.get(name) == "dropdown":
            cls._backend().dropdown_set(handle, index)

    @classmethod
    def GetDropDownItemCount(cls, name: str) -> int:
        handle = cls._widgets.get(name)
        if handle is not None and cls._types.get(name) == "dropdown":
            return cls._backend().dropdown_count(handle)
        return 0

    @classmethod
    def GetDropDownItems(cls, name: str) -> list:
        handle = cls._widgets.get(name)
        if handle is not None and cls._types.get(name) == "dropdown":
            return cls._backend().dropdown_items(handle)
        return []

    # ── Slider ────────────────────────────────────────────────────
    @classmethod
    def AddSlider(cls, minimum: int, maximum: int, left: int, top: int) -> str:
        cls._backend().ensure()
        cls._counter += 1
        name = f"Slider{cls._counter}"

        def on_change():
            cls._last_changed_slider = name
            if cls.SliderChanged:
                cls.SliderChanged()

        handle = cls._backend().add_slider(
            minimum, maximum, left, top, callback=on_change)
        cls._widgets[name] = handle
        cls._types[name] = "slider"
        return name

    @classmethod
    def GetSliderValue(cls, name: str) -> int:
        handle = cls._widgets.get(name)
        if handle is not None and cls._types.get(name) == "slider":
            return cls._backend().slider_get(handle)
        return 0

    @classmethod
    def SetSliderValue(cls, name: str, value: int) -> None:
        handle = cls._widgets.get(name)
        if handle is not None and cls._types.get(name) == "slider":
            cls._backend().slider_set(handle, value)

    # ── ProgressBar ───────────────────────────────────────────────
    @classmethod
    def AddProgressBar(cls, left: int, top: int) -> str:
        cls._backend().ensure()
        cls._counter += 1
        name = f"ProgressBar{cls._counter}"
        handle = cls._backend().add_progressbar(left, top)
        cls._widgets[name] = handle
        cls._types[name] = "progressbar"
        return name

    @classmethod
    def GetProgressBarValue(cls, name: str) -> int:
        handle = cls._widgets.get(name)
        if handle is not None and cls._types.get(name) == "progressbar":
            return cls._backend().progress_get(handle)
        return 0

    @classmethod
    def SetProgressBarValue(cls, name: str, value: int) -> None:
        handle = cls._widgets.get(name)
        if handle is not None and cls._types.get(name) == "progressbar":
            cls._backend().progress_set(handle, value)

    # ── Table (2D array, first row = column headers) ─────────────
    @classmethod
    def AddTable(cls, data, left: int, top: int) -> str:
        cls._backend().ensure()
        cls._counter += 1
        name = f"Table{cls._counter}"

        def on_select():
            cls._last_selected_table = name
            if cls.TableRowSelected:
                cls.TableRowSelected()

        handle = cls._backend().add_table(data, left, top, callback=on_select)
        cls._widgets[name] = handle
        cls._types[name] = "table"
        return name

    @classmethod
    def SetTableData(cls, name: str, data) -> None:
        handle = cls._widgets.get(name)
        if handle is not None and cls._types.get(name) == "table":
            cls._backend().table_set_data(handle, data)

    @classmethod
    def GetSelectedTableRow(cls, name: str) -> int:
        """Return the currently selected data row (1-based), or 0 if none."""
        handle = cls._widgets.get(name)
        if handle is not None and cls._types.get(name) == "table":
            return cls._backend().table_selected_row(handle)
        return 0