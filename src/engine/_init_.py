# src/engine/__init__.py
from .Simulator import Simulator  # Makes Simulator available at package level

__all__ = ['Simulator']  # Controls what gets imported with `from engine import *`