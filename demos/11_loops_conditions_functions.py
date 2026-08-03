"""
Demo 11: For loops, While loops, Conditions, Functions

This demo shows how Python control flow concepts map to
Small Basic thinking while using the library's features.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import TextWindow, Math, Program

TextWindow.Title = "Loops, Conditions & Functions"
TextWindow.ForegroundColor = "White"
TextWindow.BackgroundColor = "DarkBlue"
TextWindow.Show()

# ─────────────────────────────────────────────
# FOR LOOPS (For i = 1 To 10)
# ─────────────────────────────────────────────
TextWindow.WriteLine("=== FOR LOOPS ===")

# Simple for loop
TextWindow.WriteLine("Counting 1 to 5:")
for i in range(1, 6):
    TextWindow.WriteLine(f"  {i}")

# For loop with step
TextWindow.WriteLine("Even numbers 2 to 10:")
for i in range(2, 11, 2):
    TextWindow.WriteLine(f"  {i}")

# For loop backwards
TextWindow.WriteLine("Countdown 5 to 1:")
for i in range(5, 0, -1):
    TextWindow.WriteLine(f"  {i}")

# For loop over a list
colors = ["Red", "Green", "Blue", "Yellow"]
TextWindow.WriteLine("Colors in list:")
for color in colors:
    TextWindow.WriteLine(f"  {color}")

# For loop using Small Basic's Math.GetRandomNumber
TextWindow.WriteLine("5 Random Numbers (1-100):")
for _ in range(5):
    TextWindow.Write(Math.GetRandomNumber(100), " ")

TextWindow.WriteLine("\n")

# ─────────────────────────────────────────────
# WHILE LOOPS
# ─────────────────────────────────────────────
TextWindow.WriteLine("=== WHILE LOOPS ===")

# Simple while loop
count = 1
TextWindow.WriteLine("While loop (count to 3):")
while count <= 3:
    TextWindow.WriteLine(f"  Count is {count}")
    count += 1

# While loop with condition
remaining = 5
TextWindow.WriteLine("Countdown with while:")
while remaining > 0:
    TextWindow.WriteLine(f"  {remaining}...")
    remaining -= 1
    Program.Delay(300)

TextWindow.WriteLine("  Blast off!\n")

# ─────────────────────────────────────────────
# CONDITIONS (If...Then...Else)
# ─────────────────────────────────────────────
TextWindow.WriteLine("=== CONDITIONS ===")

# If-elif-else
age = 12
TextWindow.WriteLine(f"If the person is {age} years old:")
if age < 5:
    TextWindow.WriteLine("  Too young for school")
elif age < 11:
    TextWindow.WriteLine("  Elementary school")
elif age < 14:
    TextWindow.WriteLine("  Middle school")
elif age < 18:
    TextWindow.WriteLine("  High school")
else:
    TextWindow.WriteLine("  Adult")

# Conditions with logical operators
score = 85
TextWindow.WriteLine(f"Score: {score}")
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
TextWindow.WriteLine(f"  Grade: {grade}")

# Nested conditions
x, y = 10, 20
if x >= 0 and y >= 0:
    TextWindow.WriteLine(f"  Point ({x}, {y}) is in Quadrant I")
elif x < 0 and y >= 0:
    TextWindow.WriteLine(f"  Point ({x}, {y}) is in Quadrant II")

# ─────────────────────────────────────────────
# FUNCTIONS (Subroutines / Sub)
# ─────────────────────────────────────────────
TextWindow.WriteLine("\n=== FUNCTIONS ===")

# Function without arguments (like Sub)
def say_hello():
    TextWindow.WriteLine("  Hello from a function!")

say_hello()

# Function with one argument
def greet(name):
    TextWindow.WriteLine(f"  Hello, {name}!")

greet("Amir")
greet("Sarah")

# Function with multiple arguments
def add(a, b):
    return a + b

result = add(10, 20)
TextWindow.WriteLine(f"  10 + 20 = {result}")

# Function with default arguments
def repeat(text, times=3):
    for _ in range(times):
        TextWindow.Write(text, " ")

TextWindow.Write("  Repeat 'Hi' 4 times: ")
repeat("Hi", 4)
TextWindow.WriteLine()

TextWindow.Write("  Repeat 'Yo' (default 3): ")
repeat("Yo")
TextWindow.WriteLine()

# Function returning a value (like Function in Small Basic)
def circle_area(radius):
    return Math.Pi * radius * radius

r = 5
area = circle_area(r)
TextWindow.WriteLine(f"  Area of circle r={r} is {area:.2f}")

# Function with *args (fun with arguments)
def show_many(*items):
    TextWindow.WriteLine(f"  Got {len(items)} items: " + ", ".join(str(i) for i in items))

show_many(1, 2, 3)
show_many("apple", "banana", "cherry", "date")

# Function calling other functions
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

TextWindow.WriteLine(f"  Factorial(5) = {factorial(5)}")

# Using Small Basic objects inside functions
def draw_random_shapes(count):
    for i in range(count):
        r = Math.GetRandomNumber(50) + 10
        from smallbasic import GraphicsWindow
        GraphicsWindow.BrushColor = GraphicsWindow.GetRandomColor()
        GraphicsWindow.FillEllipse(
            Math.GetRandomNumber(500),
            Math.GetRandomNumber(300),
            r, r
        )

TextWindow.WriteLine("\nRunning GraphicsWindow demo from function...")
from smallbasic import GraphicsWindow
GraphicsWindow.Title = "Function Demo"
GraphicsWindow.Width = 600
GraphicsWindow.Height = 400
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

draw_random_shapes(10)

Program.Delay(3000)
GraphicsWindow.Hide()
TextWindow.WriteLine("Done!")
TextWindow.Pause()
