# Changelog

All notable changes to this project will be documented in this file.

## [1.6.1] - 2026-08-03

### Fixed

- **Drawing before `GraphicsWindow.Show()` now works.** The tkinter canvas is
  created eagerly on `ensure()`, so `Shapes.Add*` / `Draw*` calls made before
  the window is shown no longer silently do nothing, and those shapes stay
  usable after `Show()`.
- **`Shapes.Rotate` no longer ignores a previous `Move`.** Rotation is now
  relative and applied around the shape's *current* canvas position, and the
  stored coordinates stay in sync, so repeated `Rotate` calls accumulate and
  a rotate after a move stays where the shape is.
- **`Mouse` no longer depends on an incidental global import.** `mouse.py` now
  imports `ctypes.wintypes` explicitly; cursor reads previously failed (and
  returned cached coordinates) when `smallbasic.sound` was not imported.
- **`Turtle.X` / `Turtle.Y` re-draw the sprite** when the turtle is visible.
- **`Sound.PlayAndWait` no longer returns immediately** for files whose
  duration could not be determined (uses a safety cap).
- **`Network.Get` query parameters** now append with `&` when the URL already
  contains a query string.
- **`Math.Round` / `Math.Remainder` semantics are now documented** (banker's
  rounding; Python `%` sign behaviour).
- **Resized-image cache is cleared** when the canvas is cleared, preventing an
  unbounded `PhotoImage` handle leak.
- **`TextWindow.CursorLeft` / `CursorTop`** are now implemented for the Windows
  console instead of returning stubs.

### Changed

- **Removed the legacy `_TkWindow` shim.** `GraphicsState` is the single source
  of truth for graphics state; the `graphics_window` metaclass now forwards
  directly to it instead of mirroring a duplicate state object.
- **Widget construction extracted into `smallbasic/_widgets.py`** (`TkWidgets`)
  so `TkBackend` only manages the window/canvas surface.
- **Added `reset()` helpers** on `Array`, `Stack`, `Shapes`, `Controls` and
  `ImageList` for stateful re-runs.
- Removed dead code: unused imports, the unimplemented `Backend.add_multi_textbox`
  interface method, the unused `GraphicsState.shown` / `GraphicsState.ButtonClicked`
  / `GraphicsState.TextTyped` attributes, and the unused
  `Renderer.get_metadata` / `get_all_objects` helpers.
- Added a `smallbasic/py.typed` marker for type-aware consumers.

### Performance

- **Coalesced the `<Motion>` event.** Rapid mouse movement no longer floods the
  Tk idle queue with one scheduled dispatch per event.
- **`Text.GetSubText` / `GetSubTextToEnd`** now return `""` for non-numeric
  start/length arguments instead of raising `ValueError`.

### Tests
- Updated the suite for the removed `GraphicsState.shown` dead attribute.
  **450 / 450 checks pass.**

### Added

- **File and folder pickers** on the `Controls` object — native Windows dialogs
  with no extra dependencies:
  - `Controls.AddFilePicker(caption, left, top)` — button that opens a file-open dialog.
  - `Controls.AddFolderPicker(caption, left, top)` — button that opens a folder dialog.
  - `Controls.GetPickerPath(name)` — last path chosen by a specific picker.
  - `Controls.LastPickedFile` / `Controls.LastPickedFolder` — last chosen path.
  - `Controls.FilePicked` / `Controls.FolderPicked` — no-argument events fired after a pick.

### Changed

- **Unified audio-file playback on `Sound`** — the separate WAV API
  (`WavFile` / `WavDuration` / `WavPlay` / `WavPause` / `WavStop` / `WavPlayAndWait` /
  `WavPlaying`) is removed and folded into one API that handles **WAV and MP3**.
  Files are played in-process through the Windows Media Control Interface (MCI) via
  the standard library (`ctypes` + `winmm`), so no external decoder is needed.
  - `Sound.Play(path=None)` — play a WAV/MP3 async, or play/resume the open file.
  - `Sound.PlayAndWait(path=None)` — play to the end (blocking).
  - `Sound.Open(path)` — open a file (returns `bool`), replaces the old `WavFile`.
  - `Sound.Pause()` / `Sound.Resume()` / `Sound.Stop()` / `Sound.Seek(seconds)`.
  - `Sound.CurrentFile` / `Sound.Duration` / `Sound.PlayPosition` / `Sound.IsPlaying`
    (replaces `WavPlaying`).

