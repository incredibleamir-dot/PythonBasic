"""
Demo 16: Bouncing Ball — simple animation with GraphicsWindow
"""

from smallbasic import GraphicsWindow, Program, Shapes, Clock

W, H = 600, 400
R = 15
x, y = 100, 100
dx, dy = 4, 3

GraphicsWindow.Title = "Bouncing Ball"
GraphicsWindow.Width = W
GraphicsWindow.Height = H
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

GraphicsWindow.BrushColor = "Red"
ball = Shapes.AddEllipse(R * 2, R * 2)
Shapes.Move(ball, x - R, y - R)

start = Clock.ElapsedMilliseconds
frames = 0
while Clock.ElapsedMilliseconds - start < 15000:
    x += dx
    y += dy
    if x < R or x > W - R:
        dx = -dx
    if x < R or x > W - R:
        x = max(R, min(W - R, x))
    if y < R or y > H - R:
        dy = -dy
    if y < R or y > H - R:
        y = max(R, min(H - R, y))

    GraphicsWindow.BeginBatch()
    Shapes.Move(ball, x - R, y - R)
    GraphicsWindow.EndBatch()

    frames += 1
    Program.Delay(16)
