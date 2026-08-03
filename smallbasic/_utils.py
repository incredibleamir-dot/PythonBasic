# --------------------------------------------------------------------------
# Python Small Basic
# Purpose : Shared class helpers - classproperty descriptor and property-set metaclass.
# Version : 1.2.0
# Author  : Amir Arshad
# Email   : incredibleamir@gmail.com
# --------------------------------------------------------------------------

"""
Internal utilities for Python Small Basic.
"""


class classproperty:
    """
    Descriptor that works like @property but for classes.
    
    Usage:
        class MyClass:
            @classproperty
            def Name(cls):
                return cls._name
            
            @Name.setter
            def Name(cls, value):
                cls._name = value
    """

    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset
        self.owner = None

    def __set_name__(self, owner, name):
        self.owner = owner

    def __get__(self, instance, owner):
        return self.fget(owner)

    def __set__(self, instance, value):
        if self.fset:
            cls = type(instance) if instance is not None else self.owner
            self.fset(cls, value)
        else:
            raise AttributeError("can't set attribute")

    def setter(self, fset):
        return type(self)(self.fget, fset)


class _PropSetMeta(type):
    """Metaclass that properly invokes data-descriptor __set__ on class attribute writes.

    Python's type.__setattr__ silently replaces descriptors stored in the
    class __dict__ instead of calling __set__. This metaclass intercepts
    __setattr__ to call __set__ on classproperty and similar descriptors.
    """

    def __setattr__(cls, name, value):
        for base in cls.__mro__:
            if name in base.__dict__:
                obj = base.__dict__[name]
                if hasattr(obj, '__set__'):
                    obj.__set__(None, value)
                    return
                break
        super().__setattr__(name, value)
