"""
Demo 13: WAV Player - GUI audio player using Sound.WavPlay/Pause/Stop API
Run this demo from the demos/ folder (so the sample WAV file is found).
"""

from smallbasic import GraphicsWindow, Controls, Shapes, Timer, Program, Sound

WAV_FILE = "sample-speech-1m.wav"

# ---------------------------------------------------------------------------
# Load WAV file into the Sound engine
# ---------------------------------------------------------------------------
Sound.WavFile = WAV_FILE
total_dur = Sound.WavDuration


def _fmt(sec):
    m, s = divmod(int(sec), 60)
    return f"{m:02d}:{s:02d}"


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
GraphicsWindow.Title = "WAV Player Demo"
GraphicsWindow.Width = 520
GraphicsWindow.Height = 270
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

GraphicsWindow.FontSize = 18
GraphicsWindow.FontBold = True
GraphicsWindow.PenColor = "Black"
title = Shapes.AddText("WAV Player")
Shapes.Move(title, 20, 20)

GraphicsWindow.FontSize = 11
GraphicsWindow.FontBold = False

fname = Shapes.AddText("File: " + WAV_FILE)
Shapes.Move(fname, 20, 48)

dur_label = Shapes.AddText("Duration: " + _fmt(total_dur))
Shapes.Move(dur_label, 20, 68)

elapsed_label = Shapes.AddText("Elapsed: 00:00")
Shapes.Move(elapsed_label, 20, 88)

GraphicsWindow.FontName = "Consolas"
GraphicsWindow.FontSize = 14
progress_text = Shapes.AddText("")
Shapes.Move(progress_text, 20, 110)

GraphicsWindow.FontSize = 11
GraphicsWindow.FontName = "Consolas"
GraphicsWindow.PenColor = "Gray"
status = Shapes.AddText("Ready")
Shapes.Move(status, 20, 138)

play_btn = Controls.AddButton("Play", 20, 165)
pause_btn = Controls.AddButton("Pause", 110, 165)
stop_btn = Controls.AddButton("Stop", 200, 165)

GraphicsWindow.FontSize = 10
GraphicsWindow.PenColor = "DimGray"
GraphicsWindow.DrawText(20, 210, "Play / Pause / Stop — WavPlay / WavPause / WavStop API")
GraphicsWindow.DrawText(20, 228, "Close the window to exit.")


def _update_ui():
    try:
        ct = Sound.PlayPosition
        Shapes.SetText(elapsed_label, "Elapsed: " + _fmt(ct))

        pct = ct / total_dur if total_dur > 0 else 0
        blocks = int(pct * 30)
        bar = chr(9608) * blocks + chr(9617) * (30 - blocks)
        Shapes.SetText(progress_text, "[" + bar + "] " + str(int(pct * 100)).rjust(3) + "%")

        if Sound.WavPlaying and ct >= total_dur - 0.3:
            Sound.WavStop()
            Controls.SetButtonCaption(play_btn, "Play")
            Shapes.SetText(status, "Finished")
            Timer.Pause()
    except Exception:
        pass


def on_play():
    if not Sound.WavPlaying:
        Sound.WavPlay()
        Timer.Interval = 100
        Timer.Tick = _update_ui
    Timer.Resume()
    Shapes.SetText(status, "Playing")


def on_pause():
    if not Sound._wav_playing:
        return
    Sound.WavPause()
    Controls.SetButtonCaption(play_btn, "Resume")
    Shapes.SetText(status, "Paused")
    _update_ui()


def on_stop():
    Sound.WavStop()
    Controls.SetButtonCaption(play_btn, "Play")
    Shapes.SetText(status, "Stopped")
    Timer.Pause()
    _update_ui()


def dispatch():
    try:
        btn = Controls.LastClickedButton
        if btn == play_btn:
            on_play()
        elif btn == pause_btn:
            on_pause()
        elif btn == stop_btn:
            on_stop()
    except Exception:
        pass


Controls.ButtonClicked = dispatch

Program.Delay(500)
GraphicsWindow.Wait()
