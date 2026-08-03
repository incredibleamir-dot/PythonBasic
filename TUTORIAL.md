# Python Small Basic — Quick Start Tutorial

A beginner-friendly, tutorial-style guide to the Python Small Basic library.
Everything you need to write your first programs: variables, text output,
math, graphics, arrays, events, timers, files, and more — with a runnable
example for every API.

> **Platform:** Windows. Uses only the Python standard library — no `pip install`
> beyond Python itself (optional `Pillow` only for extra image formats).

---

## Table of Contents

- [1. Installation & your first program](#1-installation--your-first-program)
- [2. Variables and data types](#2-variables-and-data-types)
- [3. Text output & input — `TextWindow`](#3-text-output--input--textwindow)
- [4. Math — the `Math` object](#4-math--the-math-object)
- [5. Text helpers — the `Text` object](#5-text-helpers--the-text-object)
- [6. Date & time — the `Clock` object](#6-date--time--the-clock-object)
- [7. Arrays](#7-arrays)
- [8. Decisions and loops](#8-decisions-and-loops)
- [9. Subroutines (functions)](#9-subroutines-functions)
- [10. Drawing — `GraphicsWindow`](#10-drawing--graphicswindow)
- [11. Keyboard & mouse events](#11-keyboard--mouse-events)
- [12. Buttons & text boxes — `Controls`](#12-buttons--text-boxes--controls)
- [13. Timers — the `Timer` object](#13-timers--the-timer-object)
- [14. Turtle graphics — the `Turtle` object](#14-turtle-graphics--the-turtle-object)
- [15. Animated shapes — the `Shapes` object](#15-animated-shapes--the-shapes-object)
- [16. Sound — the `Sound` object](#16-sound--the-sound-object)
- [17. Files — the `File` object](#17-files--the-file-object)
- [18. Internet — the `Network` object](#18-internet--the-network-object)
- [19. Mouse & screen — `Mouse` and `Desktop`](#19-mouse--screen--mouse-and-desktop)
- [20. Program utilities — the `Program` object](#20-program-utilities--the-program-object)
- [21. Stack — the `Stack` object](#21-stack--the-stack-object)
- [22. Images — the `ImageList` object](#22-images--the-imagelist-object)
- [23. Dictionary & translation](#23-dictionary--translation)
- [24. Keeping windows open — `Wait()` and friends](#24-keeping-windows-open--wait-and-friends)
- [25. Two complete example programs](#25-two-complete-example-programs)

---

## 1. Installation & your first program

### Install

```bash
pip install python-smallbasic
```

or copy the `smallbasic/` folder next to your script (everything is standard
library — no other dependencies).

### Import

The whole library is available with one import:

```python
from smallbasic import *
```

This gives you: `TextWindow`, `GraphicsWindow`, `Turtle`, `Controls`, `Shapes`,
`Sound`, `Math`, `Clock`, `Timer`, `Array`, `File`, `Network`, `Desktop`,
`Mouse`, `Program`, `Stack`, `Text`, `ImageList`, `Dictionary`.

### Hello, World!

Create `hello.py`:

```python
from smallbasic import *

TextWindow.Title = "My First Program"
TextWindow.WriteLine("Hello, World!")
TextWindow.WriteLine("Welcome to Python Small Basic!")
```

Run it:

```bash
python hello.py
```

> **Tip:** if you double-click `hello.py` (or run it from an IDE) the console
> window closes as soon as the program ends. Add `TextWindow.Pause()` at the end
> to keep it open — see [section 24](#24-keeping-windows-open--wait-and-friends).

---

## 2. Variables and data types

There is **no special syntax to declare a variable** — you create one the moment
you assign it, exactly like normal Python:

```python
age = 10            # a whole number (int)
score = 97.5        # a decimal number (float)
name = "Alice"      # a string of text
alive = True        # a boolean (True / False)
nothing = None      # no value yet
```

You can mix and reassign any type freely:

```python
x = 5
x = "now I am text"   # fine — Python doesn't care
```

Arithmetic uses normal Python operators:

```python
a = 10
b = 3
sum_   = a + b        # 13
diff   = a - b        # 7
prod   = a * b        # 30
quot   = a / b        # 3.333...
mod    = a % b        # 1   (remainder)
power  = a ** b       # 1000
```

String concatenation uses `+`, and `str()` converts numbers to text:

```python
name = "Alice"
age = 10
greeting = "Hello " + name + " you are " + str(age) + "!"
```

You can also use f-strings (normal Python):

```python
greeting = f"Hello {name} you are {age}!"
```

**Case sensitivity:** unlike Small Basic, Python is case-sensitive. `count`,
`Count`, and `COUNT` are three different variables. Pick one style and be consistent.

---

## 3. Text output & input — `TextWindow`

`TextWindow` is a console-style window for text programs.

### Output

```python
TextWindow.Show()                              # show/refresh the console
TextWindow.WriteLine("One line")               # write text + newline
TextWindow.WriteLine("a", "b", "c")            # multiple values, joined by spaces
TextWindow.Write("no newline ")                # write without a newline
TextWindow.Write("still on same line")
TextWindow.WriteLine()                         # blank line
TextWindow.Clear()                             # clear the console
```

### Input

```python
name = TextWindow.Read()          # read a whole line of text -> str
n    = TextWindow.ReadNumber()    # read a number -> float
key  = TextWindow.ReadKey()       # read a single key press -> str
```

### Pausing

```python
TextWindow.Pause()                # "Press ENTER to continue..."
TextWindow.PauseWithoutMessage()  # wait for ENTER, no message
```

### Colors & window

```python
TextWindow.Title = "My Console"
TextWindow.ForegroundColor = "Cyan"
TextWindow.BackgroundColor = "DarkBlue"
TextWindow.Left = 200             # window position on screen
TextWindow.Top = 150
```

Available color names: `Black`, `DarkBlue`, `DarkGreen`, `DarkCyan`, `DarkRed`,
`DarkMagenta`, `DarkYellow`, `Gray`, `DarkGray`, `Blue`, `Green`, `Cyan`, `Red`,
`Magenta`, `Yellow`, `White`.

**Example — a tiny quiz:**

```python
from smallbasic import *

TextWindow.Show()
TextWindow.WriteLine("Quick maths!")
TextWindow.WriteLine("What is 6 x 7?")
answer = TextWindow.ReadNumber()

if answer == 42:
    TextWindow.WriteLine("Correct!")
else:
    TextWindow.WriteLine("Nope, the answer is 42.")

TextWindow.Pause()
```

---

## 4. Math — the `Math` object

All `Math` methods are class methods on the `Math` object. Trigonometry is in
**degrees** (not radians).

```python
Math.Pi                     # 3.14159...
Math.Abs(-5)                # 5
Math.Floor(3.9)             # 3
Math.Ceiling(3.1)           # 4
Math.Round(3.5)             # 4
Math.SquareRoot(16)         # 4.0
Math.Power(2, 10)           # 1024.0
Math.NaturalLog(2.71828)    # ~1.0   (ln)
Math.Log(1000)              # ~3.0   (log base 10)

Math.Sin(90)                # 1.0
Math.Cos(0)                 # 1.0
Math.Tan(45)                # 1.0
Math.ArcSin(1)              # 90.0   (returns degrees)
Math.ArcCos(1)              # 0.0
Math.ArcTan(1)              # 45.0
Math.GetRadians(180)        # ~3.14
Math.GetDegrees(3.14159)    # ~180

Math.Remainder(10, 3)       # 1
Math.GetRandomNumber(100)   # random integer between 1 and 100
```

"Fun with arguments" — these accept any number of values:

```python
Math.Max(3, 9, 5, 7)        # 9
Math.Min(3, 9, 5, 7)        # 3
Math.Sum(1, 2, 3, 4)        # 10
Math.Average(1, 2, 3, 4)    # 2.5
```

---

## 5. Text helpers — the `Text` object

String utilities:

```python
Text.Append("Hello", "World")         # "HelloWorld"
Text.GetLength("Hello")               # 5
Text.IsSubText("hello world", "llo")  # True
Text.StartsWith("hello", "he")        # True
Text.EndsWith("hello", "lo")          # True
Text.GetIndexOf("hello world", "world")  # 7  (1-based position, 0 if not found)

Text.GetSubText("hello", 2, 3)        # "ell"  (start=1-based, length)
Text.GetSubTextToEnd("hello", 3)      # "llo"  (from 1-based position to end)
Text.ConvertToUpperCase("hi")         # "HI"
Text.ConvertToLowerCase("HI")         # "hi"
Text.GetCharacter(65)                 # "A"
Text.GetCharacterCode("A")            # 65
```

---

## 6. Date & time — the `Clock` object

Read-only properties that always reflect the current moment:

```python
Clock.Time                  # "14:05:33"
Clock.Date                  # "07/31/2026"
Clock.Year                  # 2026
Clock.Month                 # 7
Clock.Day                   # 31
Clock.WeekDay               # "Friday"
Clock.Hour                  # 14
Clock.Minute                # 5
Clock.Second                # 33
Clock.Millisecond           # 123
Clock.ElapsedMilliseconds   # ms since 1900 (handy as a stopwatch)
```

Example — time a piece of code:

```python
start = Clock.ElapsedMilliseconds
Program.Delay(500)                      # wait 500 ms (see section 20)
elapsed = Clock.ElapsedMilliseconds - start
TextWindow.WriteLine("That took " + str(elapsed) + " ms")
```

---

## 7. Arrays

You have two choices.

### Option A — plain Python lists / dicts

The simplest and most Pythonic. Zero-based indexing:

```python
scores = [10, 20, 30]        # a list
scores.append(40)            # add to the end
first = scores[0]            # 10

person = {"name": "Alice", "age": 10}   # a dictionary (named slots)
name = person["name"]
```

### Option B — the Small Basic-style `Array` object

`Array` mimics Small Basic's named array store: 1-based indexes and string keys.
Values are stored under a name you choose.

```python
Array.SetValue("students", "name", "Alice")   # store "students" -> "name" -> "Alice"
Array.SetValue("students", "age", 10)
Array.SetValue("students", "grade", "A")

Array.GetValue("students", "name")     # "Alice"
Array.GetValue("students", "missing")  # ""  (empty string, no error)
```

More `Array` methods:

```python
Array.ContainsIndex("students", "name")     # True
Array.ContainsValue("students", "Alice")    # True
Array.GetItemCount("students")              # 3
Array.RemoveValue("students", "grade")      # remove one entry
Array.GetAllIndices("students")             # {1: "name", 2: "age", ...}  (1-based)
Array.IsArray(some_value)                   # True if it's a dict or list
```

You can also pass a dict directly instead of a name:

```python
Array.SetValue("cart", "item1", "apple")
data = {"item1": "apple"}
Array.ContainsIndex(data, "item1")          # True
```

**Rule of thumb:** use Python lists for ordered collections (scores, names in a
loop) and the `Array` object when you want Small Basic-style named storage.

---

## 8. Decisions and loops

This is normal Python — `if`, `for`, `while`.

### if / elif / else

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
```

### for loops

```python
for i in range(1, 6):          # 1, 2, 3, 4, 5
    TextWindow.WriteLine(i)

for name in ["Alice", "Bob", "Carol"]:
    TextWindow.WriteLine("Hello " + name)

for i in range(10, 0, -2):     # 10, 8, 6, 4, 2 (step -2)
    TextWindow.WriteLine(i)
```

### while loops

```python
i = 0
while i < 5:
    TextWindow.WriteLine("count " + str(i))
    i += 1
```

### break and continue

```python
for i in range(1, 100):
    if i % 2 == 0:
        continue          # skip even numbers
    if i > 7:
        break             # stop at 9
    TextWindow.WriteLine(i)
```

---

## 9. Subroutines (functions)

Define reusable blocks of code with `def`, then call them:

```python
def say_hello(name):
    TextWindow.WriteLine("Hello, " + name + "!")

def add(a, b):
    return a + b

say_hello("Alice")
result = add(3, 4)          # 7
TextWindow.WriteLine(str(result))
```

Functions can return values, take defaults, etc. — everything normal Python
supports:

```python
def roll_dice(sides=6):
    return Math.GetRandomNumber(sides)

TextWindow.WriteLine("You rolled a " + str(roll_dice()))
```

---

## 10. Drawing — `GraphicsWindow`

`GraphicsWindow` is a tkinter canvas window. **Always call `GraphicsWindow.Show()`
before drawing**, and `GraphicsWindow.Wait()` at the end to keep it open (see
[section 24](#24-keeping-windows-open--wait-and-friends)).

### Set up the window

```python
GraphicsWindow.Title = "My Drawing"
GraphicsWindow.Width = 600
GraphicsWindow.Height = 400
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Left = 100
GraphicsWindow.Top = 100
GraphicsWindow.CanResize = True
GraphicsWindow.Show()
```

### Drawing state (colors, pens, fonts)

```python
GraphicsWindow.BrushColor = "Red"      # fill color for shapes
GraphicsWindow.PenColor = "DarkBlue"   # outline color
GraphicsWindow.PenWidth = 4            # outline thickness
GraphicsWindow.FontName = "Consolas"
GraphicsWindow.FontSize = 20
GraphicsWindow.FontBold = True
GraphicsWindow.FontItalic = False
```

Colors can be named colors (`"Red"`, `"DarkGreen"`, ...) or a hex value returned
by the color helpers:

```python
GraphicsWindow.GetRandomColor()            # e.g. "#4a6bd1"
GraphicsWindow.GetColorFromRGB(255, 128, 0)   # "#ff8000"
```

### Shapes

```python
# Rectangles and ellipses: (x, y, width, height) — x/y is the top-left corner
GraphicsWindow.DrawRectangle(20, 20, 100, 60)   # outline
GraphicsWindow.FillRectangle(140, 20, 100, 60)  # filled

GraphicsWindow.DrawEllipse(20, 100, 80, 80)     # outline circle
GraphicsWindow.FillEllipse(120, 100, 80, 80)    # filled circle

# Triangles: three corner points (x1,y1) (x2,y2) (x3,y3)
GraphicsWindow.DrawTriangle(20, 200, 70, 250, 20, 250)
GraphicsWindow.FillTriangle(120, 200, 170, 250, 120, 250)

# Lines and text
GraphicsWindow.DrawLine(20, 300, 300, 300)
GraphicsWindow.DrawText(20, 330, "Hello Graphics!")
GraphicsWindow.DrawBoundText(20, 360, 200, "This text wraps inside 200px.")
```

### Pixels, images, message box

```python
GraphicsWindow.SetPixel(400, 50, "Black")       # draw a single pixel
color = GraphicsWindow.GetPixel(400, 50)        # read a pixel's color

# Images (gif/ppm without Pillow; more formats with Pillow)
img = ImageList.LoadImage("my_picture.gif")
GraphicsWindow.DrawImage(img, 300, 200)
GraphicsWindow.DrawResizedImage(img, 300, 50, 100, 80)   # scaled copy

GraphicsWindow.ShowMessage("You win!", "Game Over")       # popup box
```

### Clear and batch

```python
GraphicsWindow.Clear()      # erase everything
```

For heavy drawing, wrap a group of calls in a batch so the screen refreshes only
once (nested batches are allowed):

```python
GraphicsWindow.BeginBatch()
for x in range(0, 500, 20):
    GraphicsWindow.BrushColor = GraphicsWindow.GetRandomColor()
    GraphicsWindow.FillRectangle(x, x % 200, 15, 15)
GraphicsWindow.EndBatch()
```

### Full drawing example

```python
from smallbasic import *

GraphicsWindow.Title = "Flag"
GraphicsWindow.Width = 300
GraphicsWindow.Height = 200
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

GraphicsWindow.BrushColor = "Red"
GraphicsWindow.FillRectangle(20, 20, 260, 60)
GraphicsWindow.BrushColor = "White"
GraphicsWindow.FillRectangle(20, 80, 260, 60)
GraphicsWindow.BrushColor = "Green"
GraphicsWindow.FillRectangle(20, 140, 260, 60)

GraphicsWindow.Wait()
```

---

## 11. Keyboard & mouse events

Event handlers are functions you assign to a property. **GraphicsWindow event
handlers take no arguments** — the library does *not* pass an event object to your
function. You read the keyboard/mouse state through the public properties
(`LastKey`, `LastText`, `MouseX`, `MouseY`) instead.

```python
def on_key():
    key = GraphicsWindow.LastKey          # e.g. "a", "Up", "Escape", "Return"
    TextWindow.WriteLine("Key pressed: " + key)
    if key == "Escape":
        GraphicsWindow.Clear()

def on_key_up():
    TextWindow.WriteLine("Key released: " + GraphicsWindow.LastKey)

def on_text_input():
    TextWindow.WriteLine("Typed: " + GraphicsWindow.LastText)

def on_mouse_down():
    TextWindow.WriteLine("Click at " + str(GraphicsWindow.MouseX) +
                         ", " + str(GraphicsWindow.MouseY))

def on_mouse_up():
    TextWindow.WriteLine("Released the mouse button.")

def on_mouse_move():
    pass   # fires continuously while the mouse moves
```

Assign them, then keep the window alive with `Wait()`:

```python
GraphicsWindow.KeyDown = on_key
GraphicsWindow.KeyUp = on_key_up
GraphicsWindow.TextInput = on_text_input
GraphicsWindow.MouseDown = on_mouse_down
GraphicsWindow.MouseUp = on_mouse_up
GraphicsWindow.MouseMove = on_mouse_move

GraphicsWindow.Show()
GraphicsWindow.Wait()
```

**Do not call `Wait()` inside a handler** — it would block the event loop.
Event handlers and timers run while the window is open; `Wait()` is what keeps
the window open so those events can fire.

---

## 12. Buttons & text boxes — `Controls`

`Controls` places real tkinter widgets **on the GraphicsWindow**. Add controls
**after** calling `GraphicsWindow.Show()`.

```python
from smallbasic import *

GraphicsWindow.Title = "Controls"
GraphicsWindow.Width = 400
GraphicsWindow.Height = 300
GraphicsWindow.Show()

button = Controls.AddButton("Click Me", 30, 30)      # returns e.g. "Button1"
clear  = Controls.AddButton("Clear", 30, 80)
textbox = Controls.AddTextBox(150, 30)               # single-line box
notes = Controls.AddMultiLineTextBox(150, 80)        # multi-line box
```

Read and write control contents by name:

```python
Controls.SetTextBoxText(textbox, "Hello")
text = Controls.GetTextBoxText(textbox)      # "Hello"

Controls.SetButtonCaption(button, "Pressed")
caption = Controls.GetButtonCaption(button)

Controls.SetSize(notes, 200, 120)
Controls.Move(button, 150, 150)
Controls.HideControl(clear)
Controls.ShowControl(clear)
Controls.Remove(clear)                        # destroy the widget
```

### Control events

`Controls.ButtonClicked` and `Controls.TextTyped` handlers take **no argument**:

```python
def on_button_clicked():
    name = Controls.LastClickedButton         # which button was clicked
    TextWindow.WriteLine(name + " was clicked!")

def on_text_typed():
    box = Controls.LastTypedTextBox           # which box was typed in
    TextWindow.WriteLine("You typed: " + Controls.GetTextBoxText(box))

Controls.ButtonClicked = on_button_clicked
Controls.TextTyped = on_text_typed

GraphicsWindow.Wait()     # required — keeps the window + widgets alive
```

### Extended controls: DropDown, Slider, ProgressBar, Table

`Controls` also offers richer widgets. Each returns a name you use to read/write it:

```python
fruits = ["Apple", "Banana", "Cherry"]
dd = Controls.AddDropDown(fruits, 20, 20)        # dropdown (pick one item)
Controls.SetSelectedDropDownItem(dd, 1)          # select by 0-based index
Controls.GetSelectedDropDownItem(dd)             # "Banana"
Controls.GetDropDownItemCount(dd)                # 3

sl = Controls.AddSlider(0, 100, 20, 60)          # slider 0..100
Controls.SetSliderValue(sl, 40)
Controls.GetSliderValue(sl)                      # 40

pb = Controls.AddProgressBar(20, 100)            # progress 0..100
Controls.SetProgressBarValue(pb, 75)             # clamped to 0..100

table = Controls.AddTable([                       # first row = headers
    ["Player", "Score"],
    ["Alice", 3400],
    ["Bob", 2200],
], 20, 160)
Controls.SetTableData(table, [["Player", "Score"], ["Carol", 5100]])
Controls.GetSelectedTableRow(table)              # 1-based row, or 0 if none
```

These extended controls fire their own events (handlers take **no argument**):

```python
def on_dropdown():
    TextWindow.WriteLine("Picked " + Controls.GetSelectedDropDownItem(dd))

def on_slider():
    TextWindow.WriteLine("Slider is " + str(Controls.GetSliderValue(sl)))

def on_table_row():
    TextWindow.WriteLine("Row " + str(Controls.GetSelectedTableRow(table)) +
                         " in " + Controls.LastSelectedTable)

Controls.DropDownSelected = on_dropdown
Controls.SliderChanged = on_slider
Controls.TableRowSelected = on_table_row
```

Use `Controls.LastChangedSlider` / `Controls.LastSelectedDropDown` /
`Controls.LastSelectedTable` when you have more than one of each widget and need
to know which one fired.

---

## 13. Timers — the `Timer` object

`Timer` calls a handler repeatedly at a fixed interval. Setting `Timer.Tick`
**auto-starts** the timer.

```python
from smallbasic import *

count = 0

def on_tick():
    global count
    count += 1
    TextWindow.WriteLine("Tick " + str(count) + " at " + Clock.Time)
    if count >= 5:
        Timer.Pause()

Timer.Interval = 1000     # milliseconds between ticks
Timer.Tick = on_tick      # starts ticking immediately

TextWindow.WriteLine("Timer running — 5 ticks, then paused.")
TextWindow.Pause()
```

Pause / resume:

```python
Timer.Pause()     # stop firing
Timer.Resume()    # start again (interval unchanged)
```

> **Note:** `Timer.Tick` handlers receive **no arguments**. The timer runs on a
> background thread — keep handlers short and do not block them. In a graphics
> program, pair the timer with `GraphicsWindow.Wait()` so the window (and its
> event loop) stays alive.

---

## 14. Turtle graphics — the `Turtle` object

A classic Logo-style turtle. Move it around; when the pen is down it draws on
the GraphicsWindow.

```python
from smallbasic import *

GraphicsWindow.Title = "Turtle"
GraphicsWindow.Show()

Turtle.Speed = 8          # 1 (slow) to 10 (fast)
Turtle.Show()
Turtle.PenDown()          # start drawing
Turtle.Move(100)          # forward 100
Turtle.Turn(90)           # turn right 90 degrees
Turtle.Move(100)
Turtle.TurnRight()        # turn right 90
Turtle.TurnLeft()         # turn left 90
Turtle.Move(100)
Turtle.PenUp()            # stop drawing
Turtle.MoveTo(150, 150)   # jump to absolute coordinates
Turtle.Hide()

GraphicsWindow.Wait()
```

Readable properties:

```python
Turtle.X        # current x position
Turtle.Y        # current y position
Turtle.Angle    # current heading in degrees
```

---

## 15. Animated shapes — the `Shapes` object

`Shapes` adds objects to the GraphicsWindow and lets you move, rotate, zoom,
and **animate** them later.

```python
from smallbasic import *

GraphicsWindow.Title = "Shapes"
GraphicsWindow.Show()

rect = Shapes.AddRectangle(100, 60)
Shapes.Move(rect, 50, 50)

label = Shapes.AddText("Hello")
Shapes.SetText(label, "Updated text")              # text shapes only!
Shapes.SetOpacity(rect, 50)                # 0 (invisible) - 100 (solid)
Shapes.Rotate(rect, 45)
Shapes.Zoom(rect, 1.5, 1.5)                # scale x and y
Shapes.Animate(rect, 400, 300, 2000)       # smoothly move over 2 seconds

left = Shapes.GetLeft(rect)                # current x
top  = Shapes.GetTop(rect)                 # current y
opacity = Shapes.GetOpacity(rect)

Shapes.HideShape(rect)
Shapes.ShowShape(rect)
Shapes.Remove(rect)
```

Other shape factories:

```python
Shapes.AddEllipse(80, 80)
Shapes.AddTriangle(10, 10, 50, 10, 30, 50)
Shapes.AddLine(10, 100, 200, 100)
Shapes.AddText("Hello")
Shapes.AddImage("my_picture.gif")
```

---

## 16. Sound — the `Sound` object

### System sounds (non-blocking and blocking)

```python
Sound.PlayClick()          Sound.PlayClickAndWait()
Sound.PlayChime()          Sound.PlayChimeAndWait()
Sound.PlayChimes()         Sound.PlayChimesAndWait()
Sound.PlayBellRing()       Sound.PlayBellRingAndWait()
```

### Play a music note string

```python
Sound.PlayMusic("O4 L4 C D E F G A B C5")
```

### Play a file with pause / resume

```python
Sound.Play("C:/music/song.wav")      # async (non-blocking)
Sound.Pause()
Program.Delay(1000)
Sound.Resume()
Sound.Stop()

Sound.PlayAndWait("song.wav")        # blocking — plays to the end
```

### WAV playback with position tracking (v1.2.0)

```python
Sound.WavFile = "C:/music/song.wav"     # set the file (loads its metadata)
Sound.WavDuration                       # total seconds (read-only)
Sound.WavPlay()                         # play / resume
Sound.WavPause()                        # pause, remembering position
Sound.WavStop()                         # stop, reset to 0
Sound.WavPlayAndWait()                  # play synchronously
Sound.PlayPosition                      # current position in seconds
Sound.WavPlaying                        # True while playing (read-only)
```

---

## 17. Files — the `File` object

Read, write, and manage text files. Write/append methods return `"SUCCESS"` or
`"FAILED"`; on failure, check `File.LastError`.

```python
path = "C:/temp/notes.txt"

File.WriteContents(path, "Hello file!")          # overwrite -> "SUCCESS"
File.AppendContents(path, "\nAnother line")      # add to the end
contents = File.ReadContents(path)               # whole file as one string
line2 = File.ReadLine(path, 2)                   # second line ("Another line")

File.InsertLine(path, 1, "First line")           # insert at line 1
File.CopyFile(path, "C:/temp/notes_copy.txt")
File.DeleteFile("C:/temp/notes_copy.txt")

File.CreateDirectory("C:/temp/mydir")
File.DeleteDirectory("C:/temp/mydir")
```

Listing a directory returns a 1-based dict (like Small Basic):

```python
files = File.GetFiles("C:/temp")          # {1: "a.txt", 2: "b.txt", ...}
dirs  = File.GetDirectories("C:/temp")    # {1: "subdir", ...}
```

Temp paths:

```python
tmp = File.GetTemporaryFilePath()         # a random temp filename
settings = File.GetSettingsFilePath()     # a path under the user settings dir
```

> Paths use normal Windows paths. Always use forward slashes or `r"..."` raw
> strings to avoid escaping backslashes: `"C:/temp/notes.txt"`.

---

## 18. Internet — the `Network` object

HTTP helpers. All of these are `classmethod`s you can await/skip — this library
is synchronous, so simple calls just work:

```python
html = Network.GetWebPageContents("https://example.com")
path = Network.DownloadFile("https://example.com/file.zip")   # to a temp dir
```

REST-style methods (headers and params are optional dicts):

```python
resp = Network.Get("https://api.example.com/items")
resp = Network.Post("https://api.example.com/items",
                    data={"name": "widget"}, headers={"Content-Type": "application/json"})
resp = Network.Put("https://api.example.com/items/1", data={"name": "new"})
resp = Network.Delete("https://api.example.com/items/1")
resp = Network.Patch("https://api.example.com/items/1", data={"stock": 5})
```

> **Gotcha:** running a network call blocks your program until it finishes. In a
> graphics program that is fine — just don't expect the window to redraw while
> the call runs.

---

## 19. Mouse & screen — `Mouse` and `Desktop`

### Mouse

```python
x = Mouse.MouseX          # x of the cursor (screen coordinates)
y = Mouse.MouseY          # y of the cursor
if Mouse.IsLeftButtonDown:
    TextWindow.WriteLine("Left button is held")
if Mouse.IsRightButtonDown:
    TextWindow.WriteLine("Right button is held")

Mouse.HideCursor()
Mouse.ShowCursor()
```

> `Mouse.MouseX` / `Mouse.MouseY` are **screen** coordinates, not canvas
> coordinates. Inside a graphics event, use `GraphicsWindow.MouseX` /
> `GraphicsWindow.MouseY` for canvas coordinates.

### Desktop

```python
Desktop.Width        # screen width in pixels
Desktop.Height       # screen height in pixels
Desktop.SetWallPaper("C:/pictures/wallpaper.jpg")
```

---

## 20. Program utilities — the `Program` object

```python
Program.Delay(1000)          # wait 1000 ms (program keeps running)
Program.End()                # stop the program immediately
Program.ArgumentCount        # number of command-line arguments
Program.Directory            # folder the program was run from
Program.GetArgument(1)       # first command-line argument (1-based)
```

Example:

```python
# run:  python my_program.py Alice
if Program.ArgumentCount > 0:
    name = Program.GetArgument(1)
    TextWindow.WriteLine("Hello " + name + "!")
```

---

## 21. Stack — the `Stack` object

A LIFO stack of values stored under a name:

```python
Stack.PushValue("history", "page1")
Stack.PushValue("history", "page2")
Stack.PushValue("history", "page3")

Stack.GetCount("history")     # 3
Stack.PopValue("history")     # "page3"  (most recently pushed)
Stack.PopValue("history")     # "page2"
Stack.PopValue("history")     # "page1"
Stack.PopValue("history")     # ""  (empty stack)
```

---

## 22. Images — the `ImageList` object

```python
img = ImageList.LoadImage("C:/pictures/photo.gif")    # returns a name to use elsewhere
width = ImageList.GetWidthOfImage(img)
height = ImageList.GetHeightOfImage(img)

GraphicsWindow.DrawImage(img, 10, 10)                 # draw it
```

> `LoadImage` returns `""` if the file can't be loaded. Without Pillow only
> `.gif` and `.ppm` are supported; `pip install Pillow` enables most image
> formats.

---

## 23. Dictionary & translation

Word definitions and translations (uses an online API — requires internet).

```python
definition = Dictionary.GetDefinition("hello")
TextWindow.WriteLine(definition)

# Same as GetDefinition:
Dictionary.GetDefinitionEnglishToEnglish("hello")

# Translations:
Dictionary.GetDefinitionEnglishToGerman("hello")
Dictionary.GetDefinitionEnglishToFrench("hello")
Dictionary.GetDefinitionEnglishToSpanish("hello")
Dictionary.GetDefinitionEnglishToItalian("hello")
Dictionary.GetDefinitionEnglishToJapanese("hello")
Dictionary.GetDefinitionEnglishToKorean("hello")
Dictionary.GetDefinitionEnglishToSimplifiedChinese("hello")
Dictionary.GetDefinitionEnglishToTraditionalChinese("hello")
```

---

## 24. Keeping windows open — `Wait()` and friends

This is the #1 "why does my window flash and close?" question. Here is the rule:

| Situation | What to do |
|-----------|-----------|
| GraphicsWindow program (drawing, events, controls, timers) | end with **`GraphicsWindow.Wait()`** |
| Text-only console program | end with **`TextWindow.Pause()`** (or `Read()`/`ReadNumber()`) |
| GUI program that calls `Program.End()` or `Program.Delay()` only | still needs `Wait()` to show the window |
| Program that doesn't show any window | nothing needed — it just prints and exits |

### Why?

- `GraphicsWindow.Show()` opens the window, but when the script reaches its last
  line the program **ends** and the window closes. `GraphicsWindow.Wait()`
  blocks until the user closes the window, keeping everything alive.
- `GraphicsWindow.Wait()` also runs tkinter's **event loop** — this is what makes
  keyboard/mouse/button/timer events fire. Without it, your handlers never run.
- `Program.Delay(...)` sleeps the program; it does **not** keep a window open and
  does **not** process events while sleeping. Use `Wait()` for that.
- `TextWindow.Pause()` only works when the console is visible
  (`TextWindow.Show()`), so call `Show()` before `Pause()`.

### Typical graphics program skeleton

```python
from smallbasic import *

GraphicsWindow.Title = "My Game"
GraphicsWindow.Width = 640
GraphicsWindow.Height = 480
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

# ... draw things ...
# ... set up events, controls, timer ...

GraphicsWindow.Wait()   # <-- keep the window open; drive the events
```

### Typical console program skeleton

```python
from smallbasic import *

TextWindow.Show()
TextWindow.WriteLine("Hello!")
# ...
TextWindow.Pause()      # <-- keep the console open
```

---

## 25. Two complete example programs

### Example 1 — a full console program

```python
"""A small number-guessing game (console)."""
from smallbasic import *

TextWindow.Title = "Guess the Number"
TextWindow.ForegroundColor = "Cyan"
TextWindow.Show()

secret = Math.GetRandomNumber(20)
TextWindow.WriteLine("I'm thinking of a number from 1 to 20.")

for attempt in range(1, 6):
    TextWindow.WriteLine("Guess #" + str(attempt) + ":")
    guess = TextWindow.ReadNumber()

    if guess < secret:
        TextWindow.WriteLine("Too low!")
    elif guess > secret:
        TextWindow.WriteLine("Too high!")
    else:
        TextWindow.WriteLine("Correct! The number was " + str(secret) + ".")
        break
else:
    TextWindow.WriteLine("Out of tries! It was " + str(secret) + ".")

TextWindow.Pause()
```

### Example 2 — a full graphics program

```python
"""Bouncing ball with keyboard control (graphics + events + timer)."""
from smallbasic import *

ball_x = 200
ball_y = 150
ball_vx = 4
ball_vy = 3
radius = 20

GraphicsWindow.Title = "Bouncing Ball"
GraphicsWindow.Width = 500
GraphicsWindow.Height = 400
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

def on_tick():
    global ball_x, ball_y, ball_vx, ball_vy
    ball_x += ball_vx
    ball_y += ball_vy
    if ball_x - radius < 0 or ball_x + radius > GraphicsWindow.Width:
        ball_vx = -ball_vx
    if ball_y - radius < 0 or ball_y + radius > GraphicsWindow.Height:
        ball_vy = -ball_vy
    GraphicsWindow.Clear()
    GraphicsWindow.BrushColor = "DarkBlue"
    GraphicsWindow.FillEllipse(ball_x - radius, ball_y - radius,
                               radius * 2, radius * 2)

def on_key():
    if GraphicsWindow.LastKey == "Escape":
        Program.End()

Timer.Interval = 20
Timer.Tick = on_tick

GraphicsWindow.KeyDown = on_key
GraphicsWindow.Wait()
```

Run either file with `python filename.py`.

---

Happy coding! Run any of the standalone examples in the `demos/` folder too —
`01_hello_world.py`, `04_graphics_shapes.py`, `10_all_features.py`, and
`13_wav_player.py` are great starting points.

See [API_REFERENCE.md](API_REFERENCE.md) for the complete, exhaustive reference
of every method and property.
