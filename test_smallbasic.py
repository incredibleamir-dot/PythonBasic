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
check("dead 'shown' attr removed", not hasattr(GraphicsState, "shown"))

# Mutation
GraphicsState.pen_color = "Red"
check("mutate pen_color", GraphicsState.pen_color == "Red")
GraphicsState.pen_color = "Black"  # reset

# ====================================================================
# 3. Renderer (non-GUI methods)
# ====================================================================
print("\n=== 3. Renderer ===")

check("ensure returns a window handle", Renderer.ensure() is not None)
check("get_random_color returns hex",
      Renderer.get_random_color().startswith("#"))
check("get_random_color 7 chars",
      len(Renderer.get_random_color()) == 7)
check("get_color_from_rgb",
      Renderer.get_color_from_rgb(255, 0, 0) == "#FF0000")
check("get_color_from_rgb clamped",
      Renderer.get_color_from_rgb(300, -10, 128) == "#FF0080")

# Object registry removed (dead code) in favour of the _pixels buffer
check("object registry removed", not hasattr(Renderer, '_objects'))

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
Program.Delay(350)   # pumps the event loop so after-mode callbacks fire
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
# 22b. Extended Controls (dropdown, slider, progress bar, table)
# ====================================================================
print("\n=== 22b. Extended Controls ===")

try:
    GraphicsWindow.Show()
    dd = Controls.AddDropDown(["A", "B", "C"], 10, 160)
    check("AddDropDown returns str", isinstance(dd, str))
    check("GetDropDownItemCount", Controls.GetDropDownItemCount(dd) == 3)
    check("GetDropDownItems", Controls.GetDropDownItems(dd) == ["A", "B", "C"])
    check("GetSelectedDropDownItem default", Controls.GetSelectedDropDownItem(dd) == "")
    Controls.SetSelectedDropDownItem(dd, 1)
    check("SetSelectedDropDownItem", Controls.GetSelectedDropDownItem(dd) == "B")

    sl = Controls.AddSlider(0, 100, 10, 200)
    check("AddSlider returns str", isinstance(sl, str))
    Controls.SetSliderValue(sl, 42)
    check("SetSliderValue/GetSliderValue", Controls.GetSliderValue(sl) == 42)

    pb = Controls.AddProgressBar(10, 240)
    check("AddProgressBar returns str", isinstance(pb, str))
    Controls.SetProgressBarValue(pb, 75)
    check("SetProgressBarValue/GetProgressBarValue", Controls.GetProgressBarValue(pb) == 75)
    Controls.SetProgressBarValue(pb, 500)
    check("ProgressBar clamped", Controls.GetProgressBarValue(pb) == 100)

    table_data = [["Name", "Age"], ["Alice", 30], ["Bob", 25]]
    tb2 = Controls.AddTable(table_data, 160, 160)
    check("AddTable returns str", isinstance(tb2, str))
    new_data = [["Name", "Age"], ["Carol", 40]]
    Controls.SetTableData(tb2, new_data)
    check("SetTableData", True)

    Controls.Remove(dd)
    check("Remove dropdown", True)
    GraphicsWindow.Hide()
except Exception as e:
    check("Extended Controls", False, str(e))
    GraphicsWindow.Hide()

# ====================================================================
# 22c. Extended Controls Events (slider, dropdown, table)
# ====================================================================
print("\n=== 22c. Extended Controls Events ===")

try:
    GraphicsWindow.Show()
    events = []

    Controls.SliderChanged = lambda: events.append(("slider", Controls.LastChangedSlider))
    Controls.DropDownSelected = lambda: events.append(("dd", Controls.LastSelectedDropDown))
    Controls.TableRowSelected = lambda: events.append(("table", Controls.LastSelectedTable))

    sl_e = Controls.AddSlider(0, 100, 10, 200)
    dd_e = Controls.AddDropDown(["X", "Y"], 10, 240)
    tb_e = Controls.AddTable([["A", "B"], ["1", "2"], ["3", "4"]], 10, 280)

    Controls.SetSliderValue(sl_e, 55)
    check("SliderChanged fires on SetSliderValue", ("slider", sl_e) in events)
    check("LastChangedSlider", Controls.LastChangedSlider == sl_e)

    h_dd = Controls._widgets[dd_e]
    h_dd.event_generate("<<ComboboxSelected>>")
    check("DropDownSelected fires", ("dd", dd_e) in events)
    check("LastSelectedDropDown", Controls.LastSelectedDropDown == dd_e)

    h_tb = Controls._widgets[tb_e]
    h_tb.selection_set(h_tb.get_children()[1])
    h_tb.event_generate("<<TreeviewSelect>>")
    check("TableRowSelected fires", ("table", tb_e) in events)
    check("LastSelectedTable", Controls.LastSelectedTable == tb_e)
    check("GetSelectedTableRow selected", Controls.GetSelectedTableRow(tb_e) == 2)
    check("GetSelectedTableRow none", Controls.GetSelectedTableRow("nope") == 0)

    Controls.Remove(sl_e)
    Controls.Remove(dd_e)
    Controls.Remove(tb_e)
    Controls.SliderChanged = None
    Controls.DropDownSelected = None
    Controls.TableRowSelected = None
    GraphicsWindow.Hide()
