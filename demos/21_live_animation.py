"""
Demo 21: Live Animation — responsive animation.

Animation loops no longer use bare blocking sleeps: each frame keeps the
event loop alive, so the window stays fully responsive while shapes move
and the turtle draws.  Click the canvas while the animation plays —
nothing freezes or crashes.

    python demos/21_live_animation.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import GraphicsWindow, Shapes, Turtle, Controls

GraphicsWindow.Title = "Live Animation - click the canvas while it plays"
GraphicsWindow.Width = 640
GraphicsWindow.Height = 520
GraphicsWindow.Show()

# --- a progress bar that fills while things move ---
pb = Controls.AddProgressBar(20, 20)
progress = 0

# --- a bouncing ball driven by Shapes.Animate (pumps frames) ---
ball = Shapes.AddEllipse(50, 50)
GraphicsWindow.PenColor = "Orange"
GraphicsWindow.PenWidth = 3

bounce_left = [(x, 360) for x in range(60, 560, 50)]
bounce_right = [(x, 360) for x in range(560, 60, -50)]

for target in bounce_left + bounce_right:
    Shapes.Animate(ball, target[0], target[1], 350)

    progress = min(100, progress + 10)
    Controls.SetProgressBarValue(pb, progress)

# --- a turtle spiral (Turtle.Move also pumps frames) ---
Turtle.Speed = 6
Turtle.X = 320
Turtle.Y = 360
Turtle.Angle = 0
Turtle.Show()
for i in range(1, 14):
    Turtle.Move(i * 10)
    Turtle.Turn(90)
Turtle.Hide()

Controls.SetProgressBarValue(pb, 100)
GraphicsWindow.DrawText(20, 60, "Done! The window stayed responsive throughout.")
GraphicsWindow.Wait()
