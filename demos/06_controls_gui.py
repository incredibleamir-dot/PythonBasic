"""
Demo 6: Controls - Button, TextBox, MultiLine Text, events
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import Controls, GraphicsWindow, TextWindow, Program

GraphicsWindow.Title = "Controls Demo"
GraphicsWindow.Width = 600
GraphicsWindow.Height = 450
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

# TextBox
TextWindow.WriteLine("TextBox + Button Demo")
tb = Controls.AddTextBox(20, 20)
Controls.SetTextBoxText(tb, "Type something here")
Controls.AddButton("Show Text", 20, 50)

multi = Controls.AddMultiLineTextBox(20, 100)
Controls.SetTextBoxText(multi, "Multiline\ntext\nbox")
Controls.SetSize(multi, 260, 100)

# Event handling
def on_click():
    text = Controls.GetTextBoxText(tb)
    Controls.SetTextBoxText(multi, f"Button clicked!\nText was: {text}")

Controls.ButtonClicked = on_click

Program.Delay(500)
GraphicsWindow.Wait()
