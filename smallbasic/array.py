# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Array object - named value stores accessed through Small Basic array semantics.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

from typing import Any, Dict


class Array:
    """
    Provides a way of storing more than one value for a given name.
    These values can be accessed by another index.
    
    In Small Basic, arrays use 1-based indexing and string indices.
    This class wraps Python dict for similar behavior.
    
    Usage:
        arr = Array()
        Array.SetValue("myArray", "name", "John")
        val = Array.GetValue("myArray", "name")
    """

    _stores: dict = {}

    @classmethod
    def ContainsIndex(cls, array: Any, index: Any) -> bool:
        """
        Gets whether the array contains the specified index.
        
        Args:
            array: The array or array name to check.
            index: The index to check.
            
        Returns:
            True if the index exists in the array, False otherwise.
        """
        arr = cls._resolve(array)
        return index in arr

    @classmethod
    def ContainsValue(cls, array: Any, value: Any) -> bool:
        """
        Gets whether the array contains the specified value.
        
        Args:
            array: The array or array name to check.
            value: The value to check.
            
        Returns:
            True if the value exists in the array, False otherwise.
        """
        arr = cls._resolve(array)
        return value in arr.values()

    @classmethod
    def GetAllIndices(cls, array: Any) -> Dict:
        """
        Gets all indices for the array as a list.
        
        Args:
            array: The array whose indices are requested.
            
        Returns:
            A list of all indices (1-based to match Small Basic).
        """
        arr = cls._resolve(array)
        keys = list(arr.keys())
        return {i + 1: k for i, k in enumerate(keys)}

    @classmethod
    def GetItemCount(cls, array: Any) -> int:
        """
        Gets the number of items stored in the array.
        
        Args:
            array: The array for which the count is requested.
            
        Returns:
            The number of items in the array.
        """
        arr = cls._resolve(array)
        return len(arr)

    @classmethod
    def IsArray(cls, array: Any) -> bool:
        """
        Gets whether a given variable is an array.
        
        Args:
            array: The variable to check.
            
        Returns:
            True if the variable is an array, False otherwise.
        """
        return isinstance(array, (dict, list))

    @classmethod
    def SetValue(cls, array_name: str, index: Any, value: Any) -> None:
        """
        Sets a value for a given array and index.
        
        Args:
            array_name: The name of the array.
            index: Name of the index.
            value: The value to set.
        """
        if array_name not in cls._stores:
            cls._stores[array_name] = {}
        cls._stores[array_name][index] = value

    @classmethod
    def GetValue(cls, array_name: str, index: Any) -> Any:
        """
        Gets a value for a given array and index.
        
        Args:
            array_name: The name of the array.
            index: The name of the index.
            
        Returns:
            The value at the specified index.
        """
        arr = cls._stores.get(array_name, {})
        return arr.get(index, "")

    @classmethod
    def RemoveValue(cls, array_name: str, index: Any) -> None:
        """
        Removes the array item at the specified index.
        
        Args:
            array_name: The name of the array.
            index: The index of the item to remove.
        """
        arr = cls._stores.get(array_name, {})
        if index in arr:
            del arr[index]

    @classmethod
    def _resolve(cls, array: Any) -> dict:
        """Resolve an array reference to a dict."""
        if isinstance(array, str) and array in cls._stores:
            return cls._stores[array]
        if isinstance(array, dict):
            return array
        return {}
