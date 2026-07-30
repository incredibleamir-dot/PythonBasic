"""
Comprehensive test suite for Python Small Basic.
"""

import sys
import os
import time
import math
import tempfile

sys.path.insert(0, os.path.dirname(__file__))

import smallbasic
from smallbasic import *
from smallbasic._state import GraphicsState
from smallbasic._renderer import Renderer

passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  OK  {name}")
    else:
        failed += 1
        print(f"  FAIL {name}  {detail}")

# ====================================================================
# 1. Module & Public API
# ====================================================================
print("\n=== 1. Public API ===")

expected_api = {'Array', 'Clock', 'Controls', 'Desktop', 'Dictionary',
                'File', 'GraphicsWindow', 'ImageList', 'Keywords',
                'Math', 'Mouse', 'Network', 'Program', 'Shapes',
                'Sound', 'Stack', 'Text', 'TextWindow', 'Timer', 'Turtle'}
check("20 names in __all__",
      set(smallbasic.__all__) == expected_api)
# star-import verified via __all__ above

# ====================================================================
# 2. GraphicsState
# ====================================================================
print("\n=== 2. GraphicsState ===")

check("width default 640", GraphicsState.width == 640)
check("height default 480", GraphicsState.height == 480)
check("pen_color default Black", GraphicsState.pen_color == "Black")
check("pen_width default 2", GraphicsState.pen_width == 2)
check("brush_color default Gray", GraphicsState.brush_color == "Gray")
check("font_name default Consolas", GraphicsState.font_name == "Consolas")
check("font_size default 12", GraphicsState.font_size == 12)
check("font_bold default False", GraphicsState.font_bold is False)
check("font_italic default False", GraphicsState.font_italic is False)
check("left default 100", GraphicsState.left == 100)
check("top default 100", GraphicsState.top == 100)
check("can_resize default True", GraphicsState.can_resize is True)
check("shown default False", GraphicsState.shown is False)

# Mutation
GraphicsState.pen_color = "Red"
check("mutate pen_color", GraphicsState.pen_color == "Red")
GraphicsState.pen_color = "Black"  # reset

# ====================================================================
# 3. Renderer (non-GUI methods)
# ====================================================================
print("\n=== 3. Renderer ===")

check("ensure returns tk root", Renderer.ensure() is not None)
check("get_random_color returns hex",
      Renderer.get_random_color().startswith("#"))
check("get_random_color 7 chars",
      len(Renderer.get_random_color()) == 7)
check("get_color_from_rgb",
      Renderer.get_color_from_rgb(255, 0, 0) == "#FF0000")
check("get_color_from_rgb clamped",
      Renderer.get_color_from_rgb(300, -10, 128) == "#FF0080")

# Object registry
check("object registry exists",
      hasattr(Renderer, '_objects') and isinstance(Renderer._objects, dict))

# ====================================================================
# 4. GraphicsWindow — property forwarding
# ====================================================================
print("\n=== 4. GraphicsWindow properties ===")

GraphicsWindow.Width = 800
check("Width get", GraphicsWindow.Width == 800)
GraphicsWindow.Width = 640
check("Width reset", GraphicsWindow.Width == 640)

GraphicsWindow.Height = 600
check("Height get", GraphicsWindow.Height == 600)
GraphicsWindow.Height = 480

GraphicsWindow.Title = "Test"
check("Title get", GraphicsWindow.Title == "Test")
GraphicsWindow.Title = "Small Basic Graphics Window"

GraphicsWindow.BackgroundColor = "LightGray"
check("BackgroundColor get", GraphicsWindow.BackgroundColor == "LightGray")
GraphicsWindow.BackgroundColor = "White"

GraphicsWindow.PenColor = "Blue"
check("PenColor get", GraphicsWindow.PenColor == "Blue")
GraphicsWindow.PenColor = "Black"

GraphicsWindow.PenWidth = 5
check("PenWidth get", GraphicsWindow.PenWidth == 5)
GraphicsWindow.PenWidth = 2

GraphicsWindow.BrushColor = "Yellow"
check("BrushColor get", GraphicsWindow.BrushColor == "Yellow")
GraphicsWindow.BrushColor = "Gray"

