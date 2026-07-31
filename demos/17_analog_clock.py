"""
Demo 17: Analog Clock — analog + digital clock
"""

from smallbasic import GraphicsWindow, Clock, Program, Shapes, Math

CX, CY, R = 300, 300, 200
GraphicsWindow.Title = "Analog Clock"
GraphicsWindow.Width = 600
GraphicsWindow.Height = 650
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

GraphicsWindow.PenColor = "Black"
GraphicsWindow.BrushColor = "LightYellow"
GraphicsWindow.FillEllipse(CX - R, CY - R, R * 2, R * 2)
GraphicsWindow.DrawEllipse(CX - R, CY - R, R * 2, R * 2)
for h in range(12):
    a = h * 30 - 90
    inner = R - 20
    outer = R - 8
    if h % 3 == 0:
        outer = R - 4
        inner = R - 30
    x1 = CX + inner * Math.Cos(a)
    y1 = CY + inner * Math.Sin(a)
    x2 = CX + outer * Math.Cos(a)
    y2 = CY + outer * Math.Sin(a)
    GraphicsWindow.PenWidth = 3 if h % 3 == 0 else 1
    GraphicsWindow.DrawLine(int(x1), int(y1), int(x2), int(y2))

GraphicsWindow.BrushColor = "Black"
GraphicsWindow.FillEllipse(CX - 5, CY - 5, 10, 10)

hour_hand = minute_hand = second_hand = None
digital = None

while True:
    h = Clock.Hour % 12
    m = Clock.Minute
    s = Clock.Second

    ha = (h * 30 + m * 0.5 - 90) * 3.14159 / 180
    ma = (m * 6 + s * 0.1 - 90) * 3.14159 / 180
    sa = (s * 6 - 90) * 3.14159 / 180

    for old in (hour_hand, minute_hand, second_hand, digital):
        if old:
            Shapes.Remove(old)

    GraphicsWindow.BeginBatch()
    GraphicsWindow.PenWidth = 4
    GraphicsWindow.PenColor = "Black"
    hx = CX + int(R * 0.5 * Math.Cos(ha * 180 / 3.14159))
    hy = CY + int(R * 0.5 * Math.Sin(ha * 180 / 3.14159))
    hour_hand = Shapes.AddLine(CX, CY, hx, hy)

    GraphicsWindow.PenWidth = 3
    mx = CX + int(R * 0.7 * Math.Cos(ma * 180 / 3.14159))
    my = CY + int(R * 0.7 * Math.Sin(ma * 180 / 3.14159))
    minute_hand = Shapes.AddLine(CX, CY, mx, my)

    GraphicsWindow.PenWidth = 1
    GraphicsWindow.PenColor = "Red"
    sx = CX + int(R * 0.85 * Math.Cos(sa * 180 / 3.14159))
    sy = CY + int(R * 0.85 * Math.Sin(sa * 180 / 3.14159))
    second_hand = Shapes.AddLine(CX, CY, sx, sy)

    GraphicsWindow.FontSize = 24
    GraphicsWindow.FontBold = True
    GraphicsWindow.PenColor = "Black"
    digital = Shapes.AddText(f"{Clock.Hour:02d}:{Clock.Minute:02d}:{Clock.Second:02d}")
    Shapes.Move(digital, CX - 50, CY + R + 20)
    GraphicsWindow.EndBatch()

    Program.Delay(500)