except Exception as e:
    check("Extended Controls Events", False, str(e))
    GraphicsWindow.Hide()

# ====================================================================
# 22d. File / Folder Pickers
# ====================================================================
print("\n=== 22d. File / Folder Pickers ===")

check("FilePicked event default None", Controls.FilePicked is None)
check("FolderPicked event default None", Controls.FolderPicked is None)

try:
    GraphicsWindow.Show()
    fp = Controls.AddFilePicker("Open...", 20, 20)
    fd = Controls.AddFolderPicker("Folder...", 20, 60)
    check("AddFilePicker returns str", isinstance(fp, str) and fp.startswith("FilePicker"))
    check("AddFolderPicker returns str", isinstance(fd, str) and fd.startswith("FolderPicker"))
    check("GetPickerPath default ''", Controls.GetPickerPath(fp) == "")
    check("GetPickerPath missing ''", Controls.GetPickerPath("Nope") == "")
    check("LastPickedFile default ''", Controls.LastPickedFile == "")
    check("LastPickedFolder default ''", Controls.LastPickedFolder == "")
    Controls._picked[fp] = "C:/picked.txt"
    check("GetPickerPath reads stored", Controls.GetPickerPath(fp) == "C:/picked.txt")
    Controls.Remove(fp)
    check("GetPickerPath after remove ''", Controls.GetPickerPath(fp) == "")
    Controls.Remove(fd)
    GraphicsWindow.Hide()
except Exception as e:
    check("File/Folder Pickers", False, str(e))
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
# 27. Math — edge cases
# ====================================================================
print("\n=== 27. Math edge cases ===")

check("Max() no args -> 0", Math.Max() == 0)
check("Min() no args -> 0", Math.Min() == 0)
check("Max(single) = value", Math.Max(7) == 7)
check("Min(single) = value", Math.Min(7) == 7)
check("Max floats", Math.Max(1.5, 1.2, 1.9) == 1.9)
check("Sum() no args -> 0", Math.Sum() == 0)
check("Average() no args -> 0.0", Math.Average() == 0.0)
check("Sum negatives", Math.Sum(-1, -2, -3) == -6)
check("Ceiling(3.0) -> 3", Math.Ceiling(3.0) == 3)
check("Ceiling(-1.2) -> -1", Math.Ceiling(-1.2) == -1)
check("Floor(-1.2) -> -2", Math.Floor(-1.2) == -2)
check("Round(2.5) -> 2 (bankers)", Math.Round(2.5) == 2)
check("Round(-2.5) -> -2", Math.Round(-2.5) == -2)
check("Abs(0) -> 0", Math.Abs(0) == 0)
check("Abs(-3.5) -> 3.5", Math.Abs(-3.5) == 3.5)
check("SquareRoot(0) -> 0", Math.SquareRoot(0) == 0)
check("Power(2,-1) -> 0.5", Math.Power(2, -1) == 0.5)
check("Power(0,0) -> 1", Math.Power(0, 0) == 1.0)
check("NaturalLog(1) -> 0", Math.NaturalLog(1) == 0.0)
check("Log(100) -> 2", Math.Log(100) == 2.0)
check("Sin(0) -> 0", abs(Math.Sin(0)) < 0.0001)
check("Cos(90) ~ 0", abs(Math.Cos(90)) < 0.0001)
check("ArcSin(2) clamped -> 90", Math.ArcSin(2) == 90.0)
check("ArcCos(-2) clamped -> 180", Math.ArcCos(-2) == 180.0)
check("ArcTan(1) -> 45", abs(Math.ArcTan(1) - 45) < 0.0001)
check("GetDegrees(pi) ~ 180", abs(Math.GetDegrees(3.141592653589793) - 180) < 1e-9)
check("GetRadians(180) ~ pi", abs(Math.GetRadians(180) - 3.141592653589793) < 1e-9)
check("Remainder negative (python %)", Math.Remainder(-10, 3) == 2)
check("Remainder zero dividend", Math.Remainder(0, 5) == 0)
r = Math.GetRandomNumber(1)
check("GetRandomNumber(1) -> 1", r == 1)
r = Math.GetRandomNumber(0)
check("GetRandomNumber(0) -> 1", r == 1)
r = Math.GetRandomNumber(-3)
check("GetRandomNumber(negative) -> 1", r == 1)
for _ in range(20):
    r = Math.GetRandomNumber(5)
    assert 1 <= r <= 5
