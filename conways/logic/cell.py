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
        self.neighbours: set[Cell] = set()
        self.board_size = board_size
        self.alive_neighbours: int = 0

    def toggle(self) -> Cell:
        self.state = State.DEAD if self.alive else State.ALIVE
        self.alive = False if self.alive else True
        return self

    # # @property
    # def alive(self) -> bool:
    #     return self.state is State.ALIVE

    def neighbour_position(self):
        neighbours: list[Position] = list()
        pos: Position = self.position
        offset: Position
        for idx, offset in enumerate(NEIGHBOURS_DEFAULT):
            temp_pos: Position = Position(pos.x + offset.x, pos.y + offset.y)
            if temp_pos.x < 0 or temp_pos.x > self.board_size - 1:
                continue
            if temp_pos.y < 0 or temp_pos.y > self.board_size - 1:
                continue
            neighbours.append(temp_pos)
        return neighbours

    def set_alive_neighbours(self):
        tmp_count = 0
        for neighbour in self.neighbours:
            tmp_count += 1 if neighbour.alive else 0
        self.alive_neighbours = tmp_count
        return self

    @property
    def colour(self) -> Colour:
        return self.state.value

    # def set_neighbours(self) -> Cell:
    #     pos: Position = self.position
    #     offset: Position
    #     for idx, offset in enumerate(NEIGHBOURS_DEFAULT):
    #         temp_pos: Position = Position(pos.x + offset.x, pos.y + offset.y)
    #         if temp_pos.x < 0 or temp_pos.x > self.board_size - 1:
    #             continue
    #         if temp_pos.y < 0 or temp_pos.y > self.board_size - 1:
    #             continue
    #         self.neighbours.append(temp_pos)
    #     return self

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y}, {self.state.name})"
