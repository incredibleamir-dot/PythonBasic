"""
Demo 14: Mouse Coordinates — live mouse X/Y display on the GraphicsWindow
"""

from smallbasic import GraphicsWindow, Shapes, Program

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

def on_mouse_move(event):
    Shapes.SetText(coords, f"Mouse X: {event.x:>4}    Y: {event.y:>4}")

def on_mouse_down(event):
    btn = {1: "Left", 2: "Middle", 3: "Right"}.get(event.num, f"Button{event.num}")
    Shapes.SetText(mouse_info, f"{btn} button down at ({event.x}, {event.y})")

def on_mouse_up(event):
    btn = {1: "Left", 2: "Middle", 3: "Right"}.get(event.num, f"Button{event.num}")
    Shapes.SetText(mouse_info, f"{btn} button up at ({event.x}, {event.y})")

GraphicsWindow.MouseMove = on_mouse_move
GraphicsWindow.MouseDown = on_mouse_down
GraphicsWindow.MouseUp = on_mouse_up

Program.Delay(500)
GraphicsWindow.Wait()