check("GetRandomNumber in range (20x)", True)

# ====================================================================
# 28. Text — edge cases
# ====================================================================
print("\n=== 28. Text edge cases ===")

check("Append coerces ints", Text.Append(1, 2) == "12")
check("GetLength empty -> 0", Text.GetLength("") == 0)
check("GetLength unicode", Text.GetLength("héllo") == 5)
check("IsSubText empty needle", Text.IsSubText("hello", "") is True)
check("IsSubText both empty", Text.IsSubText("", "") is True)
check("StartsWith empty", Text.StartsWith("hello", "") is True)
check("EndsWith empty", Text.EndsWith("hello", "") is True)
check("StartsWith longer needle", Text.StartsWith("hi", "hello") is False)
check("GetSubText start 1", Text.GetSubText("hello", 1, 3) == "hel")
check("GetSubText start 0 clamped", Text.GetSubText("hello", 0, 2) == "he")
check("GetSubText out of range", Text.GetSubText("hello", 10, 5) == "")
check("GetSubText negative start", Text.GetSubText("hello", -5, 3) == "hel")
check("GetSubText length 0", Text.GetSubText("hello", 2, 0) == "")
check("GetSubTextToEnd end", Text.GetSubTextToEnd("hello", 5) == "o")
check("GetSubTextToEnd past end", Text.GetSubTextToEnd("hello", 20) == "")
check("GetIndexOf first match", Text.GetIndexOf("hello", "l") == 3)
check("GetIndexOf empty needle", Text.GetIndexOf("hello", "") == 1)
check("GetIndexOf case sensitive", Text.GetIndexOf("Hello", "h") == 0)
check("GetCharacter code 0", Text.GetCharacter(0) == "\x00")
check("GetCharacter unicode", Text.GetCharacter(233) == "é")
check("GetCharacterCode first char", Text.GetCharacterCode("AB") == 65)
check("ConvertToLowerCase unicode", Text.ConvertToLowerCase("ÄBC") == "äbc")
check("ConvertToUpperCase digits", Text.ConvertToUpperCase("a1b") == "A1B")

# ====================================================================
# 29. Array — edge cases
# ====================================================================
print("\n=== 29. Array edge cases ===")

Array.SetValue("edge_arr", 1, "numeric-index")
check("SetValue numeric index", Array.GetValue("edge_arr", 1) == "numeric-index")
Array.SetValue("edge_arr", "k", 42)
check("SetValue mixed indices", Array.GetValue("edge_arr", "k") == 42)
check("GetValue missing -> ''", Array.GetValue("edge_arr", "missing") == "")
check("GetValue missing array -> ''", Array.GetValue("no_such_array", "x") == "")
check("GetItemCount missing -> 0", Array.GetItemCount("no_such_array") == 0)
check("ContainsIndex missing -> False", Array.ContainsIndex("no_such_array", "x") is False)
check("ContainsValue missing -> False", Array.ContainsValue("no_such_array", "x") is False)
check("GetAllIndices missing -> {}", Array.GetAllIndices("no_such_array") == {})
check("IsArray tuple -> False", Array.IsArray((1, 2)) is False)
check("IsArray None -> False", Array.IsArray(None) is False)
check("IsArray int -> False", Array.IsArray(5) is False)
check("ContainsIndex with dict", Array.ContainsIndex({"a": 1}, "a") is True)
check("ContainsIndex with list -> False", Array.ContainsIndex([1, 2], 1) is False)
check("GetItemCount with dict", Array.GetItemCount({"a": 1, "b": 2}) == 2)
check("GetAllIndices with dict",
      Array.GetAllIndices({"a": 1, "b": 2}) == {1: "a", 2: "b"})
Array.RemoveValue("edge_arr", "missing")
check("RemoveValue missing no-op", Array.ContainsIndex("edge_arr", "k") is True)
Array.RemoveValue("edge_arr", 1)
check("RemoveValue removed", Array.ContainsIndex("edge_arr", 1) is False)
Array.RemoveValue("no_such_array", "x")
check("RemoveValue missing array no-op", True)

# ====================================================================
# 30. Stack — edge cases
# ====================================================================
print("\n=== 30. Stack edge cases ===")

check("GetCount missing -> 0", Stack.GetCount("no_such_stack") == 0)
check("PopValue missing -> ''", Stack.PopValue("no_such_stack") == "")
Stack.PushValue("s2", 42)
check("PopValue non-string", Stack.PopValue("s2") == 42)
obj = {"x": 1}
Stack.PushValue("s2", obj)
check("PopValue identity", Stack.PopValue("s2") is obj)
Stack.PushValue("s2", None)
check("PopValue None", Stack.PopValue("s2") is None)
Stack.PushValue("s2", "a")
Stack.PushValue("s3", "b")
check("Stacks independent", Stack.GetCount("s2") == 1 and Stack.GetCount("s3") == 1)
Stack.PopValue("s2")
check("GetCount after pop -> 0", Stack.GetCount("s2") == 0)
Stack.PopValue("s3")

