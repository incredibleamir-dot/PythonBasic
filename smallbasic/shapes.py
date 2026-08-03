# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Shapes object - add, move, rotate, zoom, hide and animate shapes.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

"""
Shapes — add, move, rotate, animate shapes on the Graphics Window.

All drawing goes through the internal Renderer.
State reads come from GraphicsState.
"""

import math
import time
from smallbasic._state import GraphicsState
from smallbasic._renderer import Renderer
from smallbasic._utils import classproperty


class _Shape:
    """Represents a shape on the graphics window."""
    def __init__(self, name: str, canvas_id: int, shape_type: str = "",
                 coords: tuple = ()):
        self.name = name
        self.canvas_id = canvas_id
        self.shape_type = shape_type
        self.orig_coords = coords
        self.x = 0
        self.y = 0
        self.angle = 0
        self.opacity = 100
        self.visible = True

    def __repr__(self) -> str:
        return f"Shape(name='{self.name}', type='{self.shape_type}')"


class Shapes:
    """
    Allows you to add, move, rotate, and animate shapes on the Graphics Window.

    Usage:
        rect = Shapes.AddRectangle(100, 50)
        Shapes.Move(rect, 200, 150)
        Shapes.Rotate(rect, 45)
        Shapes.Animate(rect, 300, 200, 1000)
    """

    _shapes: dict = {}
    _counter: int = 0

    @classmethod
    def _add_shape(cls, shape: _Shape) -> str:
        cls._counter += 1
        name = f"Shape{cls._counter}"
        shape.name = name
        cls._shapes[name] = shape
        return name

    @classmethod
    def _default_style(cls):
        return {"outline": GraphicsState.pen_color,
                "width": GraphicsState.pen_width}

    @classmethod
    def AddRectangle(cls, width: int, height: int) -> str:
        Renderer.ensure()
        cid = Renderer.create_rectangle(0, 0, width, height,
                                        **cls._default_style())
        shape = _Shape("", cid, "rectangle", (0, 0, width, height))
        return cls._add_shape(shape)

    @classmethod
    def AddEllipse(cls, width: int, height: int) -> str:
        Renderer.ensure()
        cid = Renderer.create_oval(0, 0, width, height,
                                   **cls._default_style())
        shape = _Shape("", cid, "ellipse", (0, 0, width, height))
        return cls._add_shape(shape)

    @classmethod
    def AddTriangle(cls, x1: int, y1: int, x2: int, y2: int,
                    x3: int, y3: int) -> str:
        Renderer.ensure()
        coords = (x1, y1, x2, y2, x3, y3)
        cid = Renderer.create_polygon(coords, fill="",
                                      **cls._default_style())
        shape = _Shape("", cid, "polygon", coords)
        return cls._add_shape(shape)

    @classmethod
    def AddLine(cls, x1: int, y1: int, x2: int, y2: int) -> str:
        Renderer.ensure()
        coords = (x1, y1, x2, y2)
        cid = Renderer.create_line(x1, y1, x2, y2,
                                   fill=GraphicsState.pen_color,
                                   width=GraphicsState.pen_width)
        shape = _Shape("", cid, "line", coords)
        shape.x, shape.y = x1, y1
        return cls._add_shape(shape)

    @classmethod
    def AddImage(cls, image_name: str) -> str:
        Renderer.ensure()
        from smallbasic.imagelist import ImageList
        img = ImageList._backend_images.get(image_name)
        cid = Renderer.create_image(0, 0, img, anchor="nw") if img else None
        shape = _Shape("", cid, "image", (0, 0))
        return cls._add_shape(shape)

    @classmethod
    def AddText(cls, text: str) -> str:
        Renderer.ensure()
        s = GraphicsState
        weight = "bold" if s.font_bold else "normal"
        slant = "italic" if s.font_italic else "roman"
        cid = Renderer.create_text(
            0, 0, text, anchor="nw",
            font=(s.font_name, s.font_size, weight, slant),
            fill=s.pen_color)
        shape = _Shape("", cid, "text", (0, 0))
        return cls._add_shape(shape)

    @classmethod
    def SetText(cls, shape_name: str, text: str) -> None:
        shape = cls._shapes.get(shape_name)
        if shape and shape.canvas_id:
            Renderer.itemconfig(shape.canvas_id, text=text)

    @classmethod
    def Remove(cls, shape_name: str) -> None:
        shape = cls._shapes.pop(shape_name, None)
        if shape and shape.canvas_id:
            Renderer.delete(shape.canvas_id)
            Renderer.update()

    @classmethod
    def Move(cls, shape_name: str, x: int, y: int) -> None:
        shape = cls._shapes.get(shape_name)
        if not shape:
            return
        if shape.canvas_id:
            if shape.shape_type in ("text", "image"):
                Renderer.coords(shape.canvas_id, x, y)
            else:
                dx = x - shape.x
                dy = y - shape.y
                current = Renderer.coords(shape.canvas_id)
                if current:
                    new_coords = tuple(
                        current[i] + (dx if i % 2 == 0 else dy)
                        for i in range(len(current))
                    )
                    Renderer.coords(shape.canvas_id, *new_coords)
            Renderer.update()
        shape.x, shape.y = x, y

    @classmethod
    def Rotate(cls, shape_name: str, angle: int) -> None:
        shape = cls._shapes.get(shape_name)
        if not shape:
            return
        shape.angle = angle
        if shape.canvas_id:
            coords = list(shape.orig_coords)
            if len(coords) < 4:
                return
            cx = sum(coords[i] for i in range(0, len(coords), 2)) / (len(coords) // 2)
            cy = sum(coords[i] for i in range(1, len(coords), 2)) / (len(coords) // 2)
            rad = math.radians(angle)
            new_coords = []
            for i in range(0, len(coords), 2):
                dx = coords[i] - cx
                dy = coords[i + 1] - cy
                nx = dx * math.cos(rad) - dy * math.sin(rad) + cx
                ny = dx * math.sin(rad) + dy * math.cos(rad) + cy
                new_coords.extend([nx, ny])
            Renderer.coords(shape.canvas_id, *new_coords)
            Renderer.update()

    @classmethod
    def Zoom(cls, shape_name: str, scale_x: float, scale_y: float) -> None:
        shape = cls._shapes.get(shape_name)
        if shape and shape.canvas_id:
            scale_x = max(0.1, min(20, float(scale_x)))
            scale_y = max(0.1, min(20, float(scale_y)))
            Renderer.scale(shape.canvas_id, shape.x, shape.y, scale_x, scale_y)
            Renderer.update()

    @classmethod
    def Animate(cls, shape_name: str, x: int, y: int, duration: int) -> None:
        shape = cls._shapes.get(shape_name)
        if not shape or not shape.canvas_id:
            return
        start_x, start_y = shape.x, shape.y
        steps = max(1, duration // 16)
        dx = (x - start_x) / steps
        dy = (y - start_y) / steps
        for i in range(steps + 1):
            cx = start_x + dx * i
            cy = start_y + dy * i
            Renderer.begin_batch()
            cls.Move(shape_name, int(cx), int(cy))
            Renderer.end_batch()
            if i < steps:
                Renderer.pump_wait(16)

    @classmethod
    def GetLeft(cls, shape_name: str) -> int:
        shape = cls._shapes.get(shape_name)
        return shape.x if shape else 0

    @classmethod
    def GetTop(cls, shape_name: str) -> int:
        shape = cls._shapes.get(shape_name)
        return shape.y if shape else 0

    @classmethod
    def GetOpacity(cls, shape_name: str) -> int:
        shape = cls._shapes.get(shape_name)
        return shape.opacity if shape else 100

    @classmethod
    def SetOpacity(cls, shape_name: str, level: int) -> None:
        shape = cls._shapes.get(shape_name)
        if shape:
            shape.opacity = max(0, min(100, int(level)))
            if shape.canvas_id:
                stipple = ""
                if shape.opacity < 100:
                    stipple = "gray75" if shape.opacity > 75 else \
                              "gray50" if shape.opacity > 50 else \
                              "gray25"
                Renderer.itemconfig(shape.canvas_id, stipple=stipple)
                Renderer.update()

    @classmethod
    def HideShape(cls, shape_name: str) -> None:
        shape = cls._shapes.get(shape_name)
        if shape:
            shape.visible = False
            if shape.canvas_id:
                Renderer.itemconfig(shape.canvas_id, state="hidden")

    @classmethod
    def ShowShape(cls, shape_name: str) -> None:
        shape = cls._shapes.get(shape_name)
        if shape:
            shape.visible = True
            if shape.canvas_id:
                Renderer.itemconfig(shape.canvas_id, state="normal")