### Fixed

- **MP3 files previously opened an external player** via `os.startfile()` with no
  control. They are now played in-process with full play/pause/seek/progress.
- **`Sound.PlayPosition` now works from Timer callbacks.** MCI reports a position
  of `0` when queried from a background thread, which froze the elapsed-time /
  progress-bar readouts in `demos/13_wav_player.py`. Position is now tracked with
  a monotonic wall-clock (like the pre-1.6 engine), so `PlayPosition` / `IsPlaying`
  are thread-safe; MCI is used only for the play/pause/stop/seek commands.
- **`demos/13_wav_player.py`** rewritten on the new API (`Sound.Open/Play/Pause/Stop/Seek`);
  it no longer depends on the removed WAV methods.
- **Demos now bootstrap `smallbasic` onto `sys.path`** (via `__file__`), so
  `python demos/<name>.py` works from any directory without installing the package
  (previously every demo failed with `ModuleNotFoundError` unless the repo root was
  already on the path).
- **`demos/13_wav_player.py` loads its sample audio relative to the script**, so the
  player shows the real duration and plays no matter which folder you launch it from.

### Added

- **New demo** `demos/15_file_folder_picker.py` — file-open and folder pickers with
  `FilePicked` / `FolderPicked` events showing the chosen path.
- **New demo** `demos/19_brick_breaker.py` — a brick-breaker game: an infinite game loop
  drives the paddle (Left / Right arrow keys), a bouncing ball and breakable bricks.

### Tests

- **Suite expanded from 427 to 450 checks.** `Sound` section 37 now exercises the unified
  API and performs a real WAV playback cycle (open, duration, play, pause-holds-position,
  resume, seek, stop). New section 22d covers the file/folder pickers.

## [1.5.0] - 2026-08-03

### Added

- **Events for the extended controls**, following the existing
  `ButtonClicked` / `TextTyped` pattern (handlers take **no arguments**):
  - `Controls.SliderChanged` — fires on any slider change (drag **and**
    programmatic `SetSliderValue`). Use `Controls.LastChangedSlider`.
  - `Controls.DropDownSelected` — fires when a dropdown item is picked.
    Use `Controls.LastSelectedDropDown`.
  - `Controls.TableRowSelected` — fires when a table row is selected.
    Use `Controls.LastSelectedTable` and `Controls.GetSelectedTableRow(name)`
    (returns the 1-based row index, or `0` if none).
- **`Controls.GetSelectedTableRow(name)`** — returns the currently selected row.
- **Author / version header block** (`# Purpose`, `# Version`, `# Author`,
  `# Email`) added to all 25 core modules.
- **Test suite expanded to 427 checks** — new section 22c covers the
  extended-control events (slider trace, dropdown selection, table selection).

### Fixed

- **Graphics event handlers are now no-argument.** The tkinter backend dispatches
  callbacks with `cb()` — no `tk.Event` is passed, so `def on_key():` works instead of
  raising `TypeError` (previously the callback had to accept the internal event). The
  event state is read through the public API: `GraphicsWindow.LastKey`, `LastText`,
  `MouseX`, `MouseY`.
- **Demos now use only the public Small Basic API** — removed `import os`,
  `import time`, `print()`, and internal `event.x` / `event.num` / `event.key`
  attributes from `demos/08`, `10`, `11`, `13`, `14`. `demos/13_wav_player.py`
  no longer relies on `os.path`; it looks for `sample-speech-1m.wav` in the current
  directory.
