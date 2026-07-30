# Changelog

All notable changes to this project will be documented in this file.

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
