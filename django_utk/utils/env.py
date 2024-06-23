import sys

"""
PYTHON_VERSION
    Just shortcut to get current running python interpreter version
    
    For example "Check is python version lower 3.11":
    
    >>> from django_utk.utils.env import PYTHON_VERSION
    >>>
    >>> if PYTHON_VERSION < (3, 11):
    >>>    foo()

"""

PYTHON_VERSION = sys.version_info[:2]