GraphicsWindow.FontName = "Arial"
check("FontName get", GraphicsWindow.FontName == "Arial")
GraphicsWindow.FontName = "Consolas"

GraphicsWindow.FontSize = 18
check("FontSize get", GraphicsWindow.FontSize == 18)
GraphicsWindow.FontSize = 12

GraphicsWindow.FontBold = True
check("FontBold get", GraphicsWindow.FontBold is True)
GraphicsWindow.FontBold = False

GraphicsWindow.FontItalic = True
check("FontItalic get", GraphicsWindow.FontItalic is True)
GraphicsWindow.FontItalic = False

GraphicsWindow.CanResize = False
check("CanResize get", GraphicsWindow.CanResize is False)
GraphicsWindow.CanResize = True

GraphicsWindow.Left = 200
check("Left get", GraphicsWindow.Left == 200)
GraphicsWindow.Left = 100

GraphicsWindow.Top = 200
check("Top get", GraphicsWindow.Top == 200)
GraphicsWindow.Top = 100

# ====================================================================
# 5. GraphicsWindow — event forwarding
# ====================================================================
print("\n=== 5. GraphicsWindow events ===")

def cb(): pass

GraphicsWindow.KeyDown = cb
check("KeyDown forward", GraphicsState.KeyDown is cb)
GraphicsWindow.KeyDown = None
check("KeyDown reset", GraphicsState.KeyDown is None)

GraphicsWindow.KeyUp = cb
check("KeyUp forward", GraphicsState.KeyUp is cb)
GraphicsWindow.KeyUp = None

GraphicsWindow.MouseDown = cb
check("MouseDown forward", GraphicsState.MouseDown is cb)
GraphicsWindow.MouseDown = None

GraphicsWindow.MouseUp = cb
check("MouseUp forward", GraphicsState.MouseUp is cb)
GraphicsWindow.MouseUp = None

GraphicsWindow.MouseMove = cb
check("MouseMove forward", GraphicsState.MouseMove is cb)
GraphicsWindow.MouseMove = None

# ====================================================================
# 6. GraphicsWindow — drawing methods (smoke, no display)
# ====================================================================
print("\n=== 6. GraphicsWindow drawing (smoke) ===")

try:
    GraphicsWindow.Show()
    check("Show()", True)
    GraphicsWindow.DrawRectangle(10, 10, 100, 50)
    check("DrawRectangle", True)
    GraphicsWindow.FillRectangle(120, 10, 100, 50)
    check("FillRectangle", True)
    GraphicsWindow.DrawEllipse(10, 70, 80, 50)
    check("DrawEllipse", True)
    GraphicsWindow.FillEllipse(100, 70, 80, 50)
    check("FillEllipse", True)
    GraphicsWindow.DrawTriangle(200, 10, 250, 60, 180, 60)
    check("DrawTriangle", True)
    GraphicsWindow.FillTriangle(270, 10, 320, 60, 250, 60)
    check("FillTriangle", True)
    GraphicsWindow.DrawLine(10, 130, 200, 130)
    check("DrawLine", True)
    GraphicsWindow.DrawText(10, 140, "Hello")
    check("DrawText", True)
    GraphicsWindow.DrawBoundText(10, 160, 100, "Wrapped text test")
    check("DrawBoundText", True)
    GraphicsWindow.SetPixel(10, 200, "Red")
    check("SetPixel", True)
    color = GraphicsWindow.GetPixel(10, 200)
    check("GetPixel returns color", isinstance(color, str) and len(color) > 0)
    rc = GraphicsWindow.GetRandomColor()
    check("GetRandomColor", rc.startswith("#") and len(rc) == 7)
    rgb = GraphicsWindow.GetColorFromRGB(100, 150, 200)
    check("GetColorFromRGB", rgb == "#6496C8")
    GraphicsWindow.Clear()
    check("Clear", True)

    # DrawImage and DrawResizedImage (no image loaded — should not crash)
    GraphicsWindow.DrawImage("nonexistent", 0, 0)
    check("DrawImage (missing)", True)
    GraphicsWindow.DrawResizedImage("nonexistent", 0, 0, 50, 50)
    check("DrawResizedImage (missing)", True)

    GraphicsWindow.Hide()
    check("Hide", True)
