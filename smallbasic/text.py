# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Text object - string manipulation and searching helpers.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

from typing import Union


class Text:
    """
    Provides helpful operations for working with text.
    
    Usage:
        length = Text.GetLength("Hello")
        result = Text.Append("Hello", " World")
        upper = Text.ConvertToUpperCase("hello")
        index = Text.GetIndexOf("Hello World", "World")
    """

    @classmethod
    def Append(cls, text1: str, text2: str) -> str:
        """
        Appends two text values together.
        
        Args:
            text1: The first text.
            text2: The text to append.
            
        Returns:
            The combined text.
        """
        return str(text1) + str(text2)

    @classmethod
    def GetLength(cls, text: str) -> int:
        """
        Gets the length of the specified text.
        
        Args:
            text: The input text.
            
        Returns:
            The number of characters.
        """
        return len(str(text))

    @classmethod
    def IsSubText(cls, text: str, sub_text: str) -> bool:
        """
        Checks if sub_text is found within text.
        
        Args:
            text: The text to search in.
            sub_text: The text to search for.
            
        Returns:
            True if sub_text is found, False otherwise.
        """
        return str(sub_text) in str(text)

    @classmethod
    def EndsWith(cls, text: str, sub_text: str) -> bool:
        """
        Checks if text ends with the specified sub_text.
        
        Args:
            text: The input text.
            sub_text: The suffix to check.
            
        Returns:
            True if text ends with sub_text.
        """
        return str(text).endswith(str(sub_text))

    @classmethod
    def StartsWith(cls, text: str, sub_text: str) -> bool:
        """
        Checks if text starts with the specified sub_text.
        
        Args:
            text: The input text.
            sub_text: The prefix to check.
            
        Returns:
            True if text starts with sub_text.
        """
        return str(text).startswith(str(sub_text))

    @classmethod
    def GetSubText(cls, text: str, start: int, length: int) -> str:
        """
        Gets a substring starting at the specified position.
        
        Args:
            text: The input text.
            start: The 1-based start position.
            length: The number of characters to extract.
            
        Returns:
            The extracted substring.
        """
        t = str(text)
        start_idx = max(0, int(start) - 1)
        return t[start_idx:start_idx + int(length)]

    @classmethod
    def GetSubTextToEnd(cls, text: str, start: int) -> str:
        """
        Gets a substring from the specified position to the end.
        
        Args:
            text: The input text.
            start: The 1-based start position.
            
        Returns:
            The substring from start to end.
        """
        t = str(text)
        start_idx = max(0, int(start) - 1)
        return t[start_idx:]

    @classmethod
    def GetIndexOf(cls, text: str, sub_text: str) -> int:
        """
        Gets the 1-based index of sub_text within text.
        
        Args:
            text: The text to search in.
            sub_text: The text to search for.
            
        Returns:
            The 1-based index, or 0 if not found.
        """
        idx = str(text).find(str(sub_text))
        return idx + 1 if idx >= 0 else 0

    @classmethod
    def ConvertToLowerCase(cls, text: str) -> str:
        """
        Converts text to lower case.
        
        Args:
            text: The input text.
            
        Returns:
            The lower-cased text.
        """
        return str(text).lower()

    @classmethod
    def ConvertToUpperCase(cls, text: str) -> str:
        """
        Converts text to upper case.
        
        Args:
            text: The input text.
            
        Returns:
            The upper-cased text.
        """
        return str(text).upper()

    @classmethod
    def GetCharacter(cls, code: int) -> str:
        """
        Gets the character for the specified character code.
        
        Args:
            code: The ASCII/Unicode character code.
            
        Returns:
            The character.
        """
        return chr(int(code))

    @classmethod
    def GetCharacterCode(cls, character: str) -> int:
        """
        Gets the character code for the specified character.
        
        Args:
            character: A single character.
            
        Returns:
            The ASCII/Unicode code.
        """
        return ord(str(character)[0])
