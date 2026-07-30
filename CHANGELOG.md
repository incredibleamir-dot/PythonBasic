# Changelog

All notable changes to this project will be documented in this file.

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
