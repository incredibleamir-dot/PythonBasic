"""
Demo 2: TextWindow - colors, cursor, read/write, fun with args
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import TextWindow, Program

TextWindow.Title = "TextWindow I/O Demo"
TextWindow.Show()

# Colors
TextWindow.ForegroundColor = "Red"
TextWindow.BackgroundColor = "White"
TextWindow.WriteLine("This is RED text on white background")

TextWindow.ForegroundColor = "Blue"
TextWindow.WriteLine("This is BLUE text")

# Fun with arguments
TextWindow.ForegroundColor = "Purple"
TextWindow.WriteLine("Multiple", "arguments", "are", "joined!")
TextWindow.Write("Counting: ")
for i in range(1, 6):
    TextWindow.Write(i, "...")
TextWindow.WriteLine("Done!")

# Input
TextWindow.ForegroundColor = "Black"
TextWindow.Write("Enter a number: ")
num = TextWindow.ReadNumber()
TextWindow.WriteLine(f"You entered: {num}")

TextWindow.WriteLine(f"{num} x 2 = {num * 2}")

Program.Delay(2000)
TextWindow.Clear()
TextWindow.WriteLine("Cleared!")
TextWindow.Pause()
