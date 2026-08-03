# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Stack object - named LIFO value stacks.
# Version : 1.7.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

from typing import Dict, Any


class Stack:
    """
    Provides a way of storing values like stacking plates.
    You can push a value onto the top of the stack and pop it off.
    Last pushed value is the first one to pop out (LIFO).
    
    Usage:
        Stack.PushValue("myStack", "Hello")
        Stack.PushValue("myStack", "World")
        val = Stack.PopValue("myStack")  # Returns "World"
        count = Stack.GetCount("myStack")
    """

    _stacks: Dict[str, list] = {}

    @classmethod
    def PushValue(cls, stack_name: str, value: Any) -> None:
        """
        Pushes a value onto the specified stack.
        
        Args:
            stack_name: The name of the stack.
            value: The value to push.
        """
        if stack_name not in cls._stacks:
            cls._stacks[stack_name] = []
        cls._stacks[stack_name].append(value)

    @classmethod
    def GetCount(cls, stack_name: str) -> int:
        """
        Gets the number of items in the specified stack.
        
        Args:
            stack_name: The name of the stack.
            
        Returns:
            The number of items.
        """
        return len(cls._stacks.get(stack_name, []))

    @classmethod
    def PopValue(cls, stack_name: str) -> Any:
        """
        Pops a value from the specified stack.
        
        Args:
            stack_name: The name of the stack.
            
        Returns:
            The value from the top of the stack, or "" if empty.
        """
        stack = cls._stacks.get(stack_name, [])
        if stack:
            return stack.pop()
        return ""

    @classmethod
    def reset(cls) -> None:
        """Forget all named stacks."""
        cls._stacks.clear()
