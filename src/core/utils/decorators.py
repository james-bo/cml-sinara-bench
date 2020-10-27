# coding: utf-8

import inspect
from functools import wraps
from ui.console import terminal


def method_info(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        terminal.show_debug_message("Function called: {}", func.__qualname__)
        terminal.show_debug_message("Values: {}", inspect.getcallargs(func, *args, **kwargs))
        return func(*args, **kwargs)

    return wrapper
