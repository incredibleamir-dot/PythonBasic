# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : ImageList object - loads and stores images in memory for drawing.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

import tkinter as tk
from tkinter import PhotoImage
import os
from typing import Optional
from smallbasic._renderer import Renderer


class ImageList:
    """
    Helps to load and store images in memory.

    Usage:
        img = ImageList.LoadImage("C:/path/to/image.png")
        w = ImageList.GetWidthOfImage(img)
        h = ImageList.GetHeightOfImage(img)
    """

    _images: dict = {}          # name -> PIL Image (source of truth)
    _backend_images: dict = {}  # name -> backend image handle
    _tk_images: dict = {}       # backward-compat PhotoImage handles

    @classmethod
    def LoadImage(cls, file_path: str) -> str:
        name = os.path.basename(file_path)
        try:
            from PIL import Image
            pil_img = Image.open(file_path)
            cls._images[name] = pil_img
            backend = Renderer.backend()
            handle = backend.load_image(pil_img)
            cls._backend_images[name] = handle
            if backend.name == "TKINTER":
                cls._tk_images[name] = handle
        except Exception:
            try:
                tk_img = tk.PhotoImage(file=file_path)
                cls._backend_images[name] = tk_img
                cls._tk_images[name] = tk_img
            except Exception:
                name = ""
        return name

    @classmethod
    def _resize(cls, handle, width: int, height: int):
        try:
            return Renderer.backend().resize_image(handle, width, height)
        except Exception:
            return None

    @classmethod
    def GetWidthOfImage(cls, image_name: str) -> int:
        if image_name in cls._images:
            return cls._images[image_name].width
        if image_name in cls._tk_images:
            return cls._tk_images[image_name].width()
        return 0

    @classmethod
    def GetHeightOfImage(cls, image_name: str) -> int:
        if image_name in cls._images:
            return cls._images[image_name].height
        if image_name in cls._tk_images:
            return cls._tk_images[image_name].height()
        return 0