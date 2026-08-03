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
- [API Reference](#api-reference)
- [Differences from Microsoft Small Basic](#differences-from-microsoft-small-basic)
- [Changelog](#changelog)
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
| **GraphicsWindow** | Drawing shapes (rectangles, ellipses, triangles, lines, text), colors, batch rendering, events |
| **Turtle**       | Logo-style turtle graphics with Move, Turn, PenUp/PenDown, Speed, Show/Hide |
| **Controls**     | Real tkinter widgets: Button, TextBox, MultiLine Text, DropDown, Slider, ProgressBar, Table + events |
| **Mouse**        | Get cursor position relative to the screen, button state detection          |
| **Shapes**       | Animate, move, rotate, zoom shapes on the GraphicsWindow canvas             |
| **Sound**        | Play tones/melodies, WAV files with position-tracked pause/resume           |
| **Clock**        | Current date, time, weekday, milliseconds                                   |
| **Timer**        | Interval-based event callbacks with pause/resume                            |
| **Network**      | HTTP GET, POST, PUT, DELETE, PATCH, JSON, file downloads                    |
| **File**         | Read, write, append, copy, delete text and files and directories            |
| **Desktop**      | Screen dimensions, wallpaper setting                                        |
| **Math**         | Trigonometry, random numbers, min/max/sum/average (with `*args`), rounding |
| **Dictionary**   | Online word definitions and translations (English to 9+ languages)          |
| **Array**        | Indexed list operations                                                     |
| **Stack**        | Push/pop operations                                                         |
| **Program**      | Program.Delay, Program.End, argument access                                 |
| **ImageList**    | Load and retrieve images (uses Pillow if available, else tkinter's built-in)   |
| **Text**         | Append, convert to/from uppercase, get length, get substring                 |

### Key Features

- **Real tkinter widgets** – Buttons, TextBoxes, DropDowns, Sliders, ProgressBars and Tables are actual tkinter GUI widgets (not just stored models).
- **Control events** – `ButtonClicked`, `TextTyped`, plus `SliderChanged`, `DropDownSelected` and `TableRowSelected` for the extended controls.
- **Color support** – Named colors + `GetColorFromRGB(r, g, b)` + `GetRandomColor()`.
- **Fun with arguments** – `Math.Max(1, 2, 3, 4, 5)` (variadic `*args`), `TextWindow.WriteLine("a", "b", "c")`.
- **Event-driven** – `KeyDown`, `KeyUp`, `MouseDown`, `MouseUp`, `MouseMove`, `ButtonClicked`, `Timer.Tick`. Handlers take **no arguments** and read state via the public API (`LastKey`, `MouseX`, `MouseY`, `LastClickedButton`, …).
- **Full type hints** – Every function/method has typed parameters, return annotations, and docstrings.
- **Shape rotation** – Proper 2D rotation using rotation matrices.
- **Sound pause/resume** – Pause and resume audio playback, including position-tracked WAV playback.
- **Translation support** – Dictionary methods that actually translate words using the MyMemory API.

## What It Cannot Do (Yet)

- **Flickr** – The original Small Basic `Flickr` object is omitted because the Flickr API requires an API key and OAuth. No replacement is provided.
- **ImageList.LoadImage** – Works with PIL (Pillow) if installed, or with tkinter's `.gif`/`.ppm` support only. Full image format support requires `pip install Pillow`.
- **Controls.KeyTyped** – Not implemented due to focus management complexity with real widgets.
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

Without Pillow, `ImageList.LoadImage` only supports `.gif` and `.ppm` files (via tkinter's built-in `PhotoImage`).

### Requirements

- **Python 3.10+**
- **Windows** (7, 10, 11)
- No external packages required

## Quick Start

```python
from smallbasic import *

# --- Hello World ---
TextWindow.Title = "My Program"
TextWindow.WriteLine("Hello, World!")

# --- Draw some shapes ---
GraphicsWindow.Title = "Shapes"
GraphicsWindow.Width = 400
GraphicsWindow.Height = 300
GraphicsWindow.BackgroundColor = "Black"
GraphicsWindow.Show()

GraphicsWindow.BrushColor = "Red"
GraphicsWindow.FillEllipse(10, 10, 50, 50)

# --- Rotate a shape ---
rect = Shapes.AddRectangle(100, 50)
Shapes.Rotate(rect, 45)  # Properly rotates the shape

# --- Keyboard / Mouse events ---
# Event handlers take NO arguments. Read state via the public API.
def on_key():
    TextWindow.WriteLine(f"Key pressed: {GraphicsWindow.LastKey}")

GraphicsWindow.KeyDown = on_key

def on_click():
    TextWindow.WriteLine(f"Mouse at ({GraphicsWindow.MouseX}, {GraphicsWindow.MouseY})")

GraphicsWindow.MouseDown = on_click

# --- A button-driven counter ---
count = 0
def on_button():
    global count
    count += 1
    TextWindow.WriteLine(f"Button clicked {count} times ({Controls.LastClickedButton})")

Controls.AddButton("Click Me", 20, 20)
Controls.ButtonClicked = on_button

# --- Sound ---
Sound.Play("C:/music/track.wav")
Program.Delay(2000)
Sound.Pause()
Program.Delay(1000)
Sound.Resume()

# --- Dictionary ---
definition = Dictionary.GetDefinition("hello")
TextWindow.WriteLine(definition)

# --- Keep the window open and responsive ---
GraphicsWindow.Wait()
```

> **Important:** use `GraphicsWindow.Wait()` at the end of interactive programs. `Program.Delay()` blocks the event loop, so buttons, keys and mouse events won't fire during the sleep.

## Demos

The `demos/` folder contains runnable examples covering all features:

| # | File | Description |
|---|---|-------------|
| 1 | `demos/01_hello_world.py` | TextWindow basics, colors, input |
| 2 | `demos/02_text_window_io.py` | Colors, cursor, ReadNumber, ReadKey |
| 3 | `demos/03_math_fun.py` | Math, trig, random, *args |
| 4 | `demos/04_graphics_shapes.py` | Drawing + Shapes |
| 5 | `demos/05_turtle_drawing.py` | Turtle square, triangle, star, spiral |
| 6 | `demos/06_controls_gui.py` | TextBox, Button, events |
| 7 | `demos/07_network_rest.py` | HTTP GET, JSON |
| 8 | `demos/08_file_operations.py` | Read/write/append files |
| 9 | `demos/09_clock_timer.py` | Clock + Timer events |
| 10 | `demos/10_all_features.py` | Mouse drawing + keyboard + controls |
| 11 | `demos/11_loops_conditions_functions.py` | For/while loops, if/else, functions |
| 12 | `demos/12_fractal_tree.py` | Recursive fractal tree with Turtle |
| 13 | `demos/13_wav_player.py` | Media player (WAV/MP3) with Play/Pause/Stop/Seek |
| 14 | `demos/14_mouse_coords.py` | Live mouse X/Y via MouseMove |
| 15 | `demos/15_file_folder_picker.py` | File/folder pickers + events |
| 16 | `demos/16_bouncing_ball.py` | Bouncing ball with keyboard + timer |
| 17 | `demos/17_analog_clock.py` | Analog clock drawing |
| 18 | `demos/18_binary_converter.py` | Binary / decimal converter |
| 19 | `demos/19_brick_breaker.py` | Brick-breaker game (arrow keys) |
| 20 | `demos/20_extended_controls.py` | DropDown, Slider, ProgressBar, Table + events |
| 21 | `demos/21_live_animation.py` | Animated shapes |
| 22 | `demos/22_shape_transforms.py` | Interactive shape create/move/rotate/zoom playground |

Run any demo with:

```bash
python demos/04_graphics_shapes.py
```

> **Note:** `demos/99_all_features.py` is an older "kitchen-sink" tour of the whole
> library. It predates the "public API only" demo convention and still uses `print`,
> `os`, `time` and a few internal helpers — prefer the numbered demos above.

## Testing

Run the self-contained smoke/regression suite (no test framework required):

```bash
python test_smallbasic.py
```

The suite covers every public object plus edge cases and prints a summary at
the end (e.g. `450 / 450 checks passed`). A handful of GUI sections open hidden
tkinter windows; closing the console ends the run.

## API Reference

The full, exhaustive reference for every object, method and property lives in the dedicated **[API_REFERENCE.md](API_REFERENCE.md)** file. A beginner-friendly, step-by-step walkthrough with runnable examples — including a complete `Controls` extended-controls and event section — is in the **[TUTORIAL.md](TUTORIAL.md)**.

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
| Color | Limited | Named colors + `GetColorFromRGB` + `GetRandomColor` |
| Variadic args | No | Yes — `Math.Max(1, 2, 3)` |
| Translation | Built-in | MyMemory API |
| Object model | Properties assignment | Python properties |

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full changelog.

## License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Areas that need help:

- **Cross-platform support** (Linux/macOS) – replace `winsound` with other audio backends
- **More Controls events** – `Controls.KeyTyped`, `Controls.TextChanged`
- **More demos** – Games, animations, interactive examples
- **Documentation** – Tutorials, translations
- **Tests** – Expand test coverage

Please open an issue or pull request on GitHub.