"""
Demo 20: Extended Controls — dropdown, slider, progress bar, table.

New controls added to the Controls object:

    Controls.AddDropDown(items, left, top)        1D list (or Small Basic array)
    Controls.AddSlider(min, max, left, top)
    Controls.AddProgressBar(left, top)
    Controls.AddTable(data, left, top)            data = 2D array, 1st row = headers

They also fire events, just like ButtonClicked / TextTyped:

    Controls.DropDownSelected  (use Controls.LastSelectedDropDown)
    Controls.SliderChanged     (use Controls.LastChangedSlider)
    Controls.TableRowSelected  (use Controls.LastSelectedTable + GetSelectedTableRow)
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import GraphicsWindow, Controls, TextWindow

GraphicsWindow.Title = "Extended Controls"
GraphicsWindow.Width = 880
GraphicsWindow.Height = 520
GraphicsWindow.Show()

# --- DropDown (accepts a plain 1D list or a Small Basic array) ---
fruits = ["Apple", "Banana", "Cherry", "Date"]
dd = Controls.AddDropDown(fruits, 20, 20)
Controls.SetSelectedDropDownItem(dd, 2)

# --- Slider ---
sl = Controls.AddSlider(0, 100, 20, 60)
Controls.SetSliderValue(sl, 40)

# --- Progress Bar ---
pb = Controls.AddProgressBar(20, 100)
Controls.SetProgressBarValue(pb, 25)

# --- Table (2D array: first row is used as the column headers) ---
scoreboard = [
    ["Player", "Score", "Level"],
    ["Alice", 3400, 7],
    ["Bob", 2200, 5],
    ["Carol", 5100, 9],
]
table = Controls.AddTable(scoreboard, 20, 160)


def read_values():
    TextWindow.WriteLine("Selected fruit : " + Controls.GetSelectedDropDownItem(dd))
    TextWindow.WriteLine("Slider value   : " + str(Controls.GetSliderValue(sl)))
    TextWindow.WriteLine("Progress       : " + str(Controls.GetProgressBarValue(pb)))
    TextWindow.WriteLine("DropDown items : " + ", ".join(Controls.GetDropDownItems(dd)))


btn = Controls.AddButton("Read Values", 460, 20)
Controls.ButtonClicked = read_values


def on_dropdown_selected():
    TextWindow.WriteLine("Picked: " + Controls.GetSelectedDropDownItem(dd))


def on_slider_changed():
    TextWindow.WriteLine("Slider now: " + str(Controls.GetSliderValue(sl)))


def on_table_row_selected():
    TextWindow.WriteLine("Row " + str(Controls.GetSelectedTableRow(table))
                         + " selected in " + Controls.LastSelectedTable)


Controls.DropDownSelected = on_dropdown_selected
Controls.SliderChanged = on_slider_changed
Controls.TableRowSelected = on_table_row_selected

GraphicsWindow.Wait()
