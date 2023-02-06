"""
Logic for conways game of life.

Author: Zack Hankin
Started: 3/02/2023
"""
from .util import State, Position, NEIGHBOURS_DEFAULT, Colour, logger

__all__: list[str] = ['State', 'Position', 'NEIGHBOURS_DEFAULT', 'Colour', 'logger']

from .cell import Cell

__all__ += ['Cell']

from .board_numpy import Board

__all__ += ["Board"]
