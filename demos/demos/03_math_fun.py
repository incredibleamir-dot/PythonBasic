"""
Demo 3: Math - trig, random, fun with *args
"""

from smallbasic import TextWindow, Math

TextWindow.Title = "Math Demo"
TextWindow.ForegroundColor = "White"
TextWindow.BackgroundColor = "DarkBlue"
TextWindow.Show()

TextWindow.WriteLine("=== Math Library ===")
TextWindow.WriteLine(f"Pi = {Math.Pi}")
TextWindow.WriteLine()

TextWindow.WriteLine("--- Trigonometry ---")
TextWindow.WriteLine(f"Sin(90) = {Math.Sin(90)}")
TextWindow.WriteLine(f"Cos(0)  = {Math.Cos(0)}")
TextWindow.WriteLine(f"Tan(45) = {Math.Tan(45)}")
TextWindow.WriteLine()

TextWindow.WriteLine("--- Fun with *args ---")
TextWindow.WriteLine(f"Max(10, 20, 5, 30) = {Math.Max(10, 20, 5, 30)}")
TextWindow.WriteLine(f"Min(10, 20, 5, 30) = {Math.Min(10, 20, 5, 30)}")
TextWindow.WriteLine(f"Sum(1, 2, 3, 4, 5) = {Math.Sum(1, 2, 3, 4, 5)}")
TextWindow.WriteLine(f"Average(10, 20, 30) = {Math.Average(10, 20, 30)}")
TextWindow.WriteLine()

TextWindow.WriteLine("--- Random ---")
for i in range(5):
    r = Math.GetRandomNumber(100)
    TextWindow.WriteLine(f"Random #{i + 1}: {r}")
TextWindow.WriteLine()

TextWindow.WriteLine("--- Rounding ---")
TextWindow.WriteLine(f"Floor(3.7) = {Math.Floor(3.7)}")
TextWindow.WriteLine(f"Ceiling(3.2) = {Math.Ceiling(3.2)}")
TextWindow.WriteLine(f"Round(3.5) = {Math.Round(3.5)}")
TextWindow.WriteLine(f"Abs(-42) = {Math.Abs(-42)}")

TextWindow.Pause()
