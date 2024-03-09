"""
Exceptions for Citrine classes
"""

class CitrineIncompatibleMethodError(Exception):
    """
    Raised when a ZODB method has to be disabled because of incompatibilities
    with necessary methods and functions of Citrine
    """
    def __init__(self, method_name):
        msg = f'Method "{method_name}" is disabled by Citrine'
        super().__init__(msg)

    @staticmethod
    def override_method(fn):
        """
        Decorate a method with this and it'll automatically raise when called
        """
        def decorator(*args, **kwargs):
            raise CitrineIncompatibleMethodError(fn.__name__)
        return decorator