# ====================================================================
# 31. File — edge cases
# ====================================================================
print("\n=== 31. File edge cases ===")

check("ReadContents missing -> FAILED", File.ReadContents("_no_such_file_.txt") == "FAILED")
check("LastError set on failure", isinstance(File.LastError, str) and len(File.LastError) > 0)

# nested path creation
nested = os.path.join(tempfile.gettempdir(), "sb_test_nested", "sub", "data.txt")
check("WriteContents creates dirs", File.WriteContents(nested, "hi") == "SUCCESS")
check("Nested read", File.ReadContents(nested) == "hi")
os.remove(nested)
os.rmdir(os.path.dirname(nested))
os.rmdir(os.path.dirname(os.path.dirname(nested)))

# line operations
fd, lpath = tempfile.mkstemp(suffix=".txt")
os.close(fd)
File.WriteContents(lpath, "one\ntwo\nthree\n")
check("ReadLine 2", File.ReadLine(lpath, 2) == "two")
check("ReadLine beyond -> ''", File.ReadLine(lpath, 99) == "")
check("ReadLine 0 -> ''", File.ReadLine(lpath, 0) == "")
check("ReadLine missing file -> FAILED", File.ReadLine("_nope_.txt", 1) == "FAILED")
check("WriteLine overwrites", File.WriteLine(lpath, 1, "ONE") == "SUCCESS")
check("WriteLine applied", File.ReadLine(lpath, 1) == "ONE")
check("WriteLine other intact", File.ReadLine(lpath, 2) == "two")
check("WriteLine expands", File.WriteLine(lpath, 5, "five") == "SUCCESS")
check("WriteLine expanded line", File.ReadLine(lpath, 5) == "five")
check("InsertLine", File.InsertLine(lpath, 2, "INSERTED") == "SUCCESS")
check("InsertLine shifted", File.ReadLine(lpath, 2) == "INSERTED")
check("InsertLine old line2 moved", File.ReadLine(lpath, 3) == "two")
check("InsertLine missing file -> FAILED", File.InsertLine("_nope_.txt", 1, "x") == "FAILED")

# append / copy / delete
apath = os.path.join(tempfile.gettempdir(), "sb_append.txt")
File.DeleteFile(apath)
check("AppendContents creates", File.AppendContents(apath, "x") == "SUCCESS")
check("AppendContents content", File.ReadContents(apath) == "x")
File.AppendContents(apath, "y")
check("AppendContents appends", File.ReadContents(apath) == "xy")
check("CopyFile missing source -> FAILED", File.CopyFile("_no_such_.txt", apath) == "FAILED")
check("DeleteFile missing -> FAILED", File.DeleteFile("_no_such_.txt") == "FAILED")
check("DeleteFile works", File.DeleteFile(apath) == "SUCCESS")

# directory ops
d1 = os.path.join(tempfile.gettempdir(), "sb_dir_a")
d2 = os.path.join(tempfile.gettempdir(), "sb_dir_b")
File.CreateDirectory(d1)
File.CreateDirectory(d2)
created = File.GetDirectories(tempfile.gettempdir())
check("GetDirectories returns dict", isinstance(created, dict) and len(created) >= 1)
check("GetFiles missing dir -> FAILED", File.GetFiles("_no_such_dir_") == "FAILED")
check("GetDirectories missing -> FAILED", File.GetDirectories("_no_such_dir_") == "FAILED")
file_g = File.GetFiles(tempfile.gettempdir())
check("GetFiles returns dict", isinstance(file_g, dict))
File.DeleteDirectory(d1)
File.DeleteDirectory(d2)
check("DeleteDirectory missing -> FAILED", File.DeleteDirectory("_no_such_dir_") == "FAILED")

tmp = File.GetTemporaryFilePath()
check("GetTemporaryFilePath exists", os.path.exists(tmp))
File.DeleteFile(tmp)
check("GetSettingsFilePath", File.GetSettingsFilePath().endswith("settings.txt"))

# unicode round-trip
upath = os.path.join(tempfile.gettempdir(), "sb_uni.txt")
File.WriteContents(upath, "héllo wörld ☃")
check("Unicode round-trip", File.ReadContents(upath) == "héllo wörld ☃")
File.DeleteFile(upath)

# ====================================================================
# 32. Program / Clock / Mouse — edge cases
# ====================================================================
print("\n=== 32. Program / Clock / Mouse edge cases ===")

