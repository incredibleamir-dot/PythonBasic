"""
Demo 8: File - read/write/append text files
"""

from smallbasic import File, TextWindow, Program
import os

TextWindow.Title = "File Operations Demo"
TextWindow.ForegroundColor = "White"
TextWindow.BackgroundColor = "DarkGreen"
TextWindow.Show()

TextWindow.WriteLine("=== File Operations ===")
TextWindow.WriteLine()

# Write
filename = "demo_test.txt"
File.WriteContents(filename, "Hello from Python Small Basic!\n")
TextWindow.WriteLine("File written successfully.")
Program.Delay(500)

# Append
File.AppendContents(filename, "This is line 2.\n")
File.AppendContents(filename, "This is line 3.\n")
TextWindow.WriteLine("Data appended.")
Program.Delay(500)

# Read
content = File.ReadContents(filename)
TextWindow.WriteLine(f"\nFile contents:\n{content}")

# Delete
os.remove(filename)
TextWindow.WriteLine("Cleanup complete (file deleted).")

TextWindow.Pause()
