"""
Demo 5: Turtle - Logo-style drawing
"""

from smallbasic import Turtle, GraphicsWindow, Program

GraphicsWindow.Title = "Turtle Demo"
GraphicsWindow.Width = 640
GraphicsWindow.Height = 480
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

Turtle.Speed = 8
Turtle.Show()
Program.Delay(500)

# Square
GraphicsWindow.PenColor = "Blue"
Turtle.PenDown()
for _ in range(4):
    Turtle.Move(100)
    Turtle.Turn(-90)

# Move to new position
Turtle.PenUp()
Turtle.MoveTo(200, 200)
Turtle.Angle = 0

# Triangle
GraphicsWindow.PenColor = "Red"
Turtle.PenDown()
for _ in range(3):
    Turtle.Move(80)
    Turtle.Turn(-120)

# Star
Turtle.PenUp()
Turtle.MoveTo(450, 200)
Turtle.PenDown()
GraphicsWindow.PenColor = "Purple"
for _ in range(5):
    Turtle.Move(60)
    Turtle.Turn(-144)

# Spiral
Turtle.PenUp()
Turtle.MoveTo(100, 350)
Turtle.Angle = 0
Turtle.PenDown()
GraphicsWindow.PenColor = "DarkGreen"
for i in range(20):
    Turtle.Move(8 + i * 3)
    Turtle.Turn(-60)

Turtle.Hide()
GraphicsWindow.DrawText(20, 10, "Turtle drawing complete!")
