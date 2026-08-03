"""
Demo 15: File & Folder Pickers - native file-open / folder dialogs via Controls.
The chosen path is shown in a text box and read from Controls.LastPickedFile /
Controls.LastPickedFolder, or per-picker with Controls.GetPickerPath().
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smallbasic import GraphicsWindow, Controls, Shapes, Program

GraphicsWindow.Title = "File & Folder Pickers Demo"
GraphicsWindow.Width = 520
GraphicsWindow.Height = 240
GraphicsWindow.BackgroundColor = "White"
GraphicsWindow.Show()

GraphicsWindow.FontSize = 14
GraphicsWindow.FontBold = True
GraphicsWindow.PenColor = "Black"
title = Shapes.AddText("File / Folder Pickers")
Shapes.Move(title, 20, 20)

GraphicsWindow.FontSize = 11
GraphicsWindow.FontBold = False
info = Shapes.AddText("Click a picker button to open a native dialog.")
Shapes.Move(info, 20, 50)

file_btn = Controls.AddFilePicker("Open File...", 20, 90)
folder_btn = Controls.AddFolderPicker("Open Folder...", 130, 90)
result_box = Controls.AddTextBox(260, 90)

GraphicsWindow.FontSize = 10
GraphicsWindow.PenColor = "DimGray"
GraphicsWindow.DrawText(20, 140, "The chosen path is shown on the right.")
GraphicsWindow.DrawText(20, 158, "Close the window to exit.")


def on_file():
    Controls.SetTextBoxText(result_box, Controls.LastPickedFile)
    Shapes.SetText(info, "File picked - path shown on the right.")


def on_folder():
    Controls.SetTextBoxText(result_box, Controls.LastPickedFolder)
    Shapes.SetText(info, "Folder picked - path shown on the right.")


Controls.FilePicked = on_file
Controls.FolderPicked = on_folder

Program.Delay(300)
GraphicsWindow.Wait()
