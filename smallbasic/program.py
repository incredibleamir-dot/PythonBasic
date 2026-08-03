# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Program object - program control, delays and command-line arguments.
# Version : 1.7.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

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

        If a graphics window is open the event loop is kept pumping for the
        duration, so the window stays responsive and Tk-scheduled work
        (e.g. ``Timer.Tick`` callbacks) keeps running.

        Args:
            milliseconds: The number of milliseconds to pause.
        """
        from smallbasic._renderer import Renderer
        Renderer.pump_wait(max(0, int(milliseconds)))

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
