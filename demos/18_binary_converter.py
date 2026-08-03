"""
Binary Converter: Text ↔ Binary converter
Transpiled from Microsoft Small Basic.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import *

GraphicsWindow.Width = 400
GraphicsWindow.Height = 300
GraphicsWindow.Title = "Text to Binary : Binary to Text"
GraphicsWindow.Show()

tb = Controls.AddMultiLineTextBox(10, 10)
Controls.SetSize(tb, 380, 250)
btn_tb = Controls.AddButton("Convert to Binary", 10, 265)
btn_bt = Controls.AddButton("Convert to Text", 140, 265)


def onClick():
    last = Controls.LastClickedButton
    if last == btn_tb:
        convert_to_binary()
    else:
        convert_to_text()


Controls.ButtonClicked = onClick

longbin = ""
LongString = ""


def convert_to_binary():
    global longbin
    text = Controls.GetTextBoxText(tb)
    longbin = ""
    for i in range(1, Text.GetLength(text) + 1):
        char_code = Text.GetCharacterCode(Text.GetSubText(text, i, 1))
        bits = []
        while char_code > 0:
            bits.append(Math.Remainder(char_code, 2))
            char_code = Math.Floor(char_code / 2)
        binval = ""
        for j in range(len(bits) - 1, -1, -1):
            binval = Text.Append(binval, str(bits[j]))
        while Text.GetLength(binval) < 8:
            binval = Text.Append("0", binval)
        longbin = Text.Append(longbin, binval)
    Controls.SetTextBoxText(tb, longbin)


def convert_to_text():
    global LongString
    binary = Controls.GetTextBoxText(tb)
    if Math.Remainder(Text.GetLength(binary), 8) != 0:
        GraphicsWindow.ShowMessage("Binary is uneven", "Error")
    else:
        LongString = ""
        for g in range(1, Text.GetLength(binary) + 1, 8):
            bin_char = Text.GetSubText(binary, g, 8)
            dec = 0
            for bit_count in range(1, Text.GetLength(bin_char) + 1):
                idx = Text.GetLength(bin_char) - bit_count + 1
                bit_val = Text.GetSubText(bin_char, idx, 1)
                dec = dec + int(bit_val) * Math.Power(2, bit_count - 1)
            LongString = Text.Append(LongString, Text.GetCharacter(dec))
        Controls.SetTextBoxText(tb, LongString)

GraphicsWindow.Wait()