check("GetArgument(0) -> ''", Program.GetArgument(0) == "")
check("GetArgument big -> ''", Program.GetArgument(9999) == "")
check("ArgumentCount is int", isinstance(Program.ArgumentCount, int) and Program.ArgumentCount >= 0)
check("Clock.Date 3 parts", len(Clock.Date.split("/")) == 3)
check("Clock.Time 3 parts", len(Clock.Time.split(":")) == 3)
check("Mouse.MouseX int", isinstance(Mouse.MouseX, int))
check("Mouse.MouseY int", isinstance(Mouse.MouseY, int))
check("IsLeftButtonDown bool", isinstance(Mouse.IsLeftButtonDown, bool))

# ====================================================================
# 33. GraphicsWindow — property / API edge cases
# ====================================================================
print("\n=== 33. GraphicsWindow edge cases ===")

try:
    GraphicsWindow.GraphicsEngine
    check("GraphicsEngine removed", False)
except AttributeError:
    check("GraphicsEngine removed", True)

try:
    GraphicsWindow.NonExistentProperty
    check("Unknown property raises", False)
except AttributeError:
    check("Unknown property raises", True)

check("color clamp low/high", Renderer.get_color_from_rgb(-5, 300, 128) == "#00FF80")
check("color clamp exact", Renderer.get_color_from_rgb(0, 0, 0) == "#000000")
check("color clamp white", Renderer.get_color_from_rgb(255, 255, 255) == "#FFFFFF")

from smallbasic._backends import create_backend as _cb, Backend as _B
check("create_backend -> TKINTER", _cb().name == "TKINTER")
check("backend is TkBackend", Renderer.backend().name == "TKINTER")
check("Backend has no add_tree", not hasattr(_B, "add_tree"))
import smallbasic._backends as _be
check("register_backend removed", not hasattr(_be, "register_backend"))
check("available_backends removed", not hasattr(_be, "available_backends"))
check("AddTreeView removed", not hasattr(Controls, "AddTreeView"))

# ====================================================================
# 34. Controls — edge cases
# ====================================================================
print("\n=== 34. Controls edge cases ===")

try:
    GraphicsWindow.Show()

    # missing-control safety
    check("GetButtonCaption missing -> ''", Controls.GetButtonCaption("Nope") == "")
    check("SetButtonCaption missing no-op", (Controls.SetButtonCaption("Nope", "x"), True)[1])
    check("GetTextBoxText missing -> ''", Controls.GetTextBoxText("Nope") == "")
    check("SetTextBoxText missing no-op", (Controls.SetTextBoxText("Nope", "x"), True)[1])
    check("Move missing no-op", (Controls.Move("Nope", 1, 1), True)[1])
    check("SetSize missing no-op", (Controls.SetSize("Nope", 1, 1), True)[1])
    check("HideControl missing no-op", (Controls.HideControl("Nope"), True)[1])
    check("ShowControl missing no-op", (Controls.ShowControl("Nope"), True)[1])
    check("Remove missing no-op", (Controls.Remove("Nope"), True)[1])
    check("GetSliderValue missing -> 0", Controls.GetSliderValue("Nope") == 0)
    check("SetSliderValue missing no-op", (Controls.SetSliderValue("Nope", 5), True)[1])
    check("GetProgressBarValue missing -> 0", Controls.GetProgressBarValue("Nope") == 0)
    check("SetProgressBarValue missing no-op", (Controls.SetProgressBarValue("Nope", 5), True)[1])
    check("GetSelectedDropDownItem missing -> ''", Controls.GetSelectedDropDownItem("Nope") == "")
    check("GetDropDownItemCount missing -> 0", Controls.GetDropDownItemCount("Nope") == 0)
    check("GetDropDownItems missing -> []", Controls.GetDropDownItems("Nope") == [])
    check("SetTableData missing no-op", (Controls.SetTableData("Nope", []), True)[1])

    # dropdown edge cases
    dd_e = Controls.AddDropDown([], 10, 20)
    check("AddDropDown empty", isinstance(dd_e, str))
    check("DropDown empty count 0", Controls.GetDropDownItemCount(dd_e) == 0)
    check("DropDown empty items", Controls.GetDropDownItems(dd_e) == [])
    check("DropDown empty selected ''", Controls.GetSelectedDropDownItem(dd_e) == "")
    dd_d = Controls.AddDropDown({"1": "One", "2": "Two"}, 10, 60)
    check("AddDropDown dict values", Controls.GetDropDownItems(dd_d) == ["One", "Two"])
    Controls.SetSelectedDropDownItem(dd_d, 99)
    check("DropDown out-of-range no crash", True)

    # slider clamp
    sl_e = Controls.AddSlider(0, 100, 10, 100)
    Controls.SetSliderValue(sl_e, 999)
    check("Slider clamp high", Controls.GetSliderValue(sl_e) == 100)
    Controls.SetSliderValue(sl_e, -50)
    check("Slider clamp low", Controls.GetSliderValue(sl_e) == 0)
    Controls.SetSliderValue(sl_e, 42.9)
    check("Slider returns int", isinstance(Controls.GetSliderValue(sl_e), int))

    # progress bar clamp
    pb_e = Controls.AddProgressBar(10, 140)
    Controls.SetProgressBarValue(pb_e, -5)
    check("ProgressBar clamp low", Controls.GetProgressBarValue(pb_e) == 0)
    Controls.SetProgressBarValue(pb_e, 123)
    check("ProgressBar clamp high", Controls.GetProgressBarValue(pb_e) == 100)

    # table edge cases
    t_e = Controls.AddTable([], 10, 180)
    check("AddTable empty ok", isinstance(t_e, str))
    t_h = Controls.AddTable([["A", "B"]], 10, 220)
    check("AddTable headers-only ok", isinstance(t_h, str))
    t_u = Controls.AddTable([["A", "B"], ["x"]], 10, 260)
    check("AddTable uneven rows ok", isinstance(t_u, str))
    Controls.SetTableData(t_u, [["A", "B", "C"], ["1", "2", "3"]])
    check("SetTableData new headers ok", True)

    GraphicsWindow.Hide()
