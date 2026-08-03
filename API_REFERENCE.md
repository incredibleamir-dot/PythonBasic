# Python Small Basic — API Reference Guide

> **Version 1.5.0** | Windows-only (uses `winsound`, `ctypes`, `tkinter`)

---

## Table of Contents

1. [TextWindow](#textwindow) — Console input/output
2. [Text](#text) — String manipulation
3. [Math](#math) — Mathematical operations
4. [Clock](#clock) — System date & time
5. [Program](#program) — Program control & arguments
6. [Array](#array) — Named key-value stores
7. [Stack](#stack) — LIFO data structure
8. [Desktop](#desktop) — Screen dimensions & wallpaper
9. [File](#file) — File & directory operations
10. [Network](#network) — HTTP requests & file downloads
11. [Dictionary](#dictionary) — Definitions & translations
12. [Mouse](#mouse) — Cursor position & button state
13. [Sound](#sound) — System sounds, audio files & WAV playback
14. [Timer](#timer) — Repeating interval callbacks
15. [ImageList](#imagelist) — Load & inspect images
16. [Keywords](#keywords) — Small Basic keyword reference
17. [GraphicsWindow](#graphicswindow) — Drawing, text, images & events
18. [Shapes](#shapes) — Add, move, rotate & animate shapes
19. [Turtle](#turtle) — Logo-style turtle graphics
20. [Controls](#controls) — Buttons, text boxes & extended widgets

---

## TextWindow

Console-based text input/output with color support. Calls are class-level.

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `Show()` | `() -> None` | Makes the text window visible and applies colors/title |
| `Hide()` | `() -> None` | Hides the console window |
| `Clear()` | `() -> None` | Clears the console screen |
| `WriteLine(...)` | `(*args) -> None` | Prints values separated by spaces, followed by a newline |
| `Write(...)` | `(*args) -> None` | Prints values without a trailing newline |
| `Read()` | `() -> str` | Reads a line of text input |
| `ReadNumber()` | `() -> float` | Reads a number (repeats until valid) |
| `ReadKey()` | `() -> str` | Reads a single keypress (non-blocking on Windows using `msvcrt`) |
| `Pause()` | `() -> None` | Shows "Press ENTER to continue..." and waits |
| `PauseIfVisible()` | `() -> None` | Like `Pause()` but only if the window is visible |
| `PauseWithoutMessage()` | `() -> None` | Waits for ENTER without any prompt |
| `VerifyAccess()` | `() -> None` | Placeholder — does nothing |

### Properties

| Property | Type | Get | Set | Description |
|----------|------|-----|-----|-------------|
| `Title` | `str` | ✓ | ✓ | Console window title (calls `SetConsoleTitleW`) |
| `ForegroundColor` | `str` | ✓ | ✓ | Text color name (`"White"`, `"Red"`, `"Green"`, etc.) |
| `BackgroundColor` | `str` | ✓ | ✓ | Background color name |
| `Left` | `int` | ✓ | ✓ | Left position of the console window |
| `Top` | `int` | ✓ | ✓ | Top position of the console window |
| `CursorLeft` | `int` | ✓ | ✓ | Cursor column (stub — always returns 0) |
| `CursorTop` | `int` | ✓ | ✓ | Cursor row (stub — always returns 0) |

**Valid color names:** `Black`, `DarkBlue`, `DarkGreen`, `DarkCyan`, `DarkRed`, `DarkMagenta`, `DarkYellow`, `Gray`, `DarkGray`, `Blue`, `Green`, `Cyan`, `Red`, `Magenta`, `Yellow`, `White`

```python
TextWindow.Show()
TextWindow.Title = "My App"
TextWindow.ForegroundColor = "Yellow"
TextWindow.WriteLine("Hello", "World")    # prints "Hello World"
name = TextWindow.Read()
```

---

## Text

Static string manipulation methods. All methods are class-level.

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `Append(t1, t2)` | `(str, str) -> str` | Concatenated string | Joins two text values |
| `GetLength(text)` | `(str) -> int` | Character count | Length of the string |
| `IsSubText(text, sub)` | `(str, str) -> bool` | `True`/`False` | Checks if `sub` is found in `text` |
| `EndsWith(text, sub)` | `(str, str) -> bool` | `True`/`False` | Checks suffix |
| `StartsWith(text, sub)` | `(str, str) -> bool` | `True`/`False` | Checks prefix |
| `GetSubText(text, start, length)` | `(str, int, int) -> str` | Substring | Extracts `length` chars starting at 1-based `start` |
| `GetSubTextToEnd(text, start)` | `(str, int) -> str` | Substring | Extracts from 1-based `start` to end |
| `GetIndexOf(text, sub)` | `(str, str) -> int` | 1-based index (0 if not found) | Finds first occurrence of `sub` |
| `ConvertToUpperCase(text)` | `(str) -> str` | Uppercase string | Converts to upper case |
| `ConvertToLowerCase(text)` | `(str) -> str` | Lowercase string | Converts to lower case |
| `GetCharacter(code)` | `(int) -> str` | Single character | Returns character for ASCII/Unicode code |
| `GetCharacterCode(char)` | `(str) -> int` | Integer code | Returns ASCII/Unicode code of first character |

```python
Text.Append("ab", "c")                    # "abc"
Text.GetSubText("hello", 2, 3)            # "ell"
Text.GetIndexOf("hello world", "world")   # 7
Text.GetCharacter(65)                     # "A"
```

---

## Math

Static mathematical functions and constants.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `Pi` | `float` | 3.14159… |

### Methods

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `Abs(x)` | `(Number) -> Number` | Absolute value | `abs(x)` |
| `Ceiling(x)` | `(Number) -> int` | Ceiling | `math.ceil(x)` |
| `Floor(x)` | `(Number) -> int` | Floor | `math.floor(x)` |
| `Round(x)` | `(Number) -> int` | Nearest integer | `round(x)` |
| `Sin(deg)` | `(Number) -> float` | Sine of angle in degrees | |
| `Cos(deg)` | `(Number) -> float` | Cosine of angle in degrees | |
| `Tan(deg)` | `(Number) -> float` | Tangent of angle in degrees | |
| `ArcSin(x)` | `(Number) -> float` | Arc sine in degrees (clamped to [-1, 1]) | |
| `ArcCos(x)` | `(Number) -> float` | Arc cosine in degrees (clamped) | |
| `ArcTan(x)` | `(Number) -> float` | Arc tangent in degrees | |
| `SquareRoot(x)` | `(Number) -> float` | `math.sqrt(x)` | |
| `Power(b, e)` | `(Number, Number) -> float` | `b ** e` | |
| `Log(x)` | `(Number) -> float` | Base-10 logarithm | |
| `NaturalLog(x)` | `(Number) -> float` | Natural logarithm (`ln(x)`) | |
| `Max(*values)` | `(*Number) -> Number` | Maximum value (0 if no args) | |
| `Min(*values)` | `(*Number) -> Number` | Minimum value (0 if no args) | |
| `Sum(*values)` | `(*Number) -> Number` | Sum of all arguments | |
| `Average(*values)` | `(*Number) -> float` | Average (0.0 if no args) | |
| `Remainder(d, v)` | `(Number, Number) -> Number` | `d % v` | |
| `GetRandomNumber(max)` | `(int) -> int` | Random integer 1…max | |
| `GetDegrees(rad)` | `(Number) -> float` | Convert radians to degrees | |
| `GetRadians(deg)` | `(Number) -> float` | Convert degrees to radians | |

```python
Math.Abs(-5)           # 5
Math.Max(10, 20, 30)   # 30
Math.Average(1, 2, 3)  # 2.0
Math.GetRandomNumber(6)  # 1..6
```

---

## Clock

Read-only system clock properties. All are class-level and evaluated live.

| Property | Type | Example | Description |
|----------|------|---------|-------------|
| `Time` | `str` | `"14:30:00"` | Current time as `HH:MM:SS` |
| `Date` | `str` | `"07/30/2026"` | Current date as `MM/DD/YYYY` |
| `Year` | `int` | `2026` | Current year |
| `Month` | `int` | `7` | Month (1–12) |
| `Day` | `int` | `30` | Day of month (1–31) |
| `WeekDay` | `str` | `"Thursday"` | Full weekday name |
| `Hour` | `int` | `14` | Hour (0–23) |
| `Minute` | `int` | `30` | Minute (0–59) |
| `Second` | `int` | `0` | Second (0–59) |
| `Millisecond` | `int` | `500` | Millisecond (0–999) |
| `ElapsedMilliseconds` | `int` | huge | ms since 1900-01-01 |

```python
print(Clock.Time)    # "14:30:00"
print(Clock.Year)    # 2026
```

---

## Program

Program execution control and command-line arguments.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `ArgumentCount` | `int` | Number of command-line arguments (excluding script name) |
| `Directory` | `str` | Current working directory (`os.getcwd()`) |

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `Delay(ms)` | `(int) -> None` | Sleep for `ms` milliseconds (blocks the main thread) |
| `End()` | `() -> None` | Exit the program (`sys.exit(0)`) |
| `GetArgument(index)` | `(int) -> str` | 1-based argument; returns `""` if out of range |

> **⚠ Delay vs Wait:** `Program.Delay()` calls `time.sleep()`, which **blocks the main thread** and prevents the GraphicsWindow from processing events (mouse clicks, keyboard events, button presses). Use `Delay()` only for:
> - TextWindow-only programs (no GraphicsWindow involved)
> - Short pauses between automated drawing commands (where no user interaction is expected)
>
> For interactive GraphicsWindow programs, use `GraphicsWindow.Wait()` to keep the window responsive. See [GraphicsWindow.Wait()](#graphicswindow) for details.

```python
if Program.ArgumentCount > 0:
    name = Program.GetArgument(1)
Program.Delay(1000)
Program.End()
```

---

## Array

Named key-value stores (wraps Python `dict`). 1-based indexing conventions.

### Methods

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `SetValue(name, index, value)` | `(str, Any, Any) -> None` | — | Sets `array[name][index] = value` |
| `GetValue(name, index)` | `(str, Any) -> Any` | Value or `""` | Gets a stored value |
| `ContainsIndex(array, index)` | `(Any, Any) -> bool` | `True`/`False` | Checks if index exists |
| `ContainsValue(array, value)` | `(Any, Any) -> bool` | `True`/`False` | Checks if value exists |
| `GetAllIndices(array)` | `(Any) -> Dict` | `{1: key1, 2: key2, …}` | Returns 1-indexed dict of all keys |
| `GetItemCount(array)` | `(Any) -> int` | Number of items | |
| `IsArray(value)` | `(Any) -> bool` | `True`/`False` | Checks if `type(v) in (dict, list)` |
| `RemoveValue(name, index)` | `(str, Any) -> None` | — | Deletes `array[name][index]` if it exists |

The `array` parameter accepts a string name (looked up in internal store) or a direct `dict`.

```python
Array.SetValue("users", "name", "Alice")
Array.SetValue("users", "age", 10)
print(Array.GetValue("users", "name"))    # "Alice"
print(Array.GetItemCount("users"))        # 2
```

---

## Stack

Named LIFO stacks. Each stack is identified by a string name.

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `PushValue(name, value)` | `(str, Any) -> None` | — | Push onto the stack |
| `PopValue(name)` | `(str) -> Any` | Top value or `""` | Pop from the stack |
| `GetCount(name)` | `(str) -> int` | Stack size | Number of items |

```python
Stack.PushValue("s", "first")
Stack.PushValue("s", "second")
print(Stack.PopValue("s"))   # "second"
print(Stack.GetCount("s"))   # 1
```

---

## Desktop

Screen information and wallpaper.

| Member | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `Width` | property | `int` | Screen width in pixels (`GetSystemMetrics(0)`) |
| `Height` | property | `int` | Screen height in pixels (`GetSystemMetrics(1)`) |
| `SetWallPaper(path)` | `(str) -> None` | — | Sets desktop wallpaper (`SystemParametersInfoW`) |

```python
w = Desktop.Width
h = Desktop.Height
```

---

## File

File system operations. Most methods return `"SUCCESS"` or `"FAILED"` (except readers).

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `ReadContents(path)` | `(str) -> str` | File contents or `"FAILED"` | Reads entire file |
| `WriteContents(path, text)` | `(str, str) -> str` | `"SUCCESS"`/`"FAILED"` | Writes text, replaces existing |
| `AppendContents(path, text)` | `(str, str) -> str` | `"SUCCESS"`/`"FAILED"` | Appends to end of file |
| `ReadLine(path, line)` | `(str, int) -> str` | Line text or `""`/`"FAILED"` | Reads 1-based line number |
| `WriteLine(path, line, text)` | `(str, int, str) -> str` | `"SUCCESS"`/`"FAILED"` | Overwrites a specific line |
| `InsertLine(path, line, text)` | `(str, int, str) -> str` | `"SUCCESS"`/`"FAILED"` | Inserts line without overwriting |
| `CopyFile(src, dst)` | `(str, str) -> str` | `"SUCCESS"`/`"FAILED"` | Copies file with `shutil.copy2` |
| `DeleteFile(path)` | `(str) -> str` | `"SUCCESS"`/`"FAILED"` | Deletes a file |
| `CreateDirectory(path)` | `(str) -> str` | `"SUCCESS"`/`"FAILED"` | Creates directory (including parents) |
| `DeleteDirectory(path)` | `(str) -> str` | `"SUCCESS"`/`"FAILED"` | Recursively deletes directory |
| `GetFiles(path)` | `(str) -> Dict` | 1-indexed dict of paths or `"FAILED"` | Lists files in a directory |
| `GetDirectories(path)` | `(str) -> Dict` | 1-indexed dict of paths or `"FAILED"` | Lists subdirectories |
| `GetTemporaryFilePath()` | `() -> str` | Full temp file path or `""` | Creates a temp file (caller should delete) |
| `GetSettingsFilePath()` | `() -> str` | `"settings.txt"` in CWD | Returns a fixed settings path |

### Property

| Property | Type | Description |
|----------|------|-------------|
| `LastError` | `str` | Last error message (set on failure) |

```python
File.WriteContents("data.txt", "Hello")
content = File.ReadContents("data.txt")   # "Hello"
File.AppendContents("data.txt", " World")
```

---

## Network

HTTP client for REST APIs and file downloads.

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `GetWebPageContents(url)` | `(str) -> str` | HTML/text or error | Simple GET for web pages |
| `DownloadFile(url)` | `(str) -> str` | Local path or error | Downloads to temp directory |
| `Get(url, headers?, params?)` | `(str, dict?, dict?) -> str` | Response body | REST GET |
| `Post(url, data?, headers?, as_json?)` | `(str, any?, dict?, bool?) -> str` | Response body | REST POST |
| `Put(url, data?, headers?, as_json?)` | `(str, any?, dict?, bool?) -> str` | Response body | REST PUT |
| `Delete(url, headers?)` | `(str, dict?) -> str` | Response body | REST DELETE |
| `Patch(url, data?, headers?, as_json?)` | `(str, any?, dict?, bool?) -> str` | Response body | REST PATCH |

- `data` can be a `dict` (sent as JSON or form-encoded) or a raw `str`
- `as_json=True` sends JSON (default); `as_json=False` sends form-encoded
- `headers` are merged with the default `User-Agent`
- `params` (for `Get` only) are appended as query string

```python
html = Network.GetWebPageContents("https://example.com")
result = Network.Post("https://api.example.com/data", {"key": "value"})
path = Network.DownloadFile("https://example.com/file.zip")
```

---

## Dictionary

Online English dictionary and translation service.

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `GetDefinition(word)` | `(str) -> str` | English definition | Uses DictionaryAPI.dev |
| `GetDefinitionEnglishToEnglish(word)` | `(str) -> str` | Same as `GetDefinition` | |
| `GetDefinitionEnglishToSpanish(word)` | `(str) -> str` | Spanish translation | MyMemory API |
| `GetDefinitionEnglishToFrench(word)` | `(str) -> str` | French translation | |
| `GetDefinitionEnglishToGerman(word)` | `(str) -> str` | German translation | |
| `GetDefinitionEnglishToItalian(word)` | `(str) -> str` | Italian translation | |
| `GetDefinitionEnglishToJapanese(word)` | `(str) -> str` | Japanese translation | |
| `GetDefinitionEnglishToKorean(word)` | `(str) -> str` | Korean translation | |
| `GetDefinitionEnglishToSimplifiedChinese(word)` | `(str) -> str` | Simplified Chinese | |
| `GetDefinitionEnglishToTraditionalChinese(word)` | `(str) -> str` | Traditional Chinese | |

```python
print(Dictionary.GetDefinition("hello"))
print(Dictionary.GetDefinitionEnglishToSpanish("hello"))
```

---

## Mouse

Cursor position, button state, and cursor visibility. All class-level.

### Properties

| Property | Type | Get | Set | Description |
|----------|------|-----|-----|-------------|
| `MouseX` | `int` | ✓ | ✓ | Cursor X (screen coords, `GetCursorPos`/`SetCursorPos`) |
| `MouseY` | `int` | ✓ | ✓ | Cursor Y (screen coords) |
| `IsLeftButtonDown` | `bool` | ✓ | — | Left button state (`GetAsyncKeyState(0x01) & 0x8000`) |
| `IsRightButtonDown` | `bool` | ✓ | — | Right button state (`GetAsyncKeyState(0x02) & 0x8000`) |

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `HideCursor()` | `() -> None` | Hides cursor (`ShowCursor(False)`) |
| `ShowCursor()` | `() -> None` | Shows cursor (`ShowCursor(True)`) |

```python
x = Mouse.MouseX
Mouse.MouseX = 500       # set cursor position
if Mouse.IsLeftButtonDown:
    print("Left button pressed")
```

---

## Sound

System sounds, audio file playback, and WAV playback with position tracking.

### System Sounds

| Method | Description |
|--------|-------------|
| `PlayClick()` | Async system asterisk sound |
| `PlayClickAndWait()` | Sync system asterisk |
| `PlayChime()` | Async system exclamation |
| `PlayChimeAndWait()` | Sync system exclamation |
| `PlayChimes()` | Async system question sound |
| `PlayChimesAndWait()` | Sync system question |
| `PlayBellRing()` | Async system hand sound |
| `PlayBellRingAndWait()` | Sync system hand |
| `PlayMusic(notes)` | Beep-based music (async thread) |

### Audio File Playback

| Method | Signature | Description |
|--------|-----------|-------------|
| `Play(path)` | `(str) -> None` | Play WAV (async) or open MP3/WMA via `os.startfile` |
| `PlayAndWait(path)` | `(str) -> None` | Play WAV (sync) or estimate duration for other formats |
| `Pause()` | `() -> None` | Pause playback (uses `SND_PURGE`) |
| `Resume()` | `() -> None` | Resume from pause |
| `Stop()` | `() -> None` | Stop and clear current file |

### WAV Playback (v1.2.0)

Properties and methods for playing WAV files with position-tracked pause/resume.

| Member | Type | Description |
|--------|------|-------------|
| `WavFile` | property (get/set) | Path to WAV file. Setting it loads header metadata (duration, sample rate) |
| `WavDuration` | property (read-only) | Total duration of loaded WAV in seconds (`float`) |
| `PlayPosition` | property (read-only) | Current playback position in seconds (`float`). Updates live during play |
| `WavPlaying` | property (read-only) | `True` while WAV audio is currently playing (`bool`) |
| `WavPlay()` | method | Play from beginning or resume from paused position |
| `WavPause()` | method | Pause and save current position |
| `WavStop()` | method | Stop and reset position to 0 |
| `WavPlayAndWait()` | method | Play synchronously (blocking, resets position to 0) |

**Implementation notes:**
- Uses a temp sub-WAV file for position-tracked resume (avoids `SND_MEMORY` GC issues)
- WAV must be mono or stereo 16-bit PCM (standard)
- `WavPlayAndWait()` uses synchronous `PlaySound` for accurate timing

```python
# WAV player example
Sound.WavFile = "sample-speech-1m.wav"
print(f"Duration: {Sound.WavDuration:.2f}s")    # 60.00s
Sound.WavPlay()                                   # start playback
if Sound.WavPlaying:                              # is it playing?
    pos = Sound.PlayPosition                      # current position
Sound.WavPause()                                  # pause
Sound.WavPlay()                                   # resume from pause
Sound.WavStop()                                   # stop & reset
Sound.WavPlayAndWait()                            # play & block
```

---

## Timer

Repeating interval timer with a background thread.

### Properties

| Property | Type | Get | Set | Description |
|----------|------|-----|-----|-------------|
| `Interval` | `int` | ✓ | ✓ | Interval in milliseconds (default 1000). Minimum effective sleep is 10ms |
| `Tick` | `callable` | ✓ | ✓ | Callback function. Setting it auto-starts the timer |

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `Pause()` | `() -> None` | Pause tick events (thread stays alive) |
| `Resume()` | `() -> None` | Resume tick events; starts thread if not alive |

**Note:** Tick callbacks run in a background daemon thread. Exceptions are logged via `logging.getLogger(__name__)`. Avoid blocking for long periods in callbacks.

```python
def on_tick():
    print("Tick!")

Timer.Interval = 1000    # 1 second
Timer.Tick = on_tick     # starts automatically
# ... later ...
Timer.Pause()
```

---

## ImageList

Load images from disk and query dimensions.

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `LoadImage(path)` | `(str) -> str` | Image name (basename) or `""` on failure | Loads image; tries PIL first, falls back to `tk.PhotoImage` |
| `GetWidthOfImage(name)` | `(str) -> int` | Width in pixels or `0` | |
| `GetHeightOfImage(name)` | `(str) -> int` | Height in pixels or `0` | |

```python
img = ImageList.LoadImage("C:/photo.png")
w = ImageList.GetWidthOfImage(img)
h = ImageList.GetHeightOfImage(img)
```

---

## Keywords

Documentation placeholder — no methods or properties. Provides a docstring that maps Small Basic keywords to Python equivalents:

| Small Basic | Python |
|-------------|--------|
| `For` | `for i in range(start, end+1, step):` |
| `If` | `if condition:` |
| `While` | `while condition:` |
| `Sub` | `def function_name():` |
| `And` / `Or` | `and` / `or` |

---

## GraphicsWindow

Tkinter-based drawing canvas with mouse/keyboard events.

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `Show()` | `() -> None` | Creates & shows the graphics window |
| `Hide()` | `() -> None` | Hides the window (`withdraw`) |
| `Wait()` | `() -> None` | Enters `mainloop` — keeps the window open and responsive until closed |
| `Clear()` | `() -> None` | Deletes all canvas items |
| `BeginBatch()` | `() -> None` | Start deferred rendering — display updates are suppressed until `EndBatch()` |
| `EndBatch()` | `() -> None` | Flush deferred updates accumulated since `BeginBatch()` |
| `ShowMessage(text, title)` | `(str, str) -> None` | Shows a `tk.messagebox.showinfo` dialog |

**Drawing methods** (all coordinates are relative to the canvas):

| Method | Signature | Description |
|--------|-----------|-------------|
| `DrawRectangle(x, y, w, h)` | `(int, int, int, int) -> None` | Outline rectangle |
| `FillRectangle(x, y, w, h)` | `(int, int, int, int) -> None` | Filled rectangle |
| `DrawEllipse(x, y, w, h)` | `(int, int, int, int) -> None` | Outline ellipse |
| `FillEllipse(x, y, w, h)` | `(int, int, int, int) -> None` | Filled ellipse |
| `DrawTriangle(x1,y1, x2,y2, x3,y3)` | `(int, int, int, int, int, int) -> None` | Outline triangle |
| `FillTriangle(x1,y1, x2,y2, x3,y3)` | `(int, int, int, int, int, int) -> None` | Filled triangle |
| `DrawLine(x1, y1, x2, y2)` | `(int, int, int, int) -> None` | Line segment |
| `DrawText(x, y, text)` | `(int, int, str) -> None` | Text label (anchor NW) |
| `DrawBoundText(x, y, width, text)` | `(int, int, int, str) -> None` | Text wrapped to width |
| `DrawImage(image_name, x, y)` | `(str, int, int) -> None` | Image from ImageList |
| `DrawResizedImage(name, x, y, w, h)` | `(str, int, int, int, int) -> None` | Scaled image |
| `SetPixel(x, y, color)` | `(int, int, str) -> None` | Draws a 1×1 line in `color` |
| `GetPixel(x, y)` | `(int, int) -> str` | Returns color string of nearest item, or background color |
| `GetRandomColor()` | `() -> str` | Random hex color `#RRGGBB` |
| `GetColorFromRGB(r, g, b)` | `(int, int, int) -> str` | Hex color from 0–255 values |

**Batch rendering:** Use `BeginBatch()` / `EndBatch()` to group many drawing calls into a single display refresh. This avoids redundant window updates and can significantly improve throughput when drawing hundreds of shapes:

```python
GraphicsWindow.BeginBatch()
for i in range(100):
    GraphicsWindow.DrawRectangle(i * 50, 0, 40, 30)
GraphicsWindow.EndBatch()   # single display refresh
```

Batches can be nested. Each `BeginBatch()` must be paired with a matching `EndBatch()`. The display is updated only when the outermost batch ends.

### Properties

All are class-level on `GraphicsWindow`.

| Property | Type | Get | Set | Description |
|----------|------|-----|-----|-------------|
| `Title` | `str` | ✓ | ✓ | Window title |
| `Width` | `int` | ✓ | ✓ | Canvas width (pixels) |
| `Height` | `int` | ✓ | ✓ | Canvas height (pixels) |
| `Left` | `int` | ✓ | ✓ | Window left position |
| `Top` | `int` | ✓ | ✓ | Window top position |
| `CanResize` | `bool` | ✓ | ✓ | Whether the window is resizable |
| `BackgroundColor` | `str` | ✓ | ✓ | Canvas background color |
| `BrushColor` | `str` | ✓ | ✓ | Fill color for shapes |
| `PenColor` | `str` | ✓ | ✓ | Outline/text color |
| `PenWidth` | `int` | ✓ | ✓ | Outline width (pixels) |
| `FontName` | `str` | ✓ | ✓ | Font family name |
| `FontSize` | `int` | ✓ | ✓ | Font size (points) |
| `FontBold` | `bool` | ✓ | ✓ | Bold text |
| `FontItalic` | `bool` | ✓ | ✓ | Italic text |
| `LastKey` | `str` | ✓ | — | Last key pressed (`keysym` string) |
| `LastText` | `str` | ✓ | — | Last character typed |
| `MouseX` | `int` | ✓ | — | Mouse X relative to canvas |
| `MouseY` | `int` | ✓ | — | Mouse Y relative to canvas |

### Events

Set these class-level attributes to callable functions. **Handlers take no arguments** — the internal `tkinter.Event` is *not* passed. Read the state through the public properties (`LastKey`, `LastText`, `MouseX`, `MouseY`).

| Event | Callback Signature | Description |
|-------|-------------------|-------------|
| `KeyDown` | `() -> None` | Key pressed |
| `KeyUp` | `() -> None` | Key released |
| `MouseDown` | `() -> None` | Mouse button pressed |
| `MouseUp` | `() -> None` | Mouse button released |
| `MouseMove` | `() -> None` | Mouse moved |
| `TextInput` | `() -> None` | Character input |

> **Important:** For interactive GraphicsWindow programs (controls, events, mouse/keyboard), always use `GraphicsWindow.Wait()` at the end instead of `Program.Delay()`. `Program.Delay()` blocks the main thread and prevents tkinter from processing events, so button clicks, key presses, and mouse events will not fire during the delay.
>
> **Pattern for interactive demos:**
> ```python
> GraphicsWindow.Show()
> # ... setup controls, events, drawings ...
> Program.Delay(500)        # brief pause (non-interactive)
> GraphicsWindow.Wait()     # interactive — keeps window responsive
> Program.End()
> ```

```python
GraphicsWindow.Title = "My Drawing"
GraphicsWindow.Width = 800
GraphicsWindow.Height = 600
GraphicsWindow.Show()

def on_key():
    key = GraphicsWindow.LastKey          # e.g. "a", "Up", "Escape"
    print(f"Key: {key}")

GraphicsWindow.KeyDown = on_key

def on_click():
    print(f"Clicked at ({GraphicsWindow.MouseX}, {GraphicsWindow.MouseY})")

GraphicsWindow.MouseDown = on_click

GraphicsWindow.DrawRectangle(50, 50, 100, 80)
GraphicsWindow.FillEllipse(200, 50, 80, 80)
GraphicsWindow.DrawText(10, 10, "Hello!")

GraphicsWindow.Wait()
```

---

## Shapes

Add, manipulate, and remove shapes on the Graphics Window canvas.

### Adding Shapes

Each `Add*` method returns a shape name string for later reference.

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `AddRectangle(w, h)` | `(int, int) -> str` | Shape name | Outline rectangle at (0,0) |
| `AddEllipse(w, h)` | `(int, int) -> str` | Shape name | Outline ellipse at (0,0) |
| `AddTriangle(x1,y1, x2,y2, x3,y3)` | `(int*6) -> str` | Shape name | Outline triangle |
| `AddLine(x1,y1, x2,y2)` | `(int, int, int, int) -> str` | Shape name | Line segment |
| `AddText(text)` | `(str) -> str` | Shape name | Text shape at (0,0) |
| `AddImage(image_name)` | `(str) -> str` | Shape name | Image from ImageList |

### Manipulation Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `Move(name, x, y)` | `(str, int, int) -> None` | Move shape to new position |
| `Rotate(name, angle)` | `(str, int) -> None` | Rotate shape to angle (degrees). Uses 2D rotation matrix |
| `Zoom(name, sx, sy)` | `(str, float, float) -> None` | Scale shape (0.1–20, cumulative via `canvas.scale`) |
| `Animate(name, x, y, ms)` | `(str, int, int, int) -> None` | Smooth move over `ms` milliseconds |
| `SetOpacity(name, level)` | `(str, int) -> None` | Opacity 0 (transparent) to 100 (opaque); uses stipple patterns |
| `SetText(name, text)` | `(str, str) -> None` | Update text of a text shape |
| `HideShape(name)` | `(str) -> None` | Hide the shape (`state="hidden"`) |
| `ShowShape(name)` | `(str) -> None` | Show a hidden shape |
| `Remove(name)` | `(str) -> None` | Delete shape from canvas |

### Query Methods

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `GetLeft(name)` | `(str) -> int` | X position or `0` |
| `GetTop(name)` | `(str) -> int` | Y position or `0` |
| `GetOpacity(name)` | `(str) -> int` | Opacity (0–100) or `100` |

Shapes use the current `PenColor`, `PenWidth`, `BrushColor`, `FontName`, `FontSize`, etc. from `GraphicsWindow`.

```python
rect = Shapes.AddRectangle(100, 50)
Shapes.Move(rect, 200, 150)
Shapes.Rotate(rect, 45)
Shapes.Animate(rect, 400, 300, 2000)
pos_x = Shapes.GetLeft(rect)
```

---

## Turtle

Logo-style turtle graphics. Properties support get/set. The turtle draws on the GraphicsWindow canvas.

### Properties

| Property | Type | Get | Set | Description |
|----------|------|-----|-----|-------------|
| `X` | `float` | ✓ | ✓ | X position (canvas coords) |
| `Y` | `float` | ✓ | ✓ | Y position (canvas coords) |
| `Angle` | `float` | ✓ | ✓ | Direction in degrees (0 = right, 90 = up) |
| `Speed` | `int` | ✓ | ✓ | 1 (slowest) to 10 (instant). Controls `time.sleep` delay after `Move` |

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `Show()` | `() -> None` | Makes turtle visible (creates window if needed) |
| `Hide()` | `() -> None` | Removes turtle graphics from canvas |
| `Move(distance)` | `(float) -> None` | Move forward by distance in current direction. Draws if pen is down |
| `MoveTo(x, y)` | `(float, float) -> None` | Move to absolute position; sets angle toward target |
| `Turn(angle)` | `(float) -> None` | Add angle to current direction |
| `TurnRight()` | `() -> None` | Turn 90 degrees right |
| `TurnLeft()` | `() -> None` | Turn 90 degrees left |
| `PenDown()` | `() -> None` | Start drawing on move |
| `PenUp()` | `() -> None` | Stop drawing on move |

**Note:** `MoveTo` calculates the angle to the target, so the turtle always faces the direction it's moving.

```python
Turtle.Show()
Turtle.Speed = 8
Turtle.Move(100)
Turtle.Turn(90)
Turtle.Move(50)
Turtle.PenUp()
Turtle.Move(30)
```

---

## Controls

Buttons, text boxes, and extended widgets placed on the Graphics Window.

### Methods — Standard controls

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `AddButton(caption, left, top)` | `(str, int, int) -> str` | Button name | Creates a `tk.Button` |
| `AddTextBox(left, top)` | `(int, int) -> str` | TextBox name | Creates a single-line `tk.Entry` |
| `AddMultiLineTextBox(left, top)` | `(int, int) -> str` | TextBox name | Creates a `tk.Text` widget |
| `AddMultiLineText(left, top)` | `(int, int) -> str` | TextBox name | Alias for `AddMultiLineTextBox` |
| `SetTextBoxText(name, text)` | `(str, str) -> None` | — | Sets text box content |
| `GetTextBoxText(name)` | `(str) -> str` | Current text | Gets text box content |
| `SetButtonCaption(name, caption)` | `(str, str) -> None` | — | Changes button label |
| `GetButtonCaption(name)` | `(str) -> str` | Current caption | Gets button label |
| `SetSize(name, w, h)` | `(str, int, int) -> None` | — | Resizes the control |
| `Move(name, x, y)` | `(str, int, int) -> None` | — | Moves the control |
| `Remove(name)` | `(str) -> None` | — | Destroys the control |
| `HideControl(name)` | `(str) -> None` | — | Hides control (`place_forget`) |
| `ShowControl(name)` | `(str) -> None` | — | Shows control (`place`) |

### Extended controls

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `AddDropDown(items, left, top)` | `(list, int, int) -> str` | DropDown name | A readonly combo box. `items` accepts a Python list or a Small Basic array |
| `GetSelectedDropDownItem(name)` | `(str) -> str` | Selected text | Current dropdown text (empty if none) |
| `SetSelectedDropDownItem(name, index)` | `(str, int) -> None` | — | Select an item by 0-based index |
| `GetDropDownItemCount(name)` | `(str) -> int` | Item count | Number of items |
| `GetDropDownItems(name)` | `(str) -> list` | Items | The list of items |
| `AddSlider(minimum, maximum, left, top)` | `(int, int, int, int) -> str` | Slider name | Adds a horizontal slider |
| `GetSliderValue(name)` | `(str) -> int` | Current value | Reads the slider value |
| `SetSliderValue(name, value)` | `(str, int) -> None` | — | Sets the slider value (also fires `SliderChanged`) |
| `AddProgressBar(left, top)` | `(int, int) -> str` | Bar name | Adds a determinate progress bar (0–100) |
| `GetProgressBarValue(name)` | `(str) -> int` | Current value | Reads progress value |
| `SetProgressBarValue(name, value)` | `(str, int) -> None` | — | Sets progress (clamped to 0–100) |
| `AddTable(data, left, top)` | `(2D list, int, int) -> str` | Table name | Adds a table. First row = column headers |
| `SetTableData(name, data)` | `(str, 2D list) -> None` | — | Replaces all rows |
| `GetSelectedTableRow(name)` | `(str) -> int` | 1-based row or `0` | Row currently selected |

### Properties

| Property | Type | Get | Set | Description |
|----------|------|-----|-----|-------------|
| `LastClickedButton` | `str` | ✓ | — | Name of last clicked button |
| `LastTypedTextBox` | `str` | ✓ | — | Name of last typed text box |
| `LastChangedSlider` | `str` | ✓ | — | Name of last changed slider |
| `LastSelectedDropDown` | `str` | ✓ | — | Name of last selected dropdown |
| `LastSelectedTable` | `str` | ✓ | — | Name of the table that just had a row selected |

### Events

Event handlers take **no arguments**. Use the corresponding `Last*` property to identify which widget fired, then call a getter to read its value.

| Event | Setter | Description |
|-------|--------|-------------|
| `ButtonClicked` | `Controls.ButtonClicked = callback` | Called when any button is clicked. Use `LastClickedButton` |
| `TextTyped` | `Controls.TextTyped = callback` | Called on key release in any text box. Use `LastTypedTextBox` |
| `SliderChanged` | `Controls.SliderChanged = callback` | Called when any slider changes. Use `LastChangedSlider` + `GetSliderValue` |
| `DropDownSelected` | `Controls.DropDownSelected = callback` | Called when a dropdown item is picked. Use `LastSelectedDropDown` + `GetSelectedDropDownItem` |
| `TableRowSelected` | `Controls.TableRowSelected = callback` | Called when a table row is selected. Use `LastSelectedTable` + `GetSelectedTableRow` |

```python
GraphicsWindow.Show()

def on_click():
    btn = Controls.LastClickedButton
    text = Controls.GetTextBoxText(tb)
    Controls.SetTextBoxText(output, f"{btn}: {text}")

def on_slider():
    value = Controls.GetSliderValue(Controls.LastChangedSlider)
    Controls.SetTextBoxText(output, f"Slider: {value}")

btn   = Controls.AddButton("Submit", 10, 10)
sl    = Controls.AddSlider(0, 100, 10, 60)
tb    = Controls.AddTextBox(10, 100)
output = Controls.AddMultiLineTextBox(10, 140)

Controls.ButtonClicked = on_click
Controls.SliderChanged = on_slider

GraphicsWindow.Wait()
```

### Table example

```python
table = Controls.AddTable([
    ["Player", "Score"],
    ["Alice", 3400],
    ["Bob", 2200],
], 10, 200)

def on_row():
    Controls.SetTextBoxText(output,
        Controls.LastSelectedTable + " row " +
        str(Controls.GetSelectedTableRow(table)))

Controls.TableRowSelected = on_row
```

---

## Appendix: Color Names

All color properties accept these named colors (case-insensitive matching):

`Black`, `White`, `Red`, `Green`, `Blue`, `Yellow`, `Cyan`, `Magenta`, `Gray`, `DarkGray`, `LightGray`, `DarkRed`, `DarkGreen`, `DarkBlue`, `DarkCyan`, `DarkMagenta`, `DarkYellow`, `Orange`, `Purple`, `Brown`, `Pink`, `Gold`, `Silver`, `Navy`, `Teal`, `Maroon`, `Lime`, `Aqua`, `Fuchsia`, `Olive`

Any valid Tkinter color string (`"#RRGGBB"`) also works.

---

## Appendix: Import

```python
from smallbasic import (
    Array, Clock, Controls, Desktop, Dictionary,
    File, GraphicsWindow, ImageList, Keywords,
    Math, Mouse, Network, Program, Shapes,
    Sound, Stack, Text, TextWindow, Timer, Turtle
)
# or
from smallbasic import *
```
