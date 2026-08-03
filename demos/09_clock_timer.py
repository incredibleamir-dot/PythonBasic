"""
Demo 9: Clock + Timer - time and events

Note: Timer.Tick callbacks are GUI-safe when a graphics window is open
(they run on the window's event loop); pair the timer with GraphicsWindow
so the window stays alive and keeps ticking.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import Clock, Timer, TextWindow, GraphicsWindow

TextWindow.Title = "Clock & Timer Demo"
TextWindow.ForegroundColor = "White"
TextWindow.BackgroundColor = "DarkRed"
TextWindow.Show()

TextWindow.WriteLine("=== Clock ===")
TextWindow.WriteLine(f"Time: {Clock.Time}")
TextWindow.WriteLine(f"Date: {Clock.Date}")
TextWindow.WriteLine(f"Year: {Clock.Year}  Month: {Clock.Month}  Day: {Clock.Day}")
TextWindow.WriteLine(f"WeekDay: {Clock.WeekDay}")
TextWindow.WriteLine(f"Hour: {Clock.Hour}  Minute: {Clock.Minute}  Second: {Clock.Second}")
TextWindow.WriteLine(f"Milliseconds since midnight: {Clock.ElapsedMilliseconds}")
TextWindow.WriteLine()

# Timer - using GraphicsWindow event loop to process ticks properly
GraphicsWindow.Title = "Timer Demo (close to exit)"
GraphicsWindow.Width = 400
GraphicsWindow.Height = 200
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.DrawText(20, 20, "Timer will tick 5 times in the console.")
GraphicsWindow.DrawText(20, 40, "Close this window to exit.")
GraphicsWindow.Show()

count = 0

def tick():
    global count
    count += 1
    TextWindow.WriteLine(f"Timer tick #{count} at {Clock.Time}")
    if count >= 5:
        Timer.Pause()
        TextWindow.WriteLine("Timer stopped after 5 ticks.")

Timer.Interval = 1000
Timer.Tick = tick
TextWindow.WriteLine("Timer started (1-second intervals, 5 ticks)...")

GraphicsWindow.Wait()