except Exception as e:
    check("Drawing methods", False, str(e))
    GraphicsWindow.Hide()

# ====================================================================
# 7. Program
# ====================================================================
print("\n=== 7. Program ===")

check("ArgumentCount exists", hasattr(Program, "ArgumentCount"))
check("Directory exists", os.path.isdir(Program.Directory))
check("Delay does not crash", (Program.Delay(10), True)[1])
check("GetArgument returns str", isinstance(Program.GetArgument(1), str))

# ====================================================================
# 8. Math
# ====================================================================
print("\n=== 8. Math ===")

check("Pi ~ 3.14", abs(Math.Pi - 3.14159) < 0.001)
check("Abs(-5)=5", Math.Abs(-5) == 5)
check("Ceiling(3.1)=4", Math.Ceiling(3.1) == 4)
check("Floor(3.9)=3", Math.Floor(3.9) == 3)
check("Round(3.5)=4", Math.Round(3.5) == 4)
check("Sin(90)~1", abs(Math.Sin(90) - 1) < 0.001)
check("Cos(0)~1", abs(Math.Cos(0) - 1) < 0.001)
check("Tan(45)~1", abs(Math.Tan(45) - 1) < 0.1)
check("SquareRoot(9)=3", Math.SquareRoot(9) == 3)
check("Power(2,3)=8", Math.Power(2, 3) == 8)
check("Max(1,5,3)=5", Math.Max(1, 5, 3) == 5)
check("Min(1,5,3)=1", Math.Min(1, 5, 3) == 1)
check("Sum(1,2,3)=6", Math.Sum(1, 2, 3) == 6)
check("Average(1,2,3)=2", Math.Average(1, 2, 3) == 2.0)
check("Remainder(10,3)=1", Math.Remainder(10, 3) == 1)
r = Math.GetRandomNumber(10)
check("GetRandomNumber 1..10", 1 <= r <= 10)

# ====================================================================
# 9. Text
# ====================================================================
print("\n=== 9. Text ===")

check("Append", Text.Append("ab", "c") == "abc")
check("GetLength", Text.GetLength("hello") == 5)
check("IsSubText", Text.IsSubText("hello", "ell") is True)
check("IsSubText not found", Text.IsSubText("hello", "xyz") is False)
check("StartsWith", Text.StartsWith("hello", "he") is True)
check("EndsWith", Text.EndsWith("hello", "lo") is True)
check("GetSubText", Text.GetSubText("hello", 2, 3) == "ell")
check("GetSubTextToEnd", Text.GetSubTextToEnd("hello", 3) == "llo")
check("GetIndexOf found", Text.GetIndexOf("hello", "l") == 3)
check("GetIndexOf not found", Text.GetIndexOf("hello", "x") == 0)
check("ConvertToUpperCase", Text.ConvertToUpperCase("hello") == "HELLO")
check("ConvertToLowerCase", Text.ConvertToLowerCase("HELLO") == "hello")
check("GetCharacter", Text.GetCharacter(65) == "A")
check("GetCharacterCode", Text.GetCharacterCode("A") == 65)

# ====================================================================
# 10. Clock
# ====================================================================
print("\n=== 10. Clock ===")

check("Time is str", isinstance(Clock.Time, str) and ":" in Clock.Time)
check("Date is str", isinstance(Clock.Date, str) and "/" in Clock.Date)
check("Year is int", isinstance(Clock.Year, int) and Clock.Year >= 2024)
check("Month 1..12", 1 <= Clock.Month <= 12)
check("Day 1..31", 1 <= Clock.Day <= 31)
check("Hour 0..23", 0 <= Clock.Hour <= 23)
check("Minute 0..59", 0 <= Clock.Minute <= 59)
check("Second 0..59", 0 <= Clock.Second <= 59)
check("Millisecond 0..999", 0 <= Clock.Millisecond <= 999)
check("WeekDay is str", isinstance(Clock.WeekDay, str) and len(Clock.WeekDay) > 0)
check("ElapsedMilliseconds > 0", Clock.ElapsedMilliseconds > 0)

