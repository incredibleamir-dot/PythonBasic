"""
Python Small Basic — Complete Feature Demo
Showcases ALL classes, methods, properties, and events.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import (
    TextWindow, GraphicsWindow, Turtle, Controls, Shapes, Mouse,
    Sound, Clock, Timer, Network, File, Desktop, Math, Dictionary,
    Array, Stack, Program, ImageList, Text, Keywords
)
import os
import time

print("=" * 72)
print("  PYTHON SMALL BASIC — COMPLETE FEATURE DEMO")
print("  Every class, method, property & event showcased")
print("=" * 72)

# =====================================================================
# SECTION 1: TextWindow — console I/O, colors, cursor
# =====================================================================
print("\n>>> SECTION 1: TextWindow")

TextWindow.Title = "Demo — TextWindow"
TextWindow.ForegroundColor = "Cyan"
TextWindow.BackgroundColor = "Black"
TextWindow.Left = 50
TextWindow.Top = 50
TextWindow.Show()

TextWindow.WriteLine("1.  TextWindow.WriteLine with multiple", "arguments", "like", "this!")
TextWindow.ForegroundColor = "Yellow"
TextWindow.Write("2.  TextWindow.Write (no newline)... ")
TextWindow.ForegroundColor = "Green"
TextWindow.WriteLine("then WriteLine continues.")

TextWindow.Write("3.  TextWindow.ReadNumber — enter a number: ")
_val = TextWindow.ReadNumber()
TextWindow.WriteLine(f"    You entered: {_val}")

TextWindow.Write("4.  TextWindow.Read — type something: ")
_txt = TextWindow.Read()
TextWindow.WriteLine(f"    You typed: {_txt}")

TextWindow.WriteLine("5.  TextWindow.ReadKey — press any key")
_key = TextWindow.ReadKey()
TextWindow.WriteLine(f"    Key: '{_key}'")

TextWindow.WriteLine("6.  TextWindow.CursorLeft / CursorTop (get/set)")
TextWindow.CursorLeft = 5
TextWindow.CursorTop = 2
TextWindow.WriteLine("    (cursor repositioned)")

TextWindow.ForegroundColor = "Red"
TextWindow.BackgroundColor = "DarkGray"
TextWindow.WriteLine("7.  Colors: ForegroundColor, BackgroundColor")
TextWindow.ForegroundColor = "White"
TextWindow.BackgroundColor = "Black"

TextWindow.WriteLine("8.  TextWindow.Pause — press ENTER to continue")
TextWindow.Pause()

TextWindow.WriteLine("9.  TextWindow.Clear (clears console)")
TextWindow.Clear()

TextWindow.WriteLine("10. TextWindow.Hide / Show")
TextWindow.Hide()
time.sleep(0.5)
TextWindow.Show()

TextWindow.WriteLine("11. TextWindow.PauseIfVisible / PauseWithoutMessage")
TextWindow.PauseIfVisible()
TextWindow.PauseWithoutMessage()

TextWindow.WriteLine("12. TextWindow.VerifyAccess — no-op call")
TextWindow.VerifyAccess()

# =====================================================================
# SECTION 2: Text — string operations
# =====================================================================
print("\n>>> SECTION 2: Text")

TextWindow.ForegroundColor = "Cyan"
TextWindow.WriteLine("--- Text Operations ---")

s1, s2 = "Hello", " World"
TextWindow.WriteLine(f"  Text.Append({repr(s1)}, {repr(s2)}) = {repr(Text.Append(s1, s2))}")
TextWindow.WriteLine(f"  Text.GetLength('Hello') = {Text.GetLength('Hello')}")
TextWindow.WriteLine(f"  Text.IsSubText('Hello World', 'World') = {Text.IsSubText('Hello World', 'World')}")
TextWindow.WriteLine(f"  Text.EndsWith('Hello.py', '.py') = {Text.EndsWith('Hello.py', '.py')}")
TextWindow.WriteLine(f"  Text.StartsWith('Hello World', 'Hello') = {Text.StartsWith('Hello World', 'Hello')}")
TextWindow.WriteLine(f"  Text.GetSubText('Hello World', 1, 5) = {repr(Text.GetSubText('Hello World', 1, 5))}")
TextWindow.WriteLine(f"  Text.GetSubTextToEnd('Hello World', 7) = {repr(Text.GetSubTextToEnd('Hello World', 7))}")
TextWindow.WriteLine(f"  Text.GetIndexOf('Hello World', 'World') = {Text.GetIndexOf('Hello World', 'World')}")
TextWindow.WriteLine(f"  Text.ConvertToUpperCase('hello') = {Text.ConvertToUpperCase('hello')}")
TextWindow.WriteLine(f"  Text.ConvertToLowerCase('HELLO') = {Text.ConvertToLowerCase('HELLO')}")
TextWindow.WriteLine(f"  Text.GetCharacter(65) = {repr(Text.GetCharacter(65))}")
TextWindow.WriteLine(f"  Text.GetCharacterCode('A') = {Text.GetCharacterCode('A')}")

# =====================================================================
# SECTION 3: Math — all operations
# =====================================================================
print("\n>>> SECTION 3: Math")

TextWindow.ForegroundColor = "Yellow"
TextWindow.WriteLine("--- Math Operations ---")

TextWindow.WriteLine(f"  Math.Pi = {Math.Pi}")
TextWindow.WriteLine(f"  Math.Abs(-5) = {Math.Abs(-5)}")
TextWindow.WriteLine(f"  Math.Ceiling(3.2) = {Math.Ceiling(3.2)}")
TextWindow.WriteLine(f"  Math.Floor(3.7) = {Math.Floor(3.7)}")
TextWindow.WriteLine(f"  Math.Round(3.5) = {Math.Round(3.5)}")
TextWindow.WriteLine(f"  Math.Sin(90) = {Math.Sin(90):.4f}")
TextWindow.WriteLine(f"  Math.Cos(0) = {Math.Cos(0):.4f}")
TextWindow.WriteLine(f"  Math.Tan(45) = {Math.Tan(45):.4f}")
TextWindow.WriteLine(f"  Math.ArcSin(1) = {Math.ArcSin(1):.2f} deg")
TextWindow.WriteLine(f"  Math.ArcCos(0.5) = {Math.ArcCos(0.5):.2f} deg")
TextWindow.WriteLine(f"  Math.ArcTan(1) = {Math.ArcTan(1):.2f} deg")
TextWindow.WriteLine(f"  Math.SquareRoot(144) = {Math.SquareRoot(144)}")
TextWindow.WriteLine(f"  Math.Power(2, 10) = {Math.Power(2, 10)}")
TextWindow.WriteLine(f"  Math.Log(1000) = {Math.Log(1000)}")
TextWindow.WriteLine(f"  Math.NaturalLog(e) = {Math.NaturalLog(2.71828):.4f}")
TextWindow.WriteLine(f"  Math.Max(10, 20, 5, 30, 15) = {Math.Max(10, 20, 5, 30, 15)}")
TextWindow.WriteLine(f"  Math.Min(10, 20, 5, 30, 15) = {Math.Min(10, 20, 5, 30, 15)}")
TextWindow.WriteLine(f"  Math.Sum(1, 2, 3, 4, 5) = {Math.Sum(1, 2, 3, 4, 5)}")
TextWindow.WriteLine(f"  Math.Average(10, 20, 30) = {Math.Average(10, 20, 30)}")
TextWindow.WriteLine(f"  Math.Remainder(10, 3) = {Math.Remainder(10, 3)}")
r = Math.GetRandomNumber(100)
TextWindow.WriteLine(f"  Math.GetRandomNumber(100) = {r}")
TextWindow.WriteLine(f"  Math.GetDegrees(3.14159) = {Math.GetDegrees(3.14159):.1f}")
TextWindow.WriteLine(f"  Math.GetRadians(180) = {Math.GetRadians(180):.4f}")

# =====================================================================
# SECTION 4: Clock — system time & date
# =====================================================================
print("\n>>> SECTION 4: Clock")

TextWindow.ForegroundColor = "Green"
TextWindow.WriteLine("--- Clock (System Time) ---")
TextWindow.WriteLine(f"  Clock.Time                 = {Clock.Time}")
TextWindow.WriteLine(f"  Clock.Date                 = {Clock.Date}")
TextWindow.WriteLine(f"  Clock.Year                 = {Clock.Year}")
TextWindow.WriteLine(f"  Clock.Month                = {Clock.Month}")
TextWindow.WriteLine(f"  Clock.Day                  = {Clock.Day}")
TextWindow.WriteLine(f"  Clock.WeekDay              = {Clock.WeekDay}")
TextWindow.WriteLine(f"  Clock.Hour                 = {Clock.Hour}")
TextWindow.WriteLine(f"  Clock.Minute               = {Clock.Minute}")
TextWindow.WriteLine(f"  Clock.Second               = {Clock.Second}")
TextWindow.WriteLine(f"  Clock.Millisecond          = {Clock.Millisecond}")
TextWindow.WriteLine(f"  Clock.ElapsedMilliseconds  = {Clock.ElapsedMilliseconds}")

# =====================================================================
# SECTION 5: Program — delay, args, directory
# =====================================================================
print("\n>>> SECTION 5: Program")

TextWindow.ForegroundColor = "Magenta"
TextWindow.WriteLine("--- Program ---")
TextWindow.WriteLine(f"  Program.ArgumentCount = {Program.ArgumentCount}")
TextWindow.WriteLine(f"  Program.GetArgument(0) = {repr(Program.GetArgument(0))}")
TextWindow.WriteLine(f"  Program.Directory = {Program.Directory}")
TextWindow.WriteLine("  Program.Delay(1000) — waiting 1 second...")
Program.Delay(1000)
TextWindow.WriteLine("  Done.")

# =====================================================================
# SECTION 6: Array — key-value store
# =====================================================================
print("\n>>> SECTION 6: Array")

TextWindow.ForegroundColor = "White"
TextWindow.WriteLine("--- Array Operations ---")

Array.SetValue("inventory", "apples", 10)
Array.SetValue("inventory", "oranges", 5)
Array.SetValue("inventory", "bananas", 7)
TextWindow.WriteLine(f"  Array.GetValue('inventory', 'apples') = {Array.GetValue('inventory', 'apples')}")
TextWindow.WriteLine(f"  Array.ContainsIndex('inventory', 'apples') = {Array.ContainsIndex('inventory', 'apples')}")
TextWindow.WriteLine(f"  Array.ContainsValue('inventory', 5) = {Array.ContainsValue('inventory', 5)}")
TextWindow.WriteLine(f"  Array.GetItemCount('inventory') = {Array.GetItemCount('inventory')}")
indices = Array.GetAllIndices("inventory")
TextWindow.WriteLine(f"  Array.GetAllIndices('inventory') = {indices}")
TextWindow.WriteLine(f"  Array.IsArray({{'a':1}}) = {Array.IsArray({'a': 1})}")
TextWindow.WriteLine(f"  Array.IsArray(42) = {Array.IsArray(42)}")
Array.RemoveValue("inventory", "bananas")
TextWindow.WriteLine(f"  After Remove, count = {Array.GetItemCount('inventory')}")

# =====================================================================
# SECTION 7: Stack — push / pop
# =====================================================================
print("\n>>> SECTION 7: Stack")

TextWindow.ForegroundColor = "Cyan"
TextWindow.WriteLine("--- Stack Operations ---")

Stack.PushValue("mystack", "first")
Stack.PushValue("mystack", "second")
Stack.PushValue("mystack", "third")
TextWindow.WriteLine(f"  Stack.GetCount('mystack') = {Stack.GetCount('mystack')}")
TextWindow.WriteLine(f"  Stack.PopValue('mystack') = {Stack.PopValue('mystack')}")
TextWindow.WriteLine(f"  Stack.PopValue('mystack') = {Stack.PopValue('mystack')}")
TextWindow.WriteLine(f"  Stack.PopValue('mystack') = {Stack.PopValue('mystack')}")
TextWindow.WriteLine(f"  Stack.PopValue('mystack') = {repr(Stack.PopValue('mystack'))} (empty)")

# =====================================================================
# SECTION 8: Desktop — screen dimensions, wallpaper
# =====================================================================
print("\n>>> SECTION 8: Desktop")

TextWindow.ForegroundColor = "White"
TextWindow.WriteLine("--- Desktop ---")
TextWindow.WriteLine(f"  Desktop.Width  = {Desktop.Width} px")
TextWindow.WriteLine(f"  Desktop.Height = {Desktop.Height} px")

# =====================================================================
# SECTION 9: File — read, write, copy, delete
# =====================================================================
print("\n>>> SECTION 9: File")

TextWindow.ForegroundColor = "Yellow"
TextWindow.WriteLine("--- File Operations ---")

tmp_file = File.GetTemporaryFilePath()
if tmp_file:
    TextWindow.WriteLine(f"  File.GetTemporaryFilePath() = {tmp_file}")
    r1 = File.WriteContents(tmp_file, "Hello from Python Small Basic!")
    TextWindow.WriteLine(f"  File.WriteContents → {r1}")
    r2 = File.AppendContents(tmp_file, "\nAppended line.")
    TextWindow.WriteLine(f"  File.AppendContents → {r2}")
    r3 = File.ReadContents(tmp_file)
    TextWindow.WriteLine(f"  File.ReadContents → {repr(r3[:50])}...")
    File.WriteLine(tmp_file, 2, "Overwritten line 2")
    TextWindow.WriteLine(f"  File.ReadLine(line 2) = {repr(File.ReadLine(tmp_file, 2))}")
    File.InsertLine(tmp_file, 1, "Inserted line")
    TextWindow.WriteLine(f"  After InsertLine, line 1 = {repr(File.ReadLine(tmp_file, 1))}")
    copy_path = tmp_file + ".copy"
    File.CopyFile(tmp_file, copy_path)
    TextWindow.WriteLine(f"  File.CopyFile → copy exists = {os.path.exists(copy_path)}")
    File.DeleteFile(copy_path)
    TextWindow.WriteLine("  File.DeleteFile (copy removed)")
    File.DeleteFile(tmp_file)
    TextWindow.WriteLine("  File.DeleteFile (original removed)")

test_dir = "demo_test_dir"
File.CreateDirectory(test_dir)
TextWindow.WriteLine(f"  File.CreateDirectory('{test_dir}') → {os.path.isdir(test_dir)}")
files = File.GetFiles(".")
TextWindow.WriteLine(f"  File.GetFiles('.') → {len(files)} files found")
dirs = File.GetDirectories(".")
TextWindow.WriteLine(f"  File.GetDirectories('.') → {len(dirs)} dirs found")
File.DeleteDirectory(test_dir)
TextWindow.WriteLine(f"  File.DeleteDirectory → exists = {os.path.exists(test_dir)}")
TextWindow.WriteLine(f"  File.GetSettingsFilePath() = {File.GetSettingsFilePath()}")

# =====================================================================
# SECTION 10: Network — HTTP requests
# =====================================================================
print("\n>>> SECTION 10: Network")

TextWindow.ForegroundColor = "Green"
TextWindow.WriteLine("--- Network ---")
try:
    html = Network.GetWebPageContents("https://jsonplaceholder.typicode.com/todos/1")
    TextWindow.WriteLine(f"  Network.GetWebPageContents → {html[:80]}...")
    get_resp = Network.Get("https://jsonplaceholder.typicode.com/posts/1")
    TextWindow.WriteLine(f"  Network.Get → id={get_resp[8:12] if len(get_resp)>12 else 'ok'}...")
    post_resp = Network.Post("https://jsonplaceholder.typicode.com/posts",
                              {"title": "demo", "body": "test", "userId": 1})
    TextWindow.WriteLine(f"  Network.Post → {post_resp[:50]}...")
    put_resp = Network.Put("https://jsonplaceholder.typicode.com/posts/1",
                            {"title": "updated", "body": "body", "userId": 1})
    TextWindow.WriteLine(f"  Network.Put → {put_resp[:50]}...")
    del_resp = Network.Delete("https://jsonplaceholder.typicode.com/posts/1")
    TextWindow.WriteLine(f"  Network.Delete → {del_resp[:50]}...")
    patch_resp = Network.Patch("https://jsonplaceholder.typicode.com/posts/1",
                                {"title": "patched"})
    TextWindow.WriteLine(f"  Network.Patch → {patch_resp[:50]}...")
    dl_path = Network.DownloadFile("https://jsonplaceholder.typicode.com/todos/1")
    TextWindow.WriteLine(f"  Network.DownloadFile → {dl_path}")
except Exception as e:
    TextWindow.WriteLine(f"  Network error (offline?): {e}")

# =====================================================================
# SECTION 11: Dictionary — definitions & translations
# =====================================================================
print("\n>>> SECTION 11: Dictionary")

TextWindow.ForegroundColor = "Magenta"
TextWindow.WriteLine("--- Dictionary ---")
try:
    defn = Dictionary.GetDefinition("computer")
    TextWindow.WriteLine(f"  Dictionary.GetDefinition('computer') → {defn[:80]}...")
    es = Dictionary.GetDefinitionEnglishToSpanish("hello")
    TextWindow.WriteLine(f"  GetDefinitionEnglishToSpanish('hello') → {es}")
    fr = Dictionary.GetDefinitionEnglishToFrench("hello")
    TextWindow.WriteLine(f"  GetDefinitionEnglishToFrench('hello') → {fr}")
    de = Dictionary.GetDefinitionEnglishToGerman("hello")
    TextWindow.WriteLine(f"  GetDefinitionEnglishToGerman('hello') → {de}")
    it = Dictionary.GetDefinitionEnglishToItalian("hello")
    TextWindow.WriteLine(f"  GetDefinitionEnglishToItalian('hello') → {it}")
    ja = Dictionary.GetDefinitionEnglishToJapanese("hello")
    TextWindow.WriteLine(f"  GetDefinitionEnglishToJapanese('hello') → {ja}")
    ko = Dictionary.GetDefinitionEnglishToKorean("hello")
    TextWindow.WriteLine(f"  GetDefinitionEnglishToKorean('hello') → {ko}")
    zh_s = Dictionary.GetDefinitionEnglishToSimplifiedChinese("hello")
    TextWindow.WriteLine(f"  GetDefinitionEnglishToSimplifiedChinese('hello') → {zh_s}")
    zh_t = Dictionary.GetDefinitionEnglishToTraditionalChinese("hello")
    TextWindow.WriteLine(f"  GetDefinitionEnglishToTraditionalChinese('hello') → {zh_t}")
except Exception as e:
    TextWindow.WriteLine(f"  Dictionary error (offline?): {e}")

# =====================================================================
# SECTION 12: Mouse — cursor & button state
# =====================================================================
print("\n>>> SECTION 12: Mouse")

TextWindow.ForegroundColor = "White"
TextWindow.WriteLine("--- Mouse ---")
TextWindow.WriteLine(f"  Mouse.MouseX = {Mouse.MouseX}, Mouse.MouseY = {Mouse.MouseY}")
old_x, old_y = Mouse.MouseX, Mouse.MouseY
Mouse.MouseX, Mouse.MouseY = 500, 400
TextWindow.WriteLine(f"  After Mouse.MouseX/Y set → ({Mouse.MouseX}, {Mouse.MouseY})")
Mouse.MouseX, Mouse.MouseY = old_x, old_y
TextWindow.WriteLine(f"  Mouse.IsLeftButtonDown = {Mouse.IsLeftButtonDown}")
TextWindow.WriteLine(f"  Mouse.IsRightButtonDown = {Mouse.IsRightButtonDown}")
Mouse.ShowCursor()
TextWindow.WriteLine("  Mouse.ShowCursor()")
Mouse.HideCursor()
TextWindow.WriteLine("  Mouse.HideCursor()")
Program.Delay(500)
Mouse.ShowCursor()
TextWindow.WriteLine("  Mouse.ShowCursor() restored cursor")

# =====================================================================
# SECTION 13: Sound — system sounds
# =====================================================================
print("\n>>> SECTION 13: Sound")

TextWindow.ForegroundColor = "Blue"
TextWindow.WriteLine("--- Sound ---")
Sound.PlayClick()
TextWindow.WriteLine("  Sound.PlayClick()")
Program.Delay(300)
Sound.PlayChime()
TextWindow.WriteLine("  Sound.PlayChime()")
Program.Delay(300)
Sound.PlayBellRing()
TextWindow.WriteLine("  Sound.PlayBellRing()")
Program.Delay(300)
Sound.PlayChimes()
TextWindow.WriteLine("  Sound.PlayChimes()")
Program.Delay(300)
Sound.PlayMusic("C4 D4 E4 F4 G4 A4 B4 c5")
TextWindow.WriteLine("  Sound.PlayMusic (scale)")
Program.Delay(1500)
Sound.Pause()
TextWindow.WriteLine("  Sound.Pause()")
Program.Delay(500)
Sound.Resume()
TextWindow.WriteLine("  Sound.Resume()")
Program.Delay(500)
Sound.Stop()
TextWindow.WriteLine("  Sound.Stop()")
Sound.PlayClickAndWait()
TextWindow.WriteLine("  Sound.PlayClickAndWait()")
Sound.PlayChimeAndWait()
TextWindow.WriteLine("  Sound.PlayChimeAndWait()")
Sound.PlayChimesAndWait()
TextWindow.WriteLine("  Sound.PlayChimesAndWait()")
Sound.PlayBellRingAndWait()
TextWindow.WriteLine("  Sound.PlayBellRingAndWait()")

# =====================================================================
# SECTION 14: Timer — interval-based callbacks
# =====================================================================
print("\n>>> SECTION 14: Timer")

TextWindow.ForegroundColor = "Cyan"
TextWindow.WriteLine("--- Timer ---")
tick_count = [0]

def on_tick():
    tick_count[0] += 1
    if tick_count[0] <= 3:
        TextWindow.WriteLine(f"  Timer.Tick #{tick_count[0]}")

Timer.Interval = 500
Timer.Tick = on_tick
Timer.Resume()
Program.Delay(2200)
Timer.Pause()
TextWindow.WriteLine(f"  Timer ticked {tick_count[0]} times total")
Timer.Tick = None

# =====================================================================
# SECTION 15: ImageList — loading & querying images
# =====================================================================
print("\n>>> SECTION 15: ImageList")

TextWindow.ForegroundColor = "Yellow"
TextWindow.WriteLine("--- ImageList ---")
result = ImageList.LoadImage("nonexistent_demo_file.png")
TextWindow.WriteLine(f"  ImageList.LoadImage (missing file) → '{result}'")
TextWindow.WriteLine(f"  ImageList.GetWidthOfImage('nonexistent') = {ImageList.GetWidthOfImage('nonexistent')}")
TextWindow.WriteLine(f"  ImageList.GetHeightOfImage('nonexistent') = {ImageList.GetHeightOfImage('nonexistent')}")

# =====================================================================
# SECTION 16: Keywords — placeholder class
# =====================================================================
print("\n>>> SECTION 16: Keywords")

TextWindow.ForegroundColor = "White"
TextWindow.WriteLine("--- Keywords (documentation placeholder) ---")
TextWindow.WriteLine(f"  Keywords docstring exists: {bool(Keywords.__doc__)}")

# =====================================================================
# SECTION 17: GRAPHICS WINDOW — drawings, shapes, turtle, controls
# =====================================================================
print("\n>>> SECTION 17: GraphicsWindow, Shapes, Turtle, Controls")

TextWindow.WriteLine("Initializing GraphicsWindow...")

GraphicsWindow.Title = "Python Small Basic - Complete Demo"
GraphicsWindow.Width = 800
GraphicsWindow.Height = 600
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Left = 100
GraphicsWindow.Top = 100
GraphicsWindow.CanResize = True
GraphicsWindow.Show()

# ----- 17a: Drawing primitives (batched) -----
GraphicsWindow.BeginBatch()
GraphicsWindow.PenColor = "Black"
GraphicsWindow.PenWidth = 2
GraphicsWindow.BrushColor = "LightGray"

GraphicsWindow.DrawText(10, 5, "a) Drawing primitives")
GraphicsWindow.DrawRectangle(10, 25, 80, 60)
GraphicsWindow.FillRectangle(100, 25, 80, 60)
GraphicsWindow.DrawEllipse(190, 25, 80, 60)
GraphicsWindow.FillEllipse(280, 25, 80, 60)
GraphicsWindow.DrawTriangle(370, 85, 420, 25, 470, 85)
GraphicsWindow.FillTriangle(480, 85, 530, 25, 580, 85)
GraphicsWindow.DrawLine(600, 25, 680, 85)
GraphicsWindow.SetPixel(620, 50, "Red")
GraphicsWindow.EndBatch()
pixel_color = GraphicsWindow.GetPixel(620, 50)
GraphicsWindow.DrawText(630, 50, f"Pixel: {pixel_color}")

GraphicsWindow.BeginBatch()
GraphicsWindow.PenColor = "DarkBlue"
GraphicsWindow.DrawText(10, 95, "b) Text & fonts")
GraphicsWindow.FontName = "Arial"
GraphicsWindow.FontSize = 16
GraphicsWindow.FontBold = True
GraphicsWindow.FontItalic = False
GraphicsWindow.DrawText(10, 110, "Arial 16 Bold")
GraphicsWindow.FontSize = 20
GraphicsWindow.FontBold = False
GraphicsWindow.FontItalic = True
GraphicsWindow.DrawText(10, 135, "Arial 20 Italic")
GraphicsWindow.FontSize = 24
GraphicsWindow.FontBold = True
GraphicsWindow.FontItalic = True
GraphicsWindow.DrawText(10, 165, "Arial 24 Bold Italic")
GraphicsWindow.FontSize = 12
GraphicsWindow.FontBold = False
GraphicsWindow.FontItalic = False
GraphicsWindow.FontName = "Consolas"
GraphicsWindow.DrawBoundText(10, 200, 150, "DrawBoundText wraps long text automatically at the given width.")
GraphicsWindow.EndBatch()

rc = GraphicsWindow.GetRandomColor()
GraphicsWindow.DrawText(10, 235, f"c) Random color: {rc}")
GraphicsWindow.BrushColor = rc
GraphicsWindow.FillEllipse(10, 250, 40, 40)

rgb = GraphicsWindow.GetColorFromRGB(255, 100, 50)
GraphicsWindow.DrawText(10, 295, f"d) GetColorFromRGB(255,100,50) = {rgb}")
GraphicsWindow.BrushColor = rgb
GraphicsWindow.FillRectangle(10, 310, 40, 40)

# ----- 17b: Shapes -----
GraphicsWindow.DrawText(10, 360, "e) Shapes (animated on canvas)")
shape_rect = Shapes.AddRectangle(60, 40)
Shapes.Move(shape_rect, 10, 380)
Shapes.SetOpacity(shape_rect, 70)

shape_ellipse = Shapes.AddEllipse(50, 30)
Shapes.Move(shape_ellipse, 90, 390)
Shapes.Rotate(shape_ellipse, 30)

shape_line = Shapes.AddLine(160, 380, 210, 420)

shape_tri = Shapes.AddTriangle(230, 380, 260, 420, 290, 380)
Shapes.Rotate(shape_tri, 45)

shape_text = Shapes.AddText("Shape Text")
Shapes.Move(shape_text, 310, 390)

Program.Delay(500)
Shapes.Zoom(shape_rect, 1.5, 1.5)
Shapes.Rotate(shape_ellipse, -15)
Shapes.Animate(shape_tri, 300, 430, 800)
Shapes.HideShape(shape_line)
Program.Delay(300)
Shapes.ShowShape(shape_line)
Shapes.SetText(shape_text, "Text Set!")

Program.Delay(500)
Shapes.Remove(shape_rect)
Shapes.Remove(shape_ellipse)
Shapes.Remove(shape_line)
Shapes.Remove(shape_tri)
Shapes.Remove(shape_text)

# ----- 17c: Turtle -----
GraphicsWindow.DrawText(10, 430, "f) Turtle drawing")
Turtle.Speed = 10
Turtle.X = 550
Turtle.Y = 180
Turtle.Angle = 90
Turtle.PenDown()
Turtle.Show()

# Square
GraphicsWindow.PenColor = "Blue"
for _ in range(4):
    Turtle.Move(40)
    Turtle.Turn(-90)

# Star
Turtle.PenUp()
Turtle.MoveTo(500, 280)
Turtle.PenDown()
GraphicsWindow.PenColor = "Purple"
for _ in range(5):
    Turtle.Move(35)
    Turtle.Turn(-144)

# Spiral
Turtle.PenUp()
Turtle.MoveTo(620, 340)
Turtle.Angle = 0
Turtle.PenDown()
GraphicsWindow.PenColor = "DarkGreen"
for i in range(15):
    Turtle.Move(6 + i * 2)
    Turtle.Turn(-60)

Turtle.PenUp()
Turtle.Hide()

# ----- 17d: Controls -----
GraphicsWindow.DrawText(400, 10, "g) Controls")
btn = Controls.AddButton("Click Me!", 400, 30)
tb1 = Controls.AddTextBox(400, 70)
tb2 = Controls.AddMultiLineTextBox(400, 110)

Controls.SetTextBoxText(tb1, "Edit this text")
Controls.SetTextBoxText(tb2, "Multi-line\ntext box")
txt_read = Controls.GetTextBoxText(tb1)
Controls.SetButtonCaption(btn, "Clicked!" if txt_read else "Click Me!")

def on_button_click():
    Controls.SetButtonCaption(btn, "Button Clicked!")
    GraphicsWindow.DrawText(400, 195, "ButtonClicked fired!")

def on_text_typed():
    GraphicsWindow.DrawText(400, 205, f"TextTyped: {Controls.LastTypedTextBox}")

Controls.ButtonClicked = on_button_click
Controls.TextTyped = on_text_typed

Controls.SetSize(btn, 120, 30)
Controls.Move(btn, 400, 180)

Controls.HideControl(btn)
Program.Delay(400)
Controls.ShowControl(btn)

ctrl_tb = Controls.AddTextBox(400, 220)
Controls.SetTextBoxText(ctrl_tb, "To be removed")
Controls.Remove(ctrl_tb)

# ----- 17e: Events -----
GraphicsWindow.DrawText(400, 260, "h) Events — press a key or click")

def on_keydown(evt):
    GraphicsWindow.PenColor = "DarkRed"
    GraphicsWindow.DrawText(400, 280, f"  KeyDown: {evt.keysym}")

def on_mousedown(evt):
    GraphicsWindow.PenColor = "Red"
    GraphicsWindow.FillEllipse(evt.x - 3, evt.y - 3, 6, 6)

GraphicsWindow.KeyDown = on_keydown
GraphicsWindow.MouseDown = on_mousedown

# ----- 17f: ShowMessage -----
GraphicsWindow.DrawText(400, 310, "i) ShowMessage box")
GraphicsWindow.DrawText(400, 325, "   LastKey/LastText/MouseX/MouseY also available")
Program.Delay(800)
GraphicsWindow.ShowMessage("Python Small Basic demo complete!", "Demo")

# ----- 17g: GraphicsWindow.Hide -----
GraphicsWindow.DrawText(400, 340, "j) GraphicsWindow.Hide / Show")
Program.Delay(500)
GraphicsWindow.Hide()
Program.Delay(500)
GraphicsWindow.Show()

# ----- 17h: GraphicsWindow.Clear -----
Program.Delay(500)
GraphicsWindow.Clear()

GraphicsWindow.DrawText(260, 250, "ALL FEATURES DEMONSTRATED SUCCESSFULLY!")
GraphicsWindow.DrawText(270, 280, "Close window to exit.")

# =====================================================================
# SECTION 18: Wait & Exit
# =====================================================================
print("\n>>> SECTION 18: Demo Complete")
TextWindow.WriteLine("")
TextWindow.ForegroundColor = "Green"
TextWindow.WriteLine("=" * 72)
TextWindow.WriteLine("  ALL FEATURES DEMONSTRATED SUCCESSFULLY!")
TextWindow.WriteLine("=" * 72)
TextWindow.WriteLine("Close the Graphics Window to exit.")

GraphicsWindow.Wait()
Program.End()
