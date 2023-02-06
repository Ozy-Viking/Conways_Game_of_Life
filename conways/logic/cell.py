"""
cell

Logic, classes and functions for the cell.

Author: Zack Hankin
Started: 3/02/2023
"""
from __future__ import annotations
from .util import State, Position, NEIGHBOURS_DEFAULT, Colour, logger

logger.success(f"{__name__} importing...")


class Cell:
    """
    Cell object
    """

    def __init__(
            self, x: int, y: int, board_size: int, state: State = State.DEAD
            ) -> None:
        self.x = x
        self.y = y
        self.position: Position = Position(x=x, y=y)
        self.state = state
        self.alive: bool = True if self.state is State.ALIVE else False
        self.alive_neighbours: int = 0

    def toggle(self) -> Cell:
        self.state = State.DEAD if self.state is State.ALIVE else State.ALIVE
        self.alive = True if self.state is State.ALIVE else False
        return self

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y}, {self.state.name})"