- **`demos/99_all_features.py`** is retained as a kitchen-sink reference; it still
  uses `print`, `os`, `time` and the internal `_wav_*` helpers and is **not** a
  pure-API example.

## [1.4.0] - 2026-07-31

### Fixed

- **`GraphicsWindow.KeyDown` / `LastKey` now fire.** The renderer bound both `<KeyPress>` and
  `<Key>` (aliases in Tk), so the `<Key>` binding overwrote `<KeyPress>` and key events never
  reached the handler. The bindings are merged into a single `<Key>` handler that updates both
  `LastKey`/`KeyDown` and `LastText`/`TextInput`.


## [1.3.1] - 2026-07-31

### Added

- **`Sound.WavPlaying`** — read-only property returning `True` while WAV audio is currently playing.
  High-level replacement for the internal `_wav_playing` flag in user code.

### Changed

- `demos/13_wav_player.py` — now uses the public `Sound.WavPlaying` property instead of internal
  attributes (`_wav_playing`, `_wav_position`); `on_play` logic simplified since `WavPlay()`
  already resumes from a paused position

## [1.3.0] - 2026-07-30

### Added

- **Batch rendering** — `GraphicsWindow.BeginBatch()` / `EndBatch()` defers display refreshes so
  bulk drawing operations trigger a single update. Batch scopes can be nested.
- **New demo** `demos/15_batch_rendering.py` — side-by-side timing comparison (500 rectangles
  with and without batch mode)
- `responsive_demo.py` — responsive layout demo using only the public Small Basic API
  (window resize via `Hide()`/`Show()`, no direct tkinter access)
- Internal `begin_batch()` / `end_batch()` / `update()` deferral on `Renderer`

### Changed

- **GraphicsWindow internals refactored** — drawing delegated to new `Renderer` class;
  `_TkWindow` kept as a backward-compat shim for `Controls`/`ImageList`
- Centralized `GraphicsState` for pen, brush, font, window, and event state
- `Renderer._objects` dict replaces per-module canvas id registries
- `Shapes.Animate()` wraps each frame in `begin_batch()`/`end_batch()` for consistent display
- `demos/04_graphics_shapes.py` — batched the 8-ellipse loop
- `demos/99_all_features.py` — batched sections 17a and 17b
- `pyproject.toml` — added `wheel` build dep, maintainers, `dependencies=[]`,
  optional dev/docs deps, `package-data` globs, and URL entries

### Fixed

- **`demos/09_clock_timer.py`** — replaced `Program.Delay(10000)` with `GraphicsWindow.Wait()`
  so the window stays interactive while Timer ticks fire
- **`demos/10_all_features.py`** — added `event` parameter to `draw_circle`, `on_key`, `on_move`
  callbacks (were called with a `tk.Event` but defined with no params → `TypeError`)
- **`DrawText` positional arg bug** — `x`, `y` now passed as positional args to `create_text`

## [1.2.0] - 2026-07-30

### Added

- **WAV playback API** on the `Sound` class with position-tracked pause/resume:
  - `Sound.WavFile` — set the WAV file path; automatically loads header metadata (duration, sample rate)
  - `Sound.WavDuration` — read-only property returning total duration in seconds
  - `Sound.PlayPosition` — read-only property returning current playback position in seconds
  - `Sound.WavPlay()` — play from beginning or resume from paused position
  - `Sound.WavPause()` — pause and save current position
  - `Sound.WavStop()` — stop and reset position to zero
  - `Sound.WavPlayAndWait()` — play synchronously (blocking)
- **Demo 13** (`demos/13_wav_player.py`) — GUI WAV player using the new API, with Play/Pause/Stop buttons, live elapsed time, and a text-based progress bar
- **11 tests** for the WAV API (`TestSoundWav`) in the test suite

### Changed

- `Sound` now uses `_PropSetMeta` metaclass for proper `classproperty` setter support
- Updated README Sound section with WAV properties and methods

## [1.1.0] - 2026-07-30

### Fixed

