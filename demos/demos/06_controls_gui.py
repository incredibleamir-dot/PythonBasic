"""
Demo 6: Controls - Button, TextBox, MultiLine Text, events
"""

from smallbasic import Controls, GraphicsWindow, TextWindow, Program

GraphicsWindow.Title = "Controls Demo"
GraphicsWindow.Width = 600
GraphicsWindow.Height = 450
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

# TextBox
TextWindow.WriteLine("TextBox + Button Demo")
Controls.AddTextBox(20, 20)
Controls.SetTextBoxText("1", "Type something here")
Controls.AddButton("Show Text", 20, 50)

multi = Controls.AddMultiLineTextBox(20, 100)
Controls.SetTextBoxText(multi, "Multiline\ntext\nbox")
Controls.SetSize(multi, 260, 100)

# Event handling
def on_click():
    text = Controls.GetTextBoxText("1")
    Controls.SetTextBoxText(multi, f"Button clicked!\nText was: {text}")

Controls.ButtonClicked = on_click

Program.Delay(30000)