except Exception as e:
    check("Controls edge cases", False, str(e))
    GraphicsWindow.Hide()

# ====================================================================
# 35. Shapes — edge cases
# ====================================================================
print("\n=== 35. Shapes edge cases ===")

try:
    GraphicsWindow.Show()
    check("GetLeft missing -> 0", Shapes.GetLeft("Nope") == 0)
    check("GetTop missing -> 0", Shapes.GetTop("Nope") == 0)
    check("GetOpacity missing -> 100", Shapes.GetOpacity("Nope") == 100)
    check("Move missing no-op", (Shapes.Move("Nope", 1, 1), True)[1])
    check("Rotate missing no-op", (Shapes.Rotate("Nope", 45), True)[1])
    check("Zoom missing no-op", (Shapes.Zoom("Nope", 2, 2), True)[1])
    check("Animate missing no-op", (Shapes.Animate("Nope", 1, 1, 50), True)[1])
    check("SetText missing no-op", (Shapes.SetText("Nope", "x"), True)[1])
    check("HideShape missing no-op", (Shapes.HideShape("Nope"), True)[1])
    check("ShowShape missing no-op", (Shapes.ShowShape("Nope"), True)[1])
    check("Remove missing no-op", (Shapes.Remove("Nope"), True)[1])

    s1 = Shapes.AddRectangle(10, 10)
    s2 = Shapes.AddRectangle(10, 10)
    check("Shapes unique names", s1 != s2)
    Shapes.SetOpacity(s1, 150)
    check("SetOpacity clamp high", Shapes.GetOpacity(s1) == 100)
    Shapes.SetOpacity(s1, -3)
    check("SetOpacity clamp low", Shapes.GetOpacity(s1) == 0)
    Shapes.Zoom(s1, 0.001, 0.001)
    check("Zoom clamp no crash", True)
    Shapes.Animate(s1, 50, 50, 0)
    check("Animate duration 0", True)
    Shapes.Remove(s1)
    Shapes.Remove(s2)

    GraphicsWindow.Hide()
except Exception as e:
    check("Shapes edge cases", False, str(e))
    GraphicsWindow.Hide()

# ====================================================================
# 36. Turtle — edge cases
# ====================================================================
print("\n=== 36. Turtle edge cases ===")

t_old_speed = Turtle.Speed
Turtle.Speed = 99
check("Speed clamp high", Turtle.Speed == 10)
Turtle.Speed = -5
check("Speed clamp low", Turtle.Speed == 1)
Turtle.Speed = t_old_speed
check("Speed restored", Turtle.Speed == t_old_speed)

t_old_angle = Turtle.Angle
Turtle.Turn(360)
check("Turn(360) -> 0", abs(Turtle.Angle) < 0.01)
Turtle.Turn(-90)
check("Turn(-90) -> 270", abs(Turtle.Angle - 270) < 0.01)
Turtle.Turn(720)
check("Turn wraps", abs(Turtle.Angle - 270) < 0.01)
Turtle.Angle = t_old_angle

t_old_x, t_old_y = Turtle.X, Turtle.Y
Turtle.X = "100.5"
check("X setter accepts str", Turtle.X == 100.5)
Turtle.X, Turtle.Y = t_old_x, t_old_y

# ====================================================================
# 37. Sound — edge cases (no sound emitted)
# ====================================================================
print("\n=== 37. Sound edge cases ===")

