"""
Demo 19: Brick Breaker - break all the bricks with the ball.

Move the paddle with the Left / Right arrow keys. The ball bounces off the
walls, the paddle and the bricks. Every brick you break adds a point; the
ball drops below the screen you lose a life. Three lives - break them all!

    python demos/19_brick_breaker.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import GraphicsWindow, Shapes, Program

W, H = 640, 480
GraphicsWindow.Title = "Brick Breaker"
GraphicsWindow.Width = W
GraphicsWindow.Height = H
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

# ---------------------------------------------------------------------------
# Bricks (a coloured grid near the top)
# ---------------------------------------------------------------------------
BRICK_W, BRICK_H, GAP = 62, 18, 6
MARGIN = 20
top = 45
bricks = []
colors = ["Red", "Orange", "Gold", "Lime", "Cyan"]
for row, color in enumerate(colors):
    y = top + row * (BRICK_H + GAP)
    x = MARGIN
    while x + BRICK_W <= W - MARGIN:
        GraphicsWindow.BrushColor = color
        name = Shapes.AddRectangle(BRICK_W, BRICK_H)
        Shapes.Move(name, x, y)
        bricks.append({"name": name, "x": x, "y": y,
                       "w": BRICK_W, "h": BRICK_H, "alive": True})
        x += BRICK_W + GAP

# ---------------------------------------------------------------------------
# Paddle, ball and score display
# ---------------------------------------------------------------------------
PADDLE_W, PADDLE_H = 90, 12
PADDLE_SPEED = 6
R = 8

paddle_x = (W - PADDLE_W) // 2
paddle_y = H - 40
GraphicsWindow.BrushColor = "DarkBlue"
paddle = Shapes.AddRectangle(PADDLE_W, PADDLE_H)
Shapes.Move(paddle, paddle_x, paddle_y)

ball_x, ball_y = paddle_x + PADDLE_W // 2, paddle_y - R
ball_dx, ball_dy = 3, 3
GraphicsWindow.BrushColor = "Red"
ball = Shapes.AddEllipse(R * 2, R * 2)
Shapes.Move(ball, ball_x - R, ball_y - R)

GraphicsWindow.FontSize = 12
GraphicsWindow.FontBold = True
GraphicsWindow.PenColor = "Black"
hud = Shapes.AddText("Score: 0   Lives: 3")
Shapes.Move(hud, 15, 15)

score = 0
lives = 3
keys = {"left": False, "right": False}

# ---------------------------------------------------------------------------
# Arrow-key input (events fire while the loop pumps GraphicsWindow.update())
# ---------------------------------------------------------------------------
def on_key_down():
    k = GraphicsWindow.LastKey
    if k == "Left":
        keys["left"] = True
    elif k == "Right":
        keys["right"] = True

def on_key_up():
    k = GraphicsWindow.LastKey
    if k == "Left":
        keys["left"] = False
    elif k == "Right":
        keys["right"] = False

GraphicsWindow.KeyDown = on_key_down
GraphicsWindow.KeyUp = on_key_up


def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = paddle_x + PADDLE_W // 2
    ball_y = paddle_y - R
    ball_dx, ball_dy = 3, 3


def game_over(text):
    GraphicsWindow.FontSize = 30
    GraphicsWindow.FontBold = True
    GraphicsWindow.PenColor = "Black"
    msg = Shapes.AddText(text)
    Shapes.Move(msg, W // 2 - len(text) * 8, H // 2)
    GraphicsWindow.Wait()


# ---------------------------------------------------------------------------
# Game loop
# ---------------------------------------------------------------------------
# Game loop. Every Shapes.Move / Shapes.SetText call below triggers a
# Renderer.update(), which pumps the window's event queue. That is what both
# redraws the scene AND delivers the arrow-key events, so no explicit
# main-loop / pump call is needed here.
while True:
    try:
        # paddle
        if keys["left"]:
            paddle_x = max(0, paddle_x - PADDLE_SPEED)
        if keys["right"]:
            paddle_x = min(W - PADDLE_W, paddle_x + PADDLE_SPEED)
        Shapes.Move(paddle, paddle_x, paddle_y)

        # ball
        ball_x += ball_dx
        ball_y += ball_dy

        # walls
        if ball_x < R or ball_x > W - R:
            ball_dx = -ball_dx
            ball_x = max(R, min(W - R, ball_x))
        if ball_y < R:
            ball_dy = -ball_dy
            ball_y = R

        # paddle bounce (angled by where the ball hits)
        if (ball_dy > 0 and
                paddle_y <= ball_y + R <= paddle_y + PADDLE_H + ball_dy and
                paddle_x <= ball_x <= paddle_x + PADDLE_W):
            offset = (ball_x - (paddle_x + PADDLE_W / 2)) / (PADDLE_W / 2)
            ball_dy = -abs(ball_dy)
            ball_dx = max(1.0, abs(offset * 4)) * (1 if offset >= 0 else -1)
            ball_y = paddle_y - R

        # bricks
        for brick in bricks:
            if not brick["alive"]:
                continue
            if (ball_x + R > brick["x"] and ball_x - R < brick["x"] + brick["w"] and
                    ball_y + R > brick["y"] and ball_y - R < brick["y"] + brick["h"]):
                brick["alive"] = False
                Shapes.Remove(brick["name"])
                ball_dy = -ball_dy
                score += 1
                break

        Shapes.SetText(hud, "Score: %d   Lives: %d" % (score, lives))
        Shapes.Move(ball, ball_x - R, ball_y - R)

        # win
        if score == len(bricks):
            game_over("You Win!")
            break

        # lost a life
        if ball_y - R > H:
            lives -= 1
            if lives <= 0:
                game_over("Game Over")
                break
            reset_ball()

        Program.Delay(16)
    except Exception:
        break       # window was closed -> stop the game
