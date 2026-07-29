from datetime import datetime
from smallbasic._utils import classproperty


class Clock:
    """
    Provides access to the system clock.
    
    All properties are class-level and reflect the current system time.
    
    Usage:
        print(Clock.Time)
        print(Clock.Year)
        print(Clock.Hour)
    """

    @classproperty
    def Time(cls) -> str:
        """Gets the current system time as a string (HH:MM:SS)."""
        return datetime.now().strftime("%H:%M:%S")

    @classproperty
    def Date(cls) -> str:
        """Gets the current system date as a string (MM/DD/YYYY)."""
        return datetime.now().strftime("%m/%d/%Y")

    @classproperty
    def Year(cls) -> int:
        """Gets the current year."""
        return datetime.now().year

    @classproperty
    def Month(cls) -> int:
        """Gets the current month (1-12)."""
        return datetime.now().month

    @classproperty
    def Day(cls) -> int:
        """Gets the current day of the month (1-31)."""
        return datetime.now().day

    @classproperty
    def WeekDay(cls) -> str:
        """Gets the current day of the week (e.g., 'Monday')."""
        return datetime.now().strftime("%A")

    @classproperty
    def Hour(cls) -> int:
        """Gets the current hour (0-23)."""
        return datetime.now().hour

    @classproperty
    def Minute(cls) -> int:
        """Gets the current minute (0-59)."""
        return datetime.now().minute

    @classproperty
    def Second(cls) -> int:
        """Gets the current second (0-59)."""
        return datetime.now().second

    @classproperty
    def Millisecond(cls) -> int:
        """Gets the current millisecond (0-999)."""
        return datetime.now().microsecond // 1000

    @classproperty
    def ElapsedMilliseconds(cls) -> int:
        """
        Gets the number of milliseconds that have elapsed since 1900.
        """
        delta = datetime.now() - datetime(1900, 1, 1)
        return int(delta.total_seconds() * 1000)