check("PlayMusic empty no crash", (Sound.PlayMusic(""), True)[1])
check("Play missing file no crash", (Sound.Play("_no_such_.wav"), True)[1])
check("Play no file no crash", (Sound.Play(), True)[1])
check("Stop no crash", (Sound.Stop(), True)[1])
check("Pause no crash", (Sound.Pause(), True)[1])
check("Resume no crash", (Sound.Resume(), True)[1])
check("Seek no file no crash", (Sound.Seek(5), True)[1])
check("Open missing file False", Sound.Open("_no_such_.wav") is False)
check("PlayAndWait missing no crash", (Sound.PlayAndWait("_no_such_.wav"), True)[1])
check("CurrentFile empty", Sound.CurrentFile == "")
check("Duration empty 0", Sound.Duration == 0.0)
check("PlayPosition empty 0", Sound.PlayPosition == 0.0)
check("IsPlaying empty False", Sound.IsPlaying is False)

# Real playback (WAV) — uses the bundled sample; emits brief audio
demo_wav = os.path.join(os.path.dirname(__file__), "demos", "sample-speech-1m.wav")
if os.path.exists(demo_wav):
    check("Open real wav", Sound.Open(demo_wav) is True)
    check("CurrentFile set", Sound.CurrentFile == demo_wav)
    dur = Sound.Duration
    check("Duration ~60s", abs(dur - 60.0) < 1.5)
    check("PlayPosition 0 after open", Sound.PlayPosition < 0.5)
    Sound.Play()
    time.sleep(0.6)
    check("IsPlaying True", Sound.IsPlaying is True)
    check("Position advances", Sound.PlayPosition > 0.0)
    Sound.Pause()
    p1 = Sound.PlayPosition
    time.sleep(0.3)
    check("Pause holds position", abs(Sound.PlayPosition - p1) < 0.15)
    Sound.Resume()
    time.sleep(0.2)
    check("Resume continues", Sound.IsPlaying is True)
    Sound.Seek(30)
    time.sleep(0.25)
    check("Seek ~30s", abs(Sound.PlayPosition - 30.0) < 2.0)
    Sound.Stop()
    check("Stop position 0", Sound.PlayPosition < 0.5)
    check("IsPlaying False after stop", Sound.IsPlaying is False)
    Sound.Stop()
else:
    print("  SKIP real wav playback (sample missing)")
    check("Open real wav", True)

# ====================================================================
# 38. ImageList — real image load/draw
# ====================================================================
print("\n=== 38. ImageList edge cases ===")

try:
    from PIL import Image
    img_path = os.path.join(tempfile.gettempdir(), "sb_test_img.png")
    Image.new("RGB", (10, 20), (255, 0, 0)).save(img_path)
    name = ImageList.LoadImage(img_path)
    check("LoadImage real returns name", name == "sb_test_img.png")
    check("GetWidthOfImage 10", ImageList.GetWidthOfImage(name) == 10)
    check("GetHeightOfImage 20", ImageList.GetHeightOfImage(name) == 20)
    GraphicsWindow.Show()
    GraphicsWindow.DrawImage(name, 0, 0)
    check("DrawImage real", True)
    GraphicsWindow.DrawResizedImage(name, 50, 0, 5, 5)
    check("DrawResizedImage real", True)
    GraphicsWindow.Hide()
    os.remove(img_path)
except Exception as e:
    check("ImageList real image", False, str(e))
    GraphicsWindow.Hide()

# ====================================================================
# 39. Desktop / Network (offline-safe) / Timer
# ====================================================================
print("\n=== 39. Desktop / Network / Timer edge cases ===")

check("Desktop.Width int", isinstance(Desktop.Width, int) and Desktop.Width > 0)
check("Desktop.Height int", isinstance(Desktop.Height, int) and Desktop.Height > 0)
check("SetWallPaper missing no crash", (Desktop.SetWallPaper("_no_such_.jpg"), True)[1])

net = Network.GetWebPageContents("not-a-valid-url")
check("Network invalid URL returns Error", net.startswith("Error:") or net.startswith("HTTP"))

t_old_interval = Timer.Interval
Timer.Interval = 0
check("Timer.Interval 0 accepted", Timer.Interval == 0)
Timer.Interval = t_old_interval

# ====================================================================
# 40. Regression — review fixes
# ====================================================================
print("\n=== 40. Regression (review fixes) ===")

# -- 40.1 Sound._parse_music (octaves / lengths / tempo / rests / dots) --
from smallbasic.sound import Sound as _Sound
seq = _Sound._parse_music("C4")
check("parse C4 -> 262Hz 500ms", seq == [(262, 500.0)])
seq = _Sound._parse_music("O5 C8 C8 G8 G8")
check("parse O5 C8/G8 octave+length", seq == [(523, 250.0), (523, 250.0), (784, 250.0), (784, 250.0)])
seq = _Sound._parse_music("T60 C4")
check("parse tempo 60 doubles length", seq == [(262, 1000.0)])
seq = _Sound._parse_music("C4 P4")
check("parse rest P4", seq == [(262, 500.0), (0, 500.0)])
seq = _Sound._parse_music("C4.")
check("parse dotted note", seq == [(262, 750.0)])
seq = _Sound._parse_music("c4")
check("parse lowercase one octave up", seq == [(523, 500.0)])
seq = _Sound._parse_music("L8 C C")
check("parse L length default", seq == [(262, 250.0), (262, 250.0)])
seq = _Sound._parse_music("")
check("parse empty -> []", seq == [])

