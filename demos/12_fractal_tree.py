"""
Fractal Tree — drawn with Python Small Basic Turtle.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import Turtle, GraphicsWindow, Program


def draw_branch(length, depth):
    if depth == 0:
        return

    Turtle.Move(length)

    Turtle.Turn(30)
    draw_branch(length * 0.7, depth - 1)

    Turtle.Turn(-60)
    draw_branch(length * 0.7, depth - 1)

    Turtle.Turn(30)
    Turtle.Move(-length)


GraphicsWindow.Title = "Fractal Tree"
GraphicsWindow.Width = 640
GraphicsWindow.Height = 480
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

Turtle.Speed = 10
Turtle.X = 320
Turtle.Y = 460
Turtle.Angle = 90
Turtle.PenDown()
Turtle.Show()

draw_branch(100, 8)

Turtle.Hide()
GraphicsWindow.DrawText(220, 10, "Fractal Tree - Python Small Basic")
GraphicsWindow.Wait()
