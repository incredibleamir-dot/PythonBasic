"""
Demo 10: All Features - keyboard/mouse events, mouse drawing
"""

from smallbasic import *

GraphicsWindow.Title = "All Features Demo"
GraphicsWindow.Width = 800
GraphicsWindow.Height = 600
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

# Info
TextWindow.BackgroundColor = "DarkBlue"
TextWindow.ForegroundColor = "White"
TextWindow.Title = "Event Log"
TextWindow.Show()

TextWindow.WriteLine("=== All Features Demo ===")
TextWindow.WriteLine("Click on the GraphicsWindow to draw circles.")
TextWindow.WriteLine("Press ESC to clear, UP arrow for info.")
TextWindow.WriteLine()

# Mouse drawing
def draw_circle(event):
    x = GraphicsWindow.MouseX - 15
    y = GraphicsWindow.MouseY - 15
    r = Math.GetRandomNumber(20) + 10
    GraphicsWindow.BrushColor = GraphicsWindow.GetRandomColor()
    GraphicsWindow.FillEllipse(x, y, r * 2, r * 2)
    TextWindow.WriteLine(f"Drew circle at ({x}, {y}), radius={r}")

GraphicsWindow.MouseDown = draw_circle

# Keyboard events
def on_key(event):
    key = GraphicsWindow.LastKey
    if key == "Escape":
        GraphicsWindow.Clear()
        TextWindow.WriteLine("Cleared!")
    elif key == "Up":
        TextWindow.WriteLine(
            f"Mouse: ({GraphicsWindow.MouseX}, {GraphicsWindow.MouseY})"
        )

GraphicsWindow.KeyDown = on_key

# Mouse move tracking
def on_move(event):
    pass  # Can be used for e.g. status

GraphicsWindow.MouseMove = on_move

# Controls
Controls.AddButton("Clear", 20, 20)

def on_click():
    GraphicsWindow.Clear()
Controls.ButtonClicked = on_click

TextWindow.WriteLine("Ready! Click the canvas or press keys.")
GraphicsWindow.Wait()
