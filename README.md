# Python Small Basic

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)]()

A Python library that mirrors the [Microsoft Small Basic](https://smallbasic-publicwebsite.azurewebsites.net/) API, making it easy for beginners — especially kids — to learn programming with a familiar, friendly interface. Everything runs using **Python's standard library only** (no external dependencies).

> **Platform:** Windows only (uses `tkinter` for GUI, `winsound` for Sound, `ctypes` for system info).

---

## Table of Contents

- [What is it?](#what-is-it)
- [Connection to Microsoft Small Basic](#connection-to-microsoft-small-basic)
- [What It Can Do](#what-it-can-do)
- [What It Cannot Do (Yet)](#what-it-cannot-do-yet)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Demos](#demos)
- [API Overview](#api-overview)
- [Differences from Microsoft Small Basic](#differences-from-microsoft-small-basic)
- [License](#license)
- [Contributing](#contributing)

---

## What is it?

Python Small Basic is a **faithful re-implementation** of the Microsoft Small Basic API in Python. It replaces the original `.exe`-based environment with standard Python, giving you:

- Full **Python syntax** and capabilities underneath
- **Type hints** and **docstrings** on every function for IDE autocomplete
- **Familiar Small Basic object names** (`TextWindow`, `GraphicsWindow`, `Turtle`, `Controls`, etc.)
- Educational simplicity for teaching programming concepts

## Connection to Microsoft Small Basic

[Microsoft Small Basic](https://smallbasic-publicwebsite.azurewebsites.net/) is a simplified programming language designed by Microsoft for beginners (ages 8–16). It uses an intentionally tiny API with objects like `TextWindow`, `GraphicsWindow`, `Turtle`, etc., to let kids create text-based programs, graphics, and games.

**Python Small Basic** is *not* a clone of the Small Basic language/compiler. Instead, it is an **API-compatible library** for Python 3 that lets you write Python code using the same object names and method signatures that Small Basic users already know. The goal is to let educators teach programming concepts in Small Basic first, then transition to Python without having to learn a completely new set of commands.

For example, in Microsoft Small Basic you'd write:

```
TextWindow.WriteLine("Hello World")
```

In Python Small Basic you write exactly the same thing:

```python
from smallbasic import TextWindow
TextWindow.WriteLine("Hello World")
```

## What It Can Do

| Object        | Capabilities                                                                 |
|---------------|------------------------------------------------------------------------------|
| **TextWindow**  | Console-style text output with colors, input (Read, ReadNumber), pause      |
| **GraphicsWindow** | Drawing shapes (rectangles, ellipses, triangles, lines, text), colors, window controls |
| **Turtle**       | Logo-style turtle graphics with Move, Turn, PenUp/PenDown, Speed, Show/Hide |
| **Controls**     | Real tkinter widgets: Button, TextBox, MultiLine Text                       |
| **Mouse**        | Get cursor position relative to the screen                                  |
| **Shapes**       | Animate and move shapes on the GraphicsWindow canvas                        |
| **Sound**        | Play tones/melodies (via `winsound`)                                        |
| **Clock**        | Current date, time, weekday, milliseconds                                   |
| **Timer**        | Interval-based event callbacks                                              |
| **Network**      | HTTP GET, POST, JSON, file downloads                                        |
| **File**         | Read, write, append text files                                              |
| **Desktop**      | Screen dimensions, available drives                                         |
| **Math**         | Trigonometry, random numbers, min/max/sum/average (with `*args`), rounding |
| **Dictionary**   | Key-value storage (Python dict wrapper)                                     |
| **Array**        | Indexed list operations                                                     |
| **Stack**        | Push/pop operations                                                         |
| **Program**      | Program.Delay, Program.End, argument access                                 |
| **ImageList**    | Load and retrieve images (uses PIL if available, else tkinter's built-in)   |
| **Text**         | Append, convert to/from uppercase, get length, get substring                 |

### Key Features

- **Real tkinter widgets** – Buttons, TextBoxes, and MultiLine text are actual tkinter GUI widgets (not just stored models).
- **Color support** – Named colors + `GetColorFromRGB(r, g, b)` + `GetRandomColor()`.
- **Fun with arguments** – `Math.Max(1, 2, 3, 4, 5)` (variadic `*args`), `TextWindow.WriteLine("a", "b", "c")`.
- **Event-driven** – `KeyDown`, `KeyUp`, `MouseDown`, `MouseUp`, `MouseMove`, `ButtonClicked`, `Timer.Tick`.
- **Full type hints** – Every function/method has typed parameters, return annotations, and docstrings.

## What It Cannot Do (Yet)

- **Flickr** – The original Small Basic `Flickr` object is omitted because the Flickr API requires an API key and OAuth. No replacement is provided.
- **ImageList.LoadImage** – Works with PIL (Pillow) if installed, or with tkinter's `.gif`/`.ppm` support only. Full image format support requires `pip install Pillow`.
- **Sound.PlayAndWait** – Not implemented (plays asynchronously only).
- **GraphicsWindow.MakeKeyFromTitle** / **GraphicsWindow.MakeKeyFromVisible** – Not implemented.
- **Controls events** – `Controls.KeyTyped` is not implemented due to focus management complexity with real widgets.
- **Desktop.SetWallpaper** – Not implemented (Windows policy restrictions).
- **Multi-touch** – Not supported; only single mouse cursor.
- **Linux/macOS** – This library is Windows-only (uses `winsound`, `ctypes` Windows APIs). Contributions for cross-platform support welcome.

## Installation

### Option 1: Install directly

```bash
pip install python-smallbasic
```

### Option 2: From source

```bash
git clone https://github.com/incredibleamir-dot/PythonBasic.git
cd PythonBasic
pip install -e .
```

### Option 3: Just copy the package

Copy the `smallbasic/` folder into your project directory. All dependencies are in the Python standard library — no `pip install` required.

### Optional: Image support

```bash
pip install Pillow
```

Without Pillow, `ImageList.LoadImage` only supports `.gif` and `.ppm` files (via tkinter's built-in PhotoImage).

### Requirements

- **Python 3.10+**
- **Windows** (7, 10, 11)
- No external packages required

## Quick Start

```python
from smallbasic import *

# --- Hello World ---
TextWindow.Title = "My Program"
TextWindow.ForegroundColor = "Cyan"
TextWindow.WriteLine("Hello, World!")
TextWindow.WriteLine("Welcome to Python Small Basic!")

# --- Draw some shapes ---
GraphicsWindow.Title = "Shapes"
GraphicsWindow.Width = 400
GraphicsWindow.Height = 300
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

GraphicsWindow.BrushColor = "Red"
GraphicsWindow.FillEllipse(10, 10, 50, 50)

# --- Turtle ---
Turtle.Show()
Turtle.Move(100)
Turtle.Turn(90)
Turtle.Move(50)

# --- Keyboard / Mouse events ---
def on_key():
    TextWindow.WriteLine(f"Key pressed: {GraphicsWindow.LastKey}")

GraphicsWindow.KeyDown = on_key

def on_click():
    TextWindow.WriteLine(f"Mouse at ({GraphicsWindow.MouseX}, {GraphicsWindow.MouseY})")

GraphicsWindow.MouseDown = on_click
```

## Demos

The `demos/` folder contains 11 runnable examples covering all features:

| # | File | Description |
|---|------|-------------|
| 1 | `01_hello_world.py` | TextWindow basics, colors, input |
| 2 | `02_text_window_io.py` | Colors, cursor, ReadNumber, varargs |
| 3 | `03_math_fun.py` | Trig, random, sum/average/min/max with *args |
| 4 | `04_graphics_shapes.py` | Rectangles, ellipses, triangles, lines, text |
| 5 | `05_turtle_drawing.py` | Turtle square, triangle, star, spiral |
| 6 | `06_controls_gui.py` | TextBox, Button, MultiLine Text |
| 7 | `07_network_rest.py` | HTTP GET, JSON, GetWebPageContents |
| 8 | `08_file_operations.py` | Read/write/append text files |
| 9 | `09_clock_timer.py` | Clock time/date + Timer events |
| 10 | `10_all_features.py` | Mouse drawing + keyboard events + controls |
| 11 | `11_loops_conditions_functions.py` | For/while loops, if/else, functions |

Run any demo with:

```bash
python demos/04_graphics_shapes.py
```

## API Overview

### TextWindow

| Method / Property | Description |
|---|---|
| `WriteLine(...)` | Write text with newline; accepts multiple args |
| `Write(...)` | Write text without newline |
| `Read()` | Read a line of text |
| `ReadNumber()` | Read a number |
| `Pause()` | Wait for ENTER key |
| `Clear()` | Clear the window |
| `ForegroundColor` | Text color (named) |
| `BackgroundColor` | Background color |
| `Title` | Window title |
| `Left`, `Top` | Window position |
| `Show()`, `Hide()` | Show / hide window |

### GraphicsWindow

| Method / Property | Description |
|---|---|
| `Show()` | Display the window |
| `Wait()` | Keep the window open until closed |
| `DrawRectangle(x, y, w, h)` | Outline rectangle |
| `FillRectangle(x, y, w, h)` | Filled rectangle |
| `DrawEllipse(x, y, w, h)` | Outline ellipse |
| `FillEllipse(x, y, w, h)` | Filled ellipse |
| `DrawTriangle(x1,y1, x2,y2, x3,y3)` | Outline triangle |
| `FillTriangle(x1,y1, x2,y2, x3,y3)` | Filled triangle |
| `DrawLine(x1, y1, x2, y2)` | Line |
| `DrawText(x, y, text)` | Text |
| `Clear()` | Clear canvas |
| `GetColorFromRGB(r, g, b)` | Create color string |
| `GetRandomColor()` | Random color string |
| `Width`, `Height` | Window size |
| `BrushColor`, `PenColor`, `PenWidth` | Drawing state |
| `FontName`, `FontSize`, `FontBold`, `FontItalic` | Font state |
| `BackgroundColor` | Canvas background |
| `Title` | Window caption |
| `KeyDown`, `KeyUp`, `MouseDown`, `MouseUp`, `MouseMove` | Events |
| `LastKey`, `LastText` | Latest keyboard input |
| `MouseX`, `MouseY` | Mouse position (relative to canvas) |

### Controls

| Method / Property | Description |
|---|---|
| `AddButton(caption, x, y)` | Create a Button widget |
| `AddTextBox(x, y)` | Create a single-line TextBox |
| `AddMultiLineText(x, y)` | Create a multi-line Text widget |
| `SetTextBoxText(id, text)` | Set text content |
| `GetTextBoxText(id)` | Get text content |
| `SetButtonCaption(id, text)` | Set button label |
| `GetButtonCaption(id)` | Get button label |
| `SetSize(id, w, h)` | Resize a control |
| `Move(id, x, y)` | Reposition a control |
| `ShowScrollBar(id, show)` | Show/hide scrollbar |
| `ButtonClicked` | Event: button clicked |

### Turtle

| Method / Property | Description |
|---|---|
| `Show()` | Show turtle cursor |
| `Hide()` | Hide turtle cursor |
| `Move(distance)` | Move forward |
| `Turn(angle)` | Turn right (degrees) |
| `MoveTo(x, y)` | Move to absolute position |
| `PenDown()` | Start drawing |
| `PenUp()` | Stop drawing |
| `Speed` | Animation speed (1-10) |
| `Angle` | Current heading |


### Math

| Method | Description |
|---|---|
| `Sin(deg)`, `Cos(deg)`, `Tan(deg)` | Trigonometry (degrees) |
| `Floor(n)`, `Ceiling(n)`, `Round(n)` | Rounding |
| `Abs(n)` | Absolute value |
| `Max(*args)` | Maximum (variadic) |
| `Min(*args)` | Minimum (variadic) |
| `Sum(*args)` | Sum (variadic) |
| `Average(*args)` | Average (variadic) |
| `GetRandomNumber(max)` | Random integer 1..max |
| `Remainder(a, b)` | Modulo |
| `SquareRoot(n)` | Square root |
| `Pi` | Constant (3.14159...) |

### Shapes

| Method | Description |
|---|---|
| `AddRectangle(w, h)` | Create animated shape |
| `AddEllipse(w, h)` | Create animated shape |
| `AddTriangle(x1,y1,x2,y2,x3,y3)` | Create animated shape |
| `AddLine(x1,y1,x2,y2)` | Create animated shape |
| `AddImage(url)` | Add image shape |
| `Move(id, x, y)` | Animate (delta-based) |
| `Rotate(id, angle)` | Rotate shape |
| `Zoom(id, scale)` | Scale shape |
| `Animate(id, x, y, duration)` | Smooth animation |
| `Remove(id)` | Delete shape |
| `SetText(id, text)` | Set text on shape |

### Network

| Method | Description |
|---|---|
| `Get(url)` | HTTP GET (returns JSON) |
| `Post(url, data)` | HTTP POST (sends JSON, returns JSON) |
| `GetWebPageContents(url)` | Download raw text |
| `DownloadFile(url, path)` | Download binary file |

### More Objects

- **Clock** – `Time`, `Date`, `Year`, `Month`, `Day`, `WeekDay`, `Hour`, `Minute`, `Second`, `ElapsedMilliseconds`
- **Timer** – `Interval`, `Tick` (event), `Pause()`, `Resume()`
- **Dictionary** – `SetValue(key, value)`, `GetValue(key)`, `ContainsKey(key)`, `GetAllKeys()`
- **Array** – `GetValue(index)`, `SetValue(index, value)`, `ContainsKey(index)`, `GetAllIndices()`
- **Stack** – `PushValue(key, value)`, `PopValue(key)`, `ContainsKey(key)`, `GetCount(key)`
- **Program** – `Delay(ms)`, `End()`, `GetArgument(index)`, `GetProgramDirectory()`
- **Desktop** – `Width`, `Height`, `Drives()`
- **Mouse** – `MouseX`, `MouseY` (screen coordinates)
- **Sound** – `Play(milliseconds)`, `PlayFrequency(freq, ms)`
- **File** – `ReadContents(path)`, `WriteContents(path, text)`, `AppendContents(path, text)`
- **ImageList** – `LoadImage(url)`, `GetImage(id)`, `SetSize(w, h)`, `GetWidth(id)`, `GetHeight(id)`
- **Text** – `GetLength(text)`, `Append(text1, text2)`, `GetSubText(text, start, length)`, `IsSubText(text, sub)`, `EndsWith(text, sub)`, `StartsWith(text, sub)`, `ConvertToUpperCase(text)`, `ConvertToLowerCase(text)`

## Differences from Microsoft Small Basic

| Aspect | Microsoft Small Basic | Python Small Basic |
|---|---|---|
| Language | Small Basic (custom BASIC-like) | Python 3 |
| Syntax | `x = 5` (no types) | `x = 5` (dynamic but Python) |
| Conditional | `If...Then...EndIf` | `if...else` (Python) |
| Loop | `For i = 1 To 10` | `for i in range(1, 11)` |
| Function | `Sub ... EndSub` | `def ...` |
| Error handling | None (just stops) | Python exceptions |
| Graphics | Built-in renderer | `tkinter.Canvas` |
| Sound | Built-in audio | `winsound` |
| Libraries | Limited built-in only | Full Python ecosystem |
| IDE | Custom IDE with IntelliSense | Any Python IDE (VS Code, PyCharm) |
| Platform | Windows | Windows only (currently) |
| Image support | Built-in | Requires Pillow for most formats |
| Flickr | Included | Omitted (needs API key) |
| Events | `GraphicsWindow.MouseDown = OnMouseDown` | Same syntax (Python callbacks) |
| Object model | Properties assignment | Metaclass + properties |
| Multiline text | Controls.MultiLineTextBox | Controls.AddMultiLineText |

## License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

You are free to:
- Use it in any project (personal, educational, commercial)
- Modify and improve it
- Distribute it
- Sell it
- Use it for teaching

## Contributing

Contributions are welcome! Areas that need help:

- **Cross-platform support** (Linux/macOS) – replace `winsound` with other audio backends
- **Better Controls events** – `Controls.KeyTyped`, `Controls.TextChanged`
- **Widget positioning** – Support for `Controls.SetSize`, `Controls.Move`, etc.
- **More demos** – Games, animations, interactive examples
- **Documentation** – Tutorials, translations

Please open an issue or pull request on GitHub.
