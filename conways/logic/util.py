"""
Util for logic.

Author: Zack Hankin
Started: 3/02/2023
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from enum import Enum
import logging
from typing import NamedTuple, Optional
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
DEAD_COLOUR = BLACK
ALIVE_COLOUR = WHITE


class State(Enum):
    """
    State of an individual cell.
    """

    ALIVE: bool = True
    DEAD: bool = False


class ColourState(Enum):
    ALIVE: Colour = WHITE
    DEAD: Colour = BLACK


@dataclass(slots=True)
class Condition:
    """
    Inclusive low and high.
    """
    low: int
    high: Optional[int] = None
    contains: set = field(default_factory=set)

    def __post_init__(self):
        if self.high is None:
            self.contains.add(self.low)
        else:
            self.contains |= set(range(self.low, self.high + 1))

    def __contains__(self, item):
        return item in self.contains

    def __repr__(self):
        return f"{self.__class__.__name__}({self.low}, {self.high}, {self.contains})"