# ====================================================================
# 11. Array
# ====================================================================
print("\n=== 11. Array ===")

Array.SetValue("test", "name", "Alice")
check("SetValue/GetValue", Array.GetValue("test", "name") == "Alice")
check("ContainsIndex", Array.ContainsIndex("test", "name") is True)
check("ContainsIndex missing", Array.ContainsIndex("test", "age") is False)
check("ContainsValue", Array.ContainsValue("test", "Alice") is True)
check("ContainsValue missing", Array.ContainsValue("test", "Bob") is False)
check("GetItemCount", Array.GetItemCount("test") >= 1)
check("IsArray dict", Array.IsArray({"a": 1}) is True)
check("IsArray list", Array.IsArray([1, 2]) is True)
check("IsArray str", Array.IsArray("hello") is False)
arr = Array.GetAllIndices("test")
check("GetAllIndices returns dict", isinstance(arr, dict))
Array.RemoveValue("test", "name")
check("RemoveValue", Array.ContainsIndex("test", "name") is False)

# ====================================================================
# 12. Stack
# ====================================================================
print("\n=== 12. Stack ===")

Stack.PushValue("s1", "first")
Stack.PushValue("s1", "second")
check("PopValue LIFO", Stack.PopValue("s1") == "second")
check("PopValue second", Stack.PopValue("s1") == "first")
check("PopValue empty", Stack.PopValue("s1") == "")
check("GetCount empty", Stack.GetCount("s1") == 0)
Stack.PushValue("s1", "a")
check("GetCount 1", Stack.GetCount("s1") == 1)
Stack.PopValue("s1")

# ====================================================================
# 13. TextWindow
# ====================================================================
print("\n=== 13. TextWindow ===")

check("Show", (TextWindow.Show(), True)[1])
TextWindow.Title = "Test"
check("Title get", TextWindow.Title == "Test")
TextWindow.Title = "Python Small Basic"
TextWindow.ForegroundColor = "Red"
check("ForegroundColor get", TextWindow.ForegroundColor == "Red")
TextWindow.ForegroundColor = "White"
TextWindow.BackgroundColor = "Blue"
check("BackgroundColor get", TextWindow.BackgroundColor == "Blue")
TextWindow.BackgroundColor = "DarkBlue"
TextWindow.Write("a"); TextWindow.WriteLine("b")
check("Write/Writeline", True)
check("Clear", (TextWindow.Clear(), True)[1])
check("Hide", (TextWindow.Hide(), True)[1])

# ====================================================================
# 14. Mouse
# ====================================================================
print("\n=== 14. Mouse ===")

check("MouseX is int", isinstance(Mouse.MouseX, int))
check("MouseY is int", isinstance(Mouse.MouseY, int))
check("IsLeftButtonDown is bool", isinstance(Mouse.IsLeftButtonDown, bool))
check("IsRightButtonDown is bool", isinstance(Mouse.IsRightButtonDown, bool))
old_x, old_y = Mouse.MouseX, Mouse.MouseY
Mouse.MouseX = 500
Mouse.MouseY = 400
check("MouseX set", Mouse.MouseX == 500)
check("MouseY set", Mouse.MouseY == 400)
Mouse.MouseX, Mouse.MouseY = old_x, old_y
check("HideCursor", (Mouse.HideCursor(), True)[1])
check("ShowCursor", (Mouse.ShowCursor(), True)[1])

# ====================================================================
# 15. Sound
# ====================================================================
print("\n=== 15. Sound ===")

check("PlayClick", (Sound.PlayClick(), True)[1])
check("PlayChime", (Sound.PlayChime(), True)[1])
check("PlayBellRing", (Sound.PlayBellRing(), True)[1])
check("PlayChimes", (Sound.PlayChimes(), True)[1])

# ====================================================================
# 16. File
# ====================================================================
print("\n=== 16. File ===")

