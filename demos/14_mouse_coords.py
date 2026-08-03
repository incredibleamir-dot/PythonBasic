"""
Demo 14: Mouse Coordinates — live mouse X/Y display on the GraphicsWindow
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import GraphicsWindow, Shapes, Program, Mouse

GraphicsWindow.Title = "Mouse Coordinates Demo"
GraphicsWindow.Width = 500
GraphicsWindow.Height = 300
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

GraphicsWindow.FontSize = 14
GraphicsWindow.FontBold = True
coords = Shapes.AddText("Move the mouse over this window")
Shapes.Move(coords, 20, 40)

GraphicsWindow.FontSize = 11
GraphicsWindow.FontBold = False
GraphicsWindow.PenColor = "Gray"
hint = Shapes.AddText("X, Y values update live via MouseMove event")
Shapes.Move(hint, 20, 70)

GraphicsWindow.PenColor = "LightGray"
GraphicsWindow.DrawRectangle(20, 100, 460, 100)

GraphicsWindow.PenColor = "Black"
mouse_info = Shapes.AddText("")
Shapes.Move(mouse_info, 20, 130)

def on_mouse_move():
    Shapes.SetText(coords, f"Mouse X: {GraphicsWindow.MouseX:>4}    Y: {GraphicsWindow.MouseY:>4}")

def on_mouse_down():
    if Mouse.IsLeftButtonDown:
        btn = "Left"
    elif Mouse.IsRightButtonDown:
        btn = "Right"
    else:
        btn = "Middle"
    Shapes.SetText(mouse_info,
                   f"{btn} button down at ({GraphicsWindow.MouseX}, {GraphicsWindow.MouseY})")

def on_mouse_up():
    Shapes.SetText(mouse_info,
                   f"Button up at ({GraphicsWindow.MouseX}, {GraphicsWindow.MouseY})")

GraphicsWindow.MouseMove = on_mouse_move
GraphicsWindow.MouseDown = on_mouse_down
GraphicsWindow.MouseUp = on_mouse_up

Program.Delay(500)
GraphicsWindow.Wait()
