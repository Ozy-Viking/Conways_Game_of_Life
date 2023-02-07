"""
Logic for conways game of life.

Author: Zack Hankin
Started: 3/02/2023
"""
from .util import (
    State, Position, NEIGHBOURS_DEFAULT, Colour, logger, Condition, ColourState, ALIVE_COLOUR,
    DEAD_COLOUR, WHITE, BLACK,
    )

__all__: list[str] = [
    'State',
    'Position',
    'NEIGHBOURS_DEFAULT',
    'Colour',
    'logger',
    'Condition',
    'ColourState',
    'ALIVE_COLOUR',
    'DEAD_COLOUR',
    'WHITE',
    'BLACK',
    ]

from .cell import Cell

__all__ += ['Cell']

from .board import Board

__all__ += ["Board"]
