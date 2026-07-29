import ctypes
from smallbasic._utils import classproperty


class Desktop:
    """
    Provides methods to interact with the desktop.
    
    Usage:
        w = Desktop.Width
        h = Desktop.Height
    """

    @classproperty
    def Width(cls) -> int:
        """Gets the screen width of the primary desktop in pixels."""
        try:
            user32 = ctypes.windll.user32
            return user32.GetSystemMetrics(0)
        except Exception:
            return 1920

    @classproperty
    def Height(cls) -> int:
        """Gets the screen height of the primary desktop in pixels."""
        try:
            user32 = ctypes.windll.user32
            return user32.GetSystemMetrics(1)
        except Exception:
            return 1080

    @classmethod
    def SetWallPaper(cls, file_path: str) -> None:
        """
        Sets the desktop wallpaper to the specified image.
        
        Args:
            file_path: The full path to the image file.
        """
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)
        except Exception as e:
            print(f"Could not set wallpaper: {e}")
