"""
Demo 4: GraphicsWindow - drawing shapes, text, colors
"""

from smallbasic import GraphicsWindow, Program

GraphicsWindow.Title = "Graphics Shapes Demo"
GraphicsWindow.Width = 640
GraphicsWindow.Height = 480
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

# Rectangles
GraphicsWindow.PenColor = "Blue"
GraphicsWindow.PenWidth = 3
GraphicsWindow.DrawRectangle(20, 20, 150, 100)

GraphicsWindow.BrushColor = "LightBlue"
GraphicsWindow.FillRectangle(200, 20, 150, 100)

# Ellipses
GraphicsWindow.PenColor = "Red"
GraphicsWindow.DrawEllipse(20, 140, 120, 80)

GraphicsWindow.BrushColor = "LightGreen"
GraphicsWindow.FillEllipse(200, 140, 120, 80)

# Triangles
GraphicsWindow.PenColor = "Purple"
GraphicsWindow.DrawTriangle(400, 20, 480, 120, 350, 120)

GraphicsWindow.BrushColor = "Orange"
GraphicsWindow.FillTriangle(500, 20, 580, 120, 450, 120)

# Lines
GraphicsWindow.PenColor = "Black"
GraphicsWindow.PenWidth = 2
GraphicsWindow.DrawLine(20, 260, 300, 260)
GraphicsWindow.DrawLine(20, 265, 300, 265)

# Text
GraphicsWindow.FontSize = 18
GraphicsWindow.FontBold = True
GraphicsWindow.PenColor = "DarkBlue"
GraphicsWindow.DrawText(20, 290, "Hello from Python Small Basic!")

GraphicsWindow.FontSize = 12
GraphicsWindow.FontBold = False
GraphicsWindow.FontItalic = True
GraphicsWindow.PenColor = "Gray"
GraphicsWindow.DrawText(20, 320, "Italic text - different font settings")

# Random colors (batched for efficiency)
GraphicsWindow.BeginBatch()
for i in range(8):
    color = GraphicsWindow.GetColorFromRGB(
        30 * i, 200 - 20 * i, 100 + 15 * i
    )
    GraphicsWindow.BrushColor = color
    GraphicsWindow.FillEllipse(20 + i * 55, 380, 40, 30)
GraphicsWindow.EndBatch()

GraphicsWindow.Wait()