- **CRITICAL: `Mouse.IsLeftButtonDown` / `IsRightButtonDown` always returned wrong result** — operator precedence bug where `!=` had higher precedence than `&`, causing the button state check to test the wrong bit. Added parentheses to fix: `(GetAsyncKeyState(...) & 0x8000) != 0`
- **`GraphicsWindow.GetPixel()` returned pen color instead of actual pixel color** — now uses `find_closest()` and `itemcget()` to read the color of the nearest canvas item
- **`Shapes.Rotate()` collapsed shapes to a single point** — replaced broken `coords()` call with proper 2D rotation matrix math using `math.cos`/`math.sin`
- **`Dictionary` translation methods didn't translate** — `_translate()` was a stub that called `_fetch_definition()`. Now uses the MyMemory translation API (`api.mymemory.translated.net`) for actual translations
- **`Sound.Pause()` stopped playback instead of pausing** — now uses a `threading.Event` to track pause state, with a separate `Resume()` method to continue playback
- **`Sound.PlayAndWait()` for non-WAV files used arbitrary `time.sleep(2)`** — now estimates duration from file size for a more accurate wait time
- **`Sound.Pause()` / `Stop()` required an unused `file_path` parameter** — removed the parameter since it was never used internally
- **`File.GetTemporaryFilePath()` returned `tempfile.gettempdir()` (a directory) on error** — now returns empty string to match the convention used elsewhere
- **`Timer` silently swallowed exceptions in tick callbacks** — now logs errors via `logging.getLogger(__name__)` instead of bare `pass`
- **`GraphicsWindow` event callbacks were called without the event argument** — `KeyDown`, `KeyUp`, `MouseDown`, `MouseUp`, `MouseMove`, `TextInput` now pass the event object to callbacks via `lambda e=event: callback(e)`

### Added

- `Sound.Resume()` — resumes playback from a paused state
- `Sound._current_file` — tracks the current file for pause/resume
- `Sound._pause_event` — threading event for pause state management
- Comprehensive test suite for all bug fixes

### Changed

- Updated README with accurate API documentation for all objects
- Updated "What It Cannot Do" section to reflect implemented features
- Removed "Desktop.SetWallpaper — Not implemented" (it was already implemented)
- Removed "Sound.PlayAndWait — Not implemented" (it was already implemented)
- Updated API tables with complete method/property listings

## [1.0.0] - 2026-07-30

### Added
- `GraphicsWindow.Wait()` — keeps the window open until the user closes it (calls `mainloop`)
- Full property setter support via `_PropSetMeta` metaclass (e.g., `Turtle.Speed = 8`, `TextWindow.ForegroundColor = "Red"`)
- `Timer.Tick` auto-starts the timer thread when set
- `Controls.AddMultiLineText` alias
- `Array.GetAllIndices` returns `Dict` type
- 11 demo scripts in `demos/`
- `pyproject.toml` for PyPI publishing
- GitHub Actions publish workflow (`.github/workflows/publish.yml`)
- MIT License, README, requirements, .gitignore

### Fixed
- **Turtle flickering** — replaced `root.update()` with `UpdateWindow()` (Windows native) to avoid DWM composition flicker during animation
- `GraphicsWindow.Show()` window operations (`deiconify`, `title`, `geometry`, `resizable`) now run only once; repeated calls are no-ops
- `Turtle._ensure_window()` no longer calls `GraphicsWindow.Show()` on every `Move()` — only when the canvas doesn't exist yet
- `_draw_arrow()` no longer calls `_ensure_window()` — eliminated recursion
- `Turtle.Hide()` properly resets `_shown` flag so re-showing works
- `DrawResizedImage` stores `PhotoImage` refs to prevent garbage collection
- `File.AppendContents` no longer adds extra newline
- `_apply_setting` handles `Left`/`Top` via `geometry()`
- `TextInput` event wired via `<Key>` binding

### Changed
- All `GraphicsWindow` drawing methods use `_TkWindow.update()` for immediate display
