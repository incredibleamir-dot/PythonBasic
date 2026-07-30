"""
Demo 1: Hello World - TextWindow basics
"""

from smallbasic import TextWindow

TextWindow.Title = "Hello World"
TextWindow.ForegroundColor = "Cyan"
TextWindow.WriteLine("Hello, World!")
TextWindow.WriteLine("Welcome to Python Small Basic!")

TextWindow.ForegroundColor = "Yellow"
TextWindow.Write("What is your name? ")
name = TextWindow.Read()

TextWindow.ForegroundColor = "Green"
TextWindow.WriteLine(f"Nice to meet you, {name}!")

TextWindow.Pause()
