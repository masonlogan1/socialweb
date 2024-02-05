"""
Handler classes and functions for transforming numeric data
"""

class NumberHandler:
    def str_to_number(self, set_fn):
        def decorator(obj, value):
            # converts strings to floats if the string is a decimal number
            if isinstance(value, str) and value.replace('.', '', 1).isdigit():
                return set_fn(obj, float(value))
            # converts strings to ints if the string is a whole number
            if isinstance(value, str) and value.isdigit():
                return set_fn(obj, int(value))
            # if it isn't a float or int string, attempt to set the value as-is
            set_fn(obj, value)
        return decorator