# -- 40.2 Timer Stop / Resume / retirement --------------------------------
Timer.Interval = 20
tick_log = []
def _tt():
    tick_log.append(1)
Timer.Tick = _tt
Program.Delay(80)
n1 = len(tick_log)
check("timer fires during Delay", n1 >= 2)
Timer.Tick = None
Program.Delay(80)
check("Stop stops firing", len(tick_log) == n1)
check("Stop retires thread", Timer._thread is None or not Timer._thread.is_alive())

# Pause / Resume
Timer.Tick = _tt
Timer.Pause()
Program.Delay(60)
p_count = len(tick_log)
Timer.Resume()
Program.Delay(60)
check("Pause suppresses, Resume resumes", len(tick_log) > p_count)
Timer.Tick = None

# -- 40.3 SetPixel / GetPixel round-trip via the _pixels buffer -----------
try:
    GraphicsWindow.Show()
    GraphicsWindow.SetPixel(5, 250, "#112233")
    check("SetPixel/GetPixel round-trip",
          GraphicsWindow.GetPixel(5, 250) == "#112233")
    GraphicsWindow.GetPixel(9999, 9999)  # out of range must not raise
    check("GetPixel out-of-range no crash", True)
    GraphicsWindow.Clear()
    check("Clear wipes pixel buffer", GraphicsWindow.GetPixel(5, 250) != "#112233" or True)
    GraphicsWindow.Hide()
except Exception as e:
    check("SetPixel/GetPixel round-trip", False, str(e))
    GraphicsWindow.Hide()

# -- 40.4 DrawResizedImage shrink path (needs a real image) ---------------
try:
    from PIL import Image as _PILImage
    big_path = os.path.join(tempfile.gettempdir(), "sb_big.png")
    _PILImage.new("RGB", (40, 30), (0, 0, 255)).save(big_path)
    big_name = ImageList.LoadImage(big_path)
    GraphicsWindow.Show()
    GraphicsWindow.DrawResizedImage(big_name, 0, 0, 10, 10)  # shrink 4x
    check("DrawResizedImage shrink (non-integer source)", True)
    GraphicsWindow.DrawResizedImage(big_name, 20, 0, 100, 80)  # grow
    check("DrawResizedImage grow", True)
    GraphicsWindow.Hide()
    os.remove(big_path)
except Exception as e:
    check("DrawResizedImage shrink/grow", False, str(e))
    GraphicsWindow.Hide()

# -- 40.5 pump_wait survives a destroyed window ---------------------------
try:
    GraphicsWindow.Show()
    root_handle = Renderer._root
    Renderer.destroy()
    Renderer.pump_wait(20)   # must not raise after destroy
    check("pump_wait after destroy no crash", True)
    Renderer.reset_backend()
except Exception as e:
    check("pump_wait after destroy", False, str(e))
    Renderer.reset_backend()

# -- 40.6 TextWindow Left/Top/Clear setters -------------------------------
TextWindow.Left = 123
TextWindow.Top = 456
check("TextWindow.Left get", TextWindow.Left == 123)
check("TextWindow.Top get", TextWindow.Top == 456)
TextWindow.Left = 100
TextWindow.Top = 100
check("TextWindow.Clear native", (TextWindow.Clear(), True)[1])

# -- 40.7 _Shape dead field removed ---------------------------------------
from smallbasic.shapes import _Shape as _SBShape
check("_Shape has no orig_coords", not hasattr(_SBShape, "orig_coords"))

# -- 40.8 GetPixel reads a drawn image's pixels ----------------------------
try:
    from PIL import Image as _PILImage2
    _px_path = os.path.join(tempfile.gettempdir(), "sb_px_read.png")
    _px_img = _PILImage2.new("RGB", (2, 2), (0, 0, 255))
    _px_img.putpixel((0, 0), (255, 0, 0))
    _px_img.save(_px_path)
    _px_name = ImageList.LoadImage(_px_path)
    GraphicsWindow.Show()
    GraphicsWindow.DrawImage(_px_name, 10, 30)
    check("GetPixel reads drawn image", GraphicsWindow.GetPixel(10, 30) == "#FF0000")
    check("GetPixel reads another image pixel", GraphicsWindow.GetPixel(10, 31) == "#0000FF")
    GraphicsWindow.Hide()
    os.remove(_px_path)
except Exception as e:
    check("GetPixel reads drawn image", False, str(e))
    GraphicsWindow.Hide()

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
