# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Math object - trigonometry, rounding, statistics and random numbers.
# Version : 1.7.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

import math as _math
import random as _random
from typing import Union
from smallbasic._utils import classproperty

Number = Union[int, float]


class Math:
    """
    Provides useful mathematics-related methods.
    
    Usage:
        result = Math.Sin(90)
        rand = Math.GetRandomNumber(100)
        maximum = Math.Max(10, 20)
        pi = Math.Pi
    """

    @classproperty
    def Pi(cls) -> float:
        """Gets the value of Pi (3.14159...)."""
        return _math.pi

    @classmethod
    def Abs(cls, value: Number) -> Number:
        """
        Gets the absolute value of a number.
        
        Args:
            value: The input number.
            
        Returns:
            The absolute value.
        """
        return abs(value)

    @classmethod
    def Ceiling(cls, value: Number) -> int:
        """
        Rounds a number up to the nearest integer.
        
        Args:
            value: The input number.
            
        Returns:
            The ceiling value.
        """
        return _math.ceil(value)

    @classmethod
    def Floor(cls, value: Number) -> int:
        """
        Rounds a number down to the nearest integer.
        
        Args:
            value: The input number.
            
        Returns:
            The floor value.
        """
        return _math.floor(value)

    @classmethod
    def NaturalLog(cls, value: Number) -> float:
        """
        Gets the natural logarithm of a value.
        
        Args:
            value: The input number (> 0).
            
        Returns:
            The natural logarithm.
        """
        return _math.log(value)

    @classmethod
    def Log(cls, value: Number) -> float:
        """
        Gets the base-10 logarithm of a value.
        
        Args:
            value: The input number (> 0).
            
        Returns:
            The base-10 logarithm.
        """
        return _math.log10(value)

    @classmethod
    def Cos(cls, degrees: Number) -> float:
        """
        Gets the cosine of an angle specified in degrees.
        
        Args:
            degrees: The angle in degrees.
            
        Returns:
            The cosine value.
        """
        return _math.cos(_math.radians(degrees))

    @classmethod
    def Sin(cls, degrees: Number) -> float:
        """
        Gets the sine of an angle specified in degrees.
        
        Args:
            degrees: The angle in degrees.
            
        Returns:
            The sine value.
        """
        return _math.sin(_math.radians(degrees))

    @classmethod
    def Tan(cls, degrees: Number) -> float:
        """
        Gets the tangent of an angle specified in degrees.
        
        Args:
            degrees: The angle in degrees.
            
        Returns:
            The tangent value.
        """
        return _math.tan(_math.radians(degrees))

    @classmethod
    def ArcSin(cls, value: Number) -> float:
        """
        Gets the arc sine in degrees.
        
        Args:
            value: A value between -1 and 1.
            
        Returns:
            The angle in degrees.
        """
        return _math.degrees(_math.asin(max(-1, min(1, value))))

    @classmethod
    def ArcCos(cls, value: Number) -> float:
        """
        Gets the arc cosine in degrees.
        
        Args:
            value: A value between -1 and 1.
            
        Returns:
            The angle in degrees.
        """
        return _math.degrees(_math.acos(max(-1, min(1, value))))

    @classmethod
    def ArcTan(cls, value: Number) -> float:
        """
        Gets the arc tangent in degrees.
        
        Args:
            value: Any number.
            
        Returns:
            The angle in degrees.
        """
        return _math.degrees(_math.atan(value))

    @classmethod
    def GetDegrees(cls, radians: Number) -> float:
        """
        Converts radians to degrees.
        
        Args:
            radians: The angle in radians.
            
        Returns:
            The angle in degrees.
        """
        return _math.degrees(radians)

    @classmethod
    def GetRadians(cls, degrees: Number) -> float:
        """
        Converts degrees to radians.
        
        Args:
            degrees: The angle in degrees.
            
        Returns:
            The angle in radians.
        """
        return _math.radians(degrees)

    @classmethod
    def SquareRoot(cls, value: Number) -> float:
        """
        Gets the square root of a number.
        
        Args:
            value: The input number (>= 0).
            
        Returns:
            The square root.
        """
        return _math.sqrt(value)

    @classmethod
    def Power(cls, base: Number, exponent: Number) -> float:
        """
        Raises a number to the specified power.
        
        Args:
            base: The base number.
            exponent: The exponent.
            
        Returns:
            The result of base^exponent.
        """
        return _math.pow(base, exponent)

    @classmethod
    def Round(cls, value: Number) -> int:
        """
        Rounds a number to the nearest integer.

        Uses Python's ``round()`` (banker's rounding: halves round to
        the nearest even integer), which matches Small Basic's behaviour.
        """
        return round(value)

    @classmethod
    def Max(cls, *args: Number) -> Number:
        """
        Gets the maximum of the provided values.
        Fun with arguments: accepts 2 or more values.
        
        Args:
            *args: Two or more numbers.
            
        Returns:
            The maximum value.
        """
        if len(args) < 1:
            return 0
        return max(args)

    @classmethod
    def Min(cls, *args: Number) -> Number:
        """
        Gets the minimum of the provided values.
        Fun with arguments: accepts 2 or more values.
        
        Args:
            *args: Two or more numbers.
            
        Returns:
            The minimum value.
        """
        if len(args) < 1:
            return 0
        return min(args)

    @classmethod
    def Remainder(cls, dividend: Number, divisor: Number) -> Number:
        """
        Gets the remainder of a division.

        Uses Python's ``%`` operator, so the result takes the sign of the
        divisor (``Remainder(-10, 3) == 2``).  This differs from Small
        Basic / .NET's truncating remainder (``-1``) for negative
        dividends, and is intentionally Python-idiomatic.
        """
        return dividend % divisor

    @classmethod
    def GetRandomNumber(cls, max_value: int) -> int:
        """
        Gets a random number between 1 and max_value (inclusive).
        
        Args:
            max_value: The maximum value.
            
        Returns:
            A random integer from 1 to max_value.
        """
        return _random.randint(1, max(1, int(max_value)))

    @classmethod
    def Sum(cls, *args: Number) -> Number:
        """
        Sums all the provided values.
        Fun with arguments: accepts any number of values.
        
        Args:
            *args: Numbers to sum.
            
        Returns:
            The total sum.
        """
        return sum(args)

    @classmethod
    def Average(cls, *args: Number) -> float:
        """
        Calculates the average of the provided values.
        Fun with arguments: accepts any number of values.
        
        Args:
            *args: Numbers to average.
            
        Returns:
            The average value.
        """
        if not args:
            return 0.0
        return sum(args) / len(args)
