from smallbasic.graphics_window import _TkWindow
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
    def AddRectangle(cls, width: int, height: int) -> str:
        """
        Adds a rectangle shape.
        
        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
            
        Returns:
            The name of the shape.
        """
        _TkWindow.ensure()
        cid = None
        coords = (0, 0, width, height)
        if _TkWindow._canvas:
            cid = _TkWindow._canvas.create_rectangle(
                *coords,
                outline=_TkWindow._pen_color,
                width=_TkWindow._pen_width
            )
            _TkWindow.update()
        shape = _Shape("", cid, "rectangle", coords)
        return cls._add_shape(shape)

    @classmethod
    def AddEllipse(cls, width: int, height: int) -> str:
        """
        Adds an ellipse shape.
        
        Args:
            width: The width of the ellipse.
            height: The height of the ellipse.
            
        Returns:
            The name of the shape.
        """
        _TkWindow.ensure()
        cid = None
        coords = (0, 0, width, height)
        if _TkWindow._canvas:
            cid = _TkWindow._canvas.create_oval(
                *coords,
                outline=_TkWindow._pen_color,
                width=_TkWindow._pen_width
            )
            _TkWindow.update()
        shape = _Shape("", cid, "ellipse", coords)
        return cls._add_shape(shape)

    @classmethod
    def AddTriangle(cls, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int) -> str:
        """
        Adds a triangle shape.
        
        Args:
            x1, y1, x2, y2, x3, y3: The three points.
            
        Returns:
            The name of the shape.
        """
        _TkWindow.ensure()
        cid = None
        coords = (x1, y1, x2, y2, x3, y3)
        if _TkWindow._canvas:
            cid = _TkWindow._canvas.create_polygon(
                *coords,
                outline=_TkWindow._pen_color,
                width=_TkWindow._pen_width,
                fill=""
            )
            _TkWindow.update()
        shape = _Shape("", cid, "polygon", coords)
        return cls._add_shape(shape)

    @classmethod
    def AddLine(cls, x1: int, y1: int, x2: int, y2: int) -> str:
        """
        Adds a line between two points.
        
        Args:
            x1, y1: Starting point.
            x2, y2: Ending point.
            
        Returns:
            The name of the shape.
        """
        _TkWindow.ensure()
        cid = None
        coords = (x1, y1, x2, y2)
        if _TkWindow._canvas:
            cid = _TkWindow._canvas.create_line(
                *coords,
                fill=_TkWindow._pen_color,
                width=_TkWindow._pen_width
            )
            _TkWindow.update()
        shape = _Shape("", cid, "line", coords)
        shape.x, shape.y = x1, y1
        return cls._add_shape(shape)

    @classmethod
    def AddImage(cls, image_name: str) -> str:
        """
        Adds an image as a shape.
        
        Args:
            image_name: The name of the image (from ImageList.LoadImage).
            
        Returns:
            The name of the shape.
        """
        _TkWindow.ensure()
        cid = None
        coords = (0, 0)
        if _TkWindow._canvas:
            from smallbasic.imagelist import ImageList
            img = ImageList._tk_images.get(image_name)
            if img:
                cid = _TkWindow._canvas.create_image(0, 0, image=img, anchor="nw")
                _TkWindow.update()
        shape = _Shape("", cid, "image", coords)
        return cls._add_shape(shape)

    @classmethod
    def AddText(cls, text: str) -> str:
        """
        Adds some text as a shape.
        
        Args:
            text: The text to add.
            
        Returns:
            The name of the shape.
        """
        _TkWindow.ensure()
        cid = None
        coords = (0, 0)
        if _TkWindow._canvas:
            weight = "bold" if _TkWindow._font_bold else "normal"
            slant = "italic" if _TkWindow._font_italic else "roman"
            cid = _TkWindow._canvas.create_text(
                0, 0, text=text, anchor="nw",
                font=(_TkWindow._font_name, _TkWindow._font_size, weight, slant),
                fill=_TkWindow._pen_color
            )
            _TkWindow.update()
        shape = _Shape("", cid, "text", coords)
        return cls._add_shape(shape)

    @classmethod
    def SetText(cls, shape_name: str, text: str) -> None:
        """
        Sets the text of a text shape.
        
        Args:
            shape_name: The name of the text shape.
            text: The new text value.
        """
        shape = cls._shapes.get(shape_name)
        if shape and shape.canvas_id and _TkWindow._canvas:
            _TkWindow._canvas.itemconfig(shape.canvas_id, text=text)

    @classmethod
    def Remove(cls, shape_name: str) -> None:
        """
        Removes a shape from the Graphics Window.
        
        Args:
            shape_name: The name of the shape to remove.
        """
        shape = cls._shapes.pop(shape_name, None)
        if shape and shape.canvas_id and _TkWindow._canvas:
            _TkWindow._canvas.delete(shape.canvas_id)
            _TkWindow.update()

    @classmethod
    def Move(cls, shape_name: str, x: int, y: int) -> None:
        """
        Moves the shape to a new position.
        
        Args:
            shape_name: The name of the shape.
            x: The x co-ordinate.
            y: The y co-ordinate.
        """
        shape = cls._shapes.get(shape_name)
        if not shape or not shape.canvas_id or not _TkWindow._canvas:
            return
        canvas = _TkWindow._canvas
        if shape.shape_type in ("text", "image"):
            canvas.coords(shape.canvas_id, x, y)
        else:
            dx = x - shape.x
            dy = y - shape.y
            current = canvas.coords(shape.canvas_id)
            if current:
                new_coords = tuple(
                    current[i] + (dx if i % 2 == 0 else dy)
                    for i in range(len(current))
                )
                canvas.coords(shape.canvas_id, *new_coords)
        shape.x, shape.y = x, y
        _TkWindow.update()

    @classmethod
    def Rotate(cls, shape_name: str, angle: int) -> None:
        """
        Rotates the shape to the specified angle.
        
        Args:
            shape_name: The name of the shape.
            angle: The angle in degrees.
        """
        shape = cls._shapes.get(shape_name)
        if shape and shape.canvas_id and _TkWindow._canvas:
            shape.angle = angle
            bbox = _TkWindow._canvas.bbox(shape.canvas_id)
            if bbox:
                cx = (bbox[0] + bbox[2]) / 2
                cy = (bbox[1] + bbox[3]) / 2
                _TkWindow._canvas.coords(shape.canvas_id, bbox[0], bbox[1])
                _TkWindow.update()

    @classmethod
    def Zoom(cls, shape_name: str, scale_x: float, scale_y: float) -> None:
        """
        Scales the shape by the specified zoom levels (0.1 to 20).
        
        Args:
            shape_name: The name of the shape.
            scale_x: The x-axis zoom level.
            scale_y: The y-axis zoom level.
        """
        shape = cls._shapes.get(shape_name)
        if shape and shape.canvas_id and _TkWindow._canvas:
            scale_x = max(0.1, min(20, float(scale_x)))
            scale_y = max(0.1, min(20, float(scale_y)))
            _TkWindow._canvas.scale(shape.canvas_id, shape.x, shape.y,
                                     scale_x, scale_y)
            _TkWindow.update()

    @classmethod
    def Animate(cls, shape_name: str, x: int, y: int, duration: int) -> None:
        """
        Animates a shape to a new position over the specified duration.
        
        Args:
            shape_name: The name of the shape.
            x: The target x co-ordinate.
            y: The target y co-ordinate.
            duration: The duration in milliseconds.
        """
        shape = cls._shapes.get(shape_name)
        if not shape or not shape.canvas_id or not _TkWindow._canvas:
            return
        start_x, start_y = shape.x, shape.y
        steps = max(1, duration // 16)
        dx = (x - start_x) / steps
        dy = (y - start_y) / steps
        for i in range(steps + 1):
            cx = start_x + dx * i
            cy = start_y + dy * i
            cls.Move(shape_name, int(cx), int(cy))
            import time
            time.sleep(0.016)

    @classmethod
    def GetLeft(cls, shape_name: str) -> int:
        """
        Gets the left co-ordinate of the shape.
        
        Args:
            shape_name: The name of the shape.
            
        Returns:
            The x co-ordinate.
        """
        shape = cls._shapes.get(shape_name)
        return shape.x if shape else 0

    @classmethod
    def GetTop(cls, shape_name: str) -> int:
        """
        Gets the top co-ordinate of the shape.
        
        Args:
            shape_name: The name of the shape.
            
        Returns:
            The y co-ordinate.
        """
        shape = cls._shapes.get(shape_name)
        return shape.y if shape else 0

    @classmethod
    def GetOpacity(cls, shape_name: str) -> int:
        """
        Gets the opacity of a shape.
        
        Args:
            shape_name: The name of the shape.
            
        Returns:
            Opacity from 0 (transparent) to 100 (opaque).
        """
        shape = cls._shapes.get(shape_name)
        return shape.opacity if shape else 100

    @classmethod
    def SetOpacity(cls, shape_name: str, level: int) -> None:
        """
        Sets how opaque a shape should render.
        
        Args:
            shape_name: The name of the shape.
            level: Opacity from 0 to 100.
        """
        shape = cls._shapes.get(shape_name)
        if shape:
            shape.opacity = max(0, min(100, int(level)))
            if shape.canvas_id and _TkWindow._canvas:
                stipple = ""
                if shape.opacity < 100:
                    stipple = "gray75" if shape.opacity > 75 else \
                              "gray50" if shape.opacity > 50 else \
                              "gray25"
                _TkWindow._canvas.itemconfig(shape.canvas_id, stipple=stipple)
                _TkWindow.update()

    @classmethod
    def HideShape(cls, shape_name: str) -> None:
        """
        Hides an already added shape.
        
        Args:
            shape_name: The name of the shape.
        """
        shape = cls._shapes.get(shape_name)
        if shape and shape.canvas_id and _TkWindow._canvas:
            _TkWindow._canvas.itemconfig(shape.canvas_id, state="hidden")
            shape.visible = False

    @classmethod
    def ShowShape(cls, shape_name: str) -> None:
        """
        Shows a previously hidden shape.
        
        Args:
            shape_name: The name of the shape.
        """
        shape = cls._shapes.get(shape_name)
        if shape and shape.canvas_id and _TkWindow._canvas:
            _TkWindow._canvas.itemconfig(shape.canvas_id, state="normal")
            shape.visible = True
