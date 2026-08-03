"""
Demo 22: Shape Transform Playground — create, move, rotate and zoom shapes.

Interactively transform the currently selected shape with the keyboard:

    Tab      cycle to the next shape
    Arrows   move the selected shape
    A / D    rotate left / right
    W / S    zoom in / out
    N        create a new shape
    R        reset the selected shape (position, angle, size)
    X        remove the selected shape
    Esc      quit

    python demos/22_shape_transforms.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import GraphicsWindow, Shapes, Program, Math

W, H = 640, 480
MARGIN = 30

GraphicsWindow.Title = "Shape Transform Playground"
GraphicsWindow.Width = W
GraphicsWindow.Height = H
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

# Default templates for each shape type.
TEMPLATES = {
    "rectangle": lambda: Shapes.AddRectangle(120, 70),
    "ellipse":   lambda: Shapes.AddEllipse(90, 90),
    "triangle":  lambda: Shapes.AddTriangle(0, 0, 60, 60, 120, 0),
}
ORDER = ["rectangle", "ellipse", "triangle"]
COLORS = ["Black", "DarkBlue", "DarkGreen", "DarkRed", "Purple"]

shapes = []        # list of dicts: name, type, x, y, angle, zoom
selected = 0


def random_position():
    return (Math.GetRandomNumber(W - MARGIN * 2) + MARGIN,
            Math.GetRandomNumber(H - MARGIN * 2) + MARGIN)


def spawn(shape_type, x, y):
    """Create a shape of `shape_type` at (x, y) and return its info dict."""
    GraphicsWindow.PenColor = COLORS[len(shapes) % len(COLORS)]
    GraphicsWindow.PenWidth = 2
    name = TEMPLATES[shape_type]()
    Shapes.Move(name, x, y)
    return {"name": name, "type": shape_type,
            "x": x, "y": y, "angle": 0, "zoom": 0}


# Spawn one of each shape type scattered around the window.
for stype in ORDER:
    x, y = random_position()
    shapes.append(spawn(stype, x, y))

# ---------------------------------------------------------------------------
# HUD + selection marker
# ---------------------------------------------------------------------------
GraphicsWindow.FontSize = 13
GraphicsWindow.FontBold = True
GraphicsWindow.PenColor = "DarkGray"
hud = Shapes.AddText("")
Shapes.Move(hud, 10, 10)

GraphicsWindow.PenColor = "Green"
GraphicsWindow.PenWidth = 2
marker = Shapes.AddRectangle(10, 10)
Shapes.ShowShape(marker)


def refresh_hud():
    sel = shapes[selected]
    title = f"> {sel['type'].upper():<10} pos ({sel['x']:>3},{sel['y']:>3})  angle {sel['angle']:>3}"
    hint = "Tab: next   Arrows: move   A/D: rotate   W/S: zoom   N: new   R: reset   X: remove   Esc: quit"
    Shapes.SetText(hud, f"{title}\n{hint}")


# ---------------------------------------------------------------------------
# Keyboard input (events fire while the loop pumps GraphicsWindow.update())
# ---------------------------------------------------------------------------
MOVE_STEP, ROT_STEP, ZOOM_STEP = 4, 3, 1.04
ZOOM_LIMIT = 20
keys = {"up": False, "down": False, "left": False, "right": False,
        "rot_l": False, "rot_r": False, "zoom_in": False, "zoom_out": False}


def on_key_down():
    global selected
    k = GraphicsWindow.LastKey
    if k == "Up":
        keys["up"] = True
    elif k == "Down":
        keys["down"] = True
    elif k == "Left":
        keys["left"] = True
    elif k == "Right":
        keys["right"] = True
    elif k == "a":
        keys["rot_l"] = True
    elif k == "d":
        keys["rot_r"] = True
    elif k == "w":
        keys["zoom_in"] = True
    elif k == "s":
        keys["zoom_out"] = True
    elif k == "Tab":
        selected = (selected + 1) % len(shapes)
    elif k == "n":
        x, y = random_position()
        shapes.append(spawn(ORDER[len(shapes) % len(ORDER)], x, y))
        selected = len(shapes) - 1
    elif k == "r":
        sel = shapes[selected]
        Shapes.Remove(sel["name"])
        shapes[selected] = spawn(sel["type"], sel["x"], sel["y"])
    elif k == "x":
        sel = shapes[selected]
        Shapes.Remove(sel["name"])
        shapes.pop(selected)
        if not shapes:
            GraphicsWindow.Hide()
            Program.End()
        selected %= len(shapes)
    elif k == "Escape":
        GraphicsWindow.Hide()
        Program.End()


def on_key_up():
    k = GraphicsWindow.LastKey
    if k == "Up":
        keys["up"] = False
    elif k == "Down":
        keys["down"] = False
    elif k == "Left":
        keys["left"] = False
    elif k == "Right":
        keys["right"] = False
    elif k == "a":
        keys["rot_l"] = False
    elif k == "d":
        keys["rot_r"] = False
    elif k == "w":
        keys["zoom_in"] = False
    elif k == "s":
        keys["zoom_out"] = False


GraphicsWindow.KeyDown = on_key_down
GraphicsWindow.KeyUp = on_key_up

refresh_hud()

# ---------------------------------------------------------------------------
# Main loop. Shapes.Move / Shapes.SetText below pump the Tk event queue, which
# is what delivers the KeyDown/KeyUp events, so no explicit pump call is needed.
# ---------------------------------------------------------------------------
while True:
    sel = shapes[selected]

    # Continuous transforms from held-down keys.
    moved = False
    if keys["up"]:
        sel["y"] -= MOVE_STEP; moved = True
    if keys["down"]:
        sel["y"] += MOVE_STEP; moved = True
    if keys["left"]:
        sel["x"] -= MOVE_STEP; moved = True
    if keys["right"]:
        sel["x"] += MOVE_STEP; moved = True
    if moved:
        Shapes.Move(sel["name"], sel["x"], sel["y"])

    if keys["rot_l"] or keys["rot_r"]:
        sel["angle"] = (sel["angle"] + (ROT_STEP if keys["rot_r"] else -ROT_STEP)) % 360
        Shapes.Rotate(sel["name"], sel["angle"])

    if keys["zoom_in"] and sel["zoom"] < ZOOM_LIMIT:
        Shapes.Zoom(sel["name"], ZOOM_STEP, ZOOM_STEP)
        sel["zoom"] += 1
    elif keys["zoom_out"] and sel["zoom"] > -ZOOM_LIMIT:
        Shapes.Zoom(sel["name"], 1 / ZOOM_STEP, 1 / ZOOM_STEP)
        sel["zoom"] -= 1

    # Keep the green selection marker glued to the shape's top-left corner.
    Shapes.Move(marker, sel["x"] - 5, sel["y"] - 5)
    refresh_hud()

    Program.Delay(16)
