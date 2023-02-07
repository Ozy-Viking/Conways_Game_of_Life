"""
cell

Logic, classes and functions for the cell.

Author: Zack Hankin
Started: 3/02/2023
"""
from __future__ import annotations

from dataclasses import dataclass, field
from turtle import position

from .util import State, Position, NEIGHBOURS_DEFAULT, Colour, logger

logger.success(f"{__name__} importing...")


@dataclass(slots=True)
class Cell:
    """
    Cell object
    """
    x: int
    y: int
    is_alive: bool = False
    alive_neighbours: int = field(init=False)

    def toggle(self) -> Cell:
        """
        Toggle the cell from alive to dead.

        Returns:
            Self
        """
        self.is_alive = False if self.is_alive else True
        return self

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y}, {State(self.is_alive).name})"
