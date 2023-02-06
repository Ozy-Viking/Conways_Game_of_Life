"""
Util for logic.

Author: Zack Hankin
Started: 3/02/2023
"""
from __future__ import annotations

import sys
from enum import Enum
import logging
from typing import NamedTuple
import loguru
from loguru import logger
from icecream import ic

logger.success(f"{__name__} importing...")


class Position(NamedTuple):
    """
    Position NamedTuple
    """

    x: int
    y: int


NEIGHBOURS_DEFAULT: set[Position] = {
    Position(1, 0),
    Position(1, 1),
    Position(0, 1),
    Position(-1, 0),
    Position(-1, -1),
    Position(0, -1),
    Position(1, -1),
    Position(-1, 1),
    }

Colour = tuple[int, int, int]
BLACK: Colour = 0, 0, 0
WHITE: Colour = 255, 255, 255


class State(Enum):
    """
    State of an individual cell.
    """

    ALIVE: bool = 1
    DEAD: bool = 0
