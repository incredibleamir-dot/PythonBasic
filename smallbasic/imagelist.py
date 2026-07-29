import tkinter as tk
from tkinter import PhotoImage
import os
from typing import Optional


class ImageList:
    """
    Helps to load and store images in memory.
    
    Usage:
        img = ImageList.LoadImage("C:/path/to/image.png")
        w = ImageList.GetWidthOfImage(img)
        h = ImageList.GetHeightOfImage(img)
    """

    _images: dict = {}
    _tk_images: dict = {}

    @classmethod
    def LoadImage(cls, file_path: str) -> str:
        """
        Loads an image from disk into memory.
        
        Args:
            file_path: The path to the image file.
            
        Returns:
            The image name (key) for use with other methods.
        """
        name = os.path.basename(file_path)
        try:
            from PIL import Image, ImageTk
            pil_img = Image.open(file_path)
            tk_img = ImageTk.PhotoImage(pil_img)
            cls._images[name] = pil_img
            cls._tk_images[name] = tk_img
        except ImportError:
            try:
                tk_img = tk.PhotoImage(file=file_path)
                cls._tk_images[name] = tk_img
            except Exception:
                name = ""
        return name

    @classmethod
    def GetWidthOfImage(cls, image_name: str) -> int:
        """
        Gets the width of the specified image.
        
        Args:
            image_name: The name of the image.
            
        Returns:
            The width in pixels.
        """
        if image_name in cls._images:
            return cls._images[image_name].width
        if image_name in cls._tk_images:
            return cls._tk_images[image_name].width()
        return 0

    @classmethod
    def GetHeightOfImage(cls, image_name: str) -> int:
        """
        Gets the height of the specified image.
        
        Args:
            image_name: The name of the image.
            
        Returns:
            The height in pixels.
        """
        if image_name in cls._images:
            return cls._images[image_name].height
        if image_name in cls._tk_images:
            return cls._tk_images[image_name].height()
        return 0