tmp = File.GetTemporaryFilePath()
r = File.WriteContents(tmp, "Hello World")
check("WriteContents", r == "SUCCESS")
check("ReadContents", File.ReadContents(tmp) == "Hello World")
r = File.AppendContents(tmp, "!")
check("AppendContents", File.ReadContents(tmp) == "Hello World!")
r = File.CopyFile(tmp, tmp + ".bak")
check("CopyFile", r == "SUCCESS")
check("GetFiles returns dict", isinstance(File.GetFiles("."), dict))
check("GetSettingsFilePath", isinstance(File.GetSettingsFilePath(), str))
r = File.DeleteFile(tmp + ".bak")
check("DeleteFile", r == "SUCCESS")
r = File.DeleteFile(tmp)
check("DeleteFile original", r == "SUCCESS")

# Directory ops
test_dir = "_test_sb_dir"
File.CreateDirectory(test_dir)
check("CreateDirectory", os.path.isdir(test_dir))
File.DeleteDirectory(test_dir)
check("DeleteDirectory", not os.path.exists(test_dir))

# ====================================================================
# 17. Network (skip if offline)
# ====================================================================
print("\n=== 17. Network ===")

try:
    html = Network.GetWebPageContents("https://httpbin.org/get")
    check("GetWebPageContents", len(html) > 0)
except Exception:
    print("  SKIP Network (offline)")

# ====================================================================
# 18. Dictionary (skip if offline)
# ====================================================================
print("\n=== 18. Dictionary ===")

try:
    defn = Dictionary.GetDefinition("hello")
    check("GetDefinition", len(defn) > 0)
except Exception:
    print("  SKIP Dictionary (offline)")

# ====================================================================
# 19. Timer (non-blocking)
# ====================================================================
print("\n=== 19. Timer ===")

ticks = []
def on_tick():
    ticks.append(1)
Timer.Interval = 100
Timer.Tick = on_tick
time.sleep(0.35)
Timer.Pause()
check("Timer ticked 2-5 times", 2 <= len(ticks) <= 6)
Timer.Tick = None

# ====================================================================
# 20. Shapes
# ====================================================================
print("\n=== 20. Shapes ===")

try:
    GraphicsWindow.Show()
    s_rect = Shapes.AddRectangle(100, 50)
    check("AddRectangle returns str", isinstance(s_rect, str))
    check("GetLeft initial", Shapes.GetLeft(s_rect) == 0)
    check("GetTop initial", Shapes.GetTop(s_rect) == 0)
    Shapes.Move(s_rect, 50, 50)
    check("Move", Shapes.GetLeft(s_rect) == 50 and Shapes.GetTop(s_rect) == 50)

    s_ell = Shapes.AddEllipse(80, 60)
    check("AddEllipse", isinstance(s_ell, str))
    s_tri = Shapes.AddTriangle(0, 0, 50, 50, 100, 0)
    check("AddTriangle", isinstance(s_tri, str))
    s_line = Shapes.AddLine(10, 10, 100, 10)
    check("AddLine", isinstance(s_line, str))
    s_text = Shapes.AddText("Shape Text")
    check("AddText", isinstance(s_text, str))

    Shapes.SetText(s_text, "Updated")
    check("SetText", True)
    Shapes.Rotate(s_rect, 45)
    check("Rotate", True)
    Shapes.SetOpacity(s_rect, 50)
    check("SetOpacity 50", Shapes.GetOpacity(s_rect) == 50)
    Shapes.SetOpacity(s_rect, 100)
    Shapes.HideShape(s_rect)
    check("HideShape", True)
    Shapes.ShowShape(s_rect)
    check("ShowShape", True)
    Shapes.Zoom(s_ell, 1.5, 1.5)
    check("Zoom", True)
    Shapes.Remove(s_text)
    check("Remove", True)

    # Animate (non-blocking smoke test with very short duration)
    Shapes.Animate(s_rect, 100, 100, 50)
    check("Animate", True)

    GraphicsWindow.Hide()
except Exception as e:
    check("Shapes", False, str(e))
    GraphicsWindow.Hide()

# ====================================================================
# 21. Turtle
# ====================================================================
print("\n=== 21. Turtle ===")

