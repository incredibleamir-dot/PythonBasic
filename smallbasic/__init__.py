# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Package initializer exposing the public Small Basic API.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

"""
Python Small Basic
~~~~~~~~~~~~~~~~~

A Python library that mimics Microsoft Small Basic's API.
Kids can use Python to write code using Small Basic-like methods.

Usage:
    from smallbasic import *
    
    TextWindow.Show()
    TextWindow.WriteLine("Hello, World!")
    name = TextWindow.Read()
"""

from smallbasic.array import Array
from smallbasic.clock import Clock
from smallbasic.controls import Controls
from smallbasic.desktop import Desktop
from smallbasic.dictionary import Dictionary
from smallbasic.file import File
from smallbasic.graphics_window import GraphicsWindow
from smallbasic.imagelist import ImageList
from smallbasic.keywords import Keywords
from smallbasic.math import Math
from smallbasic.mouse import Mouse
from smallbasic.network import Network
from smallbasic.program import Program
from smallbasic.shapes import Shapes
from smallbasic.sound import Sound
from smallbasic.stack import Stack
from smallbasic.text import Text
from smallbasic.text_window import TextWindow
from smallbasic.timer import Timer
from smallbasic.turtle import Turtle

__all__ = [
    'Array', 'Clock', 'Controls', 'Desktop', 'Dictionary',
    'File', 'GraphicsWindow', 'ImageList', 'Keywords',
    'Math', 'Mouse', 'Network', 'Program', 'Shapes',
    'Sound', 'Stack', 'Text', 'TextWindow', 'Timer', 'Turtle',
]
