import sys
import os
import time
from smallbasic._utils import classproperty


class Program:
    """
    Provides helpers to control program execution.
    
    Usage:
        Program.End()
        Program.Delay(1000)
        count = Program.ArgumentCount
    """

    @classproperty
    def ArgumentCount(cls) -> int:
        """
        Gets the number of command-line arguments.
        """
        return len(sys.argv) - 1

    @classproperty
    def Directory(cls) -> str:
        """
        Gets the executing program's directory.
        """
        return os.getcwd()

    @classmethod
    def End(cls) -> None:
        """
        Ends the program immediately.
        """
        sys.exit(0)

    @classmethod
    def Delay(cls, milliseconds: int) -> None:
        """
        Pauses the program for the specified duration.
        
        Args:
            milliseconds: The number of milliseconds to pause.
        """
        time.sleep(milliseconds / 1000.0)

    @classmethod
    def GetArgument(cls, index: int) -> str:
        """
        Gets the command-line argument at the specified index.
        
        Args:
            index: The 1-based index of the argument.
            
        Returns:
            The argument value, or empty string if not found.
        """
        if 0 < index < len(sys.argv):
            return sys.argv[index]
        return ""