check("Speed default 5", Turtle.Speed == 5)
Turtle.Speed = 5
check("Speed set", Turtle.Speed == 5)
check("Angle default", isinstance(Turtle.Angle, float))
check("X default", isinstance(Turtle.X, float))
check("Y default", isinstance(Turtle.Y, float))

# Non-visible turtle operations (no canvas needed)
old_x, old_y = Turtle.X, Turtle.Y
Turtle.Turn(90)
check("Turn 90", abs(Turtle.Angle - 90) < 0.01)
Turtle.TurnRight()
check("TurnRight (back to 0)", abs(Turtle.Angle) < 0.01)
Turtle.TurnLeft()
check("TurnLeft", abs(Turtle.Angle - 90) < 0.01)
Turtle.Angle = 0
Turtle.PenDown()
check("PenDown", True)
Turtle.PenUp()
check("PenUp", True)

Turtle.Hide()
check("Turtle.Hide", True)

# ====================================================================
# 22. Controls
# ====================================================================
print("\n=== 22. Controls ===")

try:
    GraphicsWindow.Show()
    btn = Controls.AddButton("Test", 10, 10)
    tb = Controls.AddTextBox(10, 50)
    mtb = Controls.AddMultiLineTextBox(10, 90)

    check("AddButton returns str", isinstance(btn, str))
    check("AddTextBox returns str", isinstance(tb, str))
    check("AddMultiLineTextBox returns str", isinstance(mtb, str))

    Controls.SetTextBoxText(tb, "Hello")
    check("SetTextBoxText/GetTextBoxText", Controls.GetTextBoxText(tb) == "Hello")

    Controls.SetButtonCaption(btn, "Clicked!")
    check("SetButtonCaption/GetButtonCaption", Controls.GetButtonCaption(btn) == "Clicked!")

    Controls.SetSize(btn, 80, 25)
    check("SetSize", True)
    Controls.Move(btn, 20, 20)
    check("Move", True)

    Controls.HideControl(btn)
    check("HideControl", True)
    Controls.ShowControl(btn)
    check("ShowControl", True)

    Controls.Remove(btn)
    check("Remove", True)

    GraphicsWindow.Hide()
except Exception as e:
    check("Controls", False, str(e))
    GraphicsWindow.Hide()

# ====================================================================
# 23. Desktop
# ====================================================================
print("\n=== 23. Desktop ===")

check("Desktop.Width > 0", Desktop.Width > 0)
check("Desktop.Height > 0", Desktop.Height > 0)

# ====================================================================
# 24. ImageList
# ====================================================================
print("\n=== 24. ImageList ===")

check("LoadImage missing returns ''", ImageList.LoadImage("_nonexistent_.png") == "")
check("GetWidthOfImage missing", ImageList.GetWidthOfImage("_nonexistent_") == 0)
check("GetHeightOfImage missing", ImageList.GetHeightOfImage("_nonexistent_") == 0)

# ====================================================================
# 25. Keywords
# ====================================================================
print("\n=== 25. Keywords ===")

check("Keywords docstring exists", Keywords.__doc__ is not None and len(Keywords.__doc__) > 0)

# ====================================================================
# 26. Integration — state persist across modules
# ====================================================================
print("\n=== 26. Integration ===")

GraphicsWindow.PenColor = "Green"
GraphicsWindow.PenWidth = 4
check("Shapes reads GState.pen_color",
      GraphicsState.pen_color == "Green")
check("Shapes reads GState.pen_width",
      GraphicsState.pen_width == 4)
GraphicsWindow.PenColor = "Black"
GraphicsWindow.PenWidth = 2

GraphicsWindow.FontBold = True
check("FontBold in GState", GraphicsState.font_bold is True)
GraphicsWindow.FontBold = False

# ====================================================================
# Summary
# ====================================================================
print("\n" + "=" * 60)
total = passed + failed
print(f"  {passed} / {total} checks passed ({failed} failed)")
if failed:
    print("  *** SOME TESTS FAILED ***")
    sys.exit(1)
else:
    print("  ALL TESTS PASSED")
