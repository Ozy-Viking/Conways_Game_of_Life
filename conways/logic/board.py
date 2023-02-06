"""
board

Author: Zack Hankin
Started: 3/02/2023
"""
from __future__ import annotations

from itertools import count
from random import randint, Random
from typing import Generator, Optional

import tqdm as tqdm

from conways.performance import Timer
from .util import Position, State, logger
from .cell import Cell

logger.success(f"{__name__} importing...")


class Board:
    """
    board[pos.y][pos.x]
    """

    def __init__(
            self,
            no_of_cells: int,
            live_conditions: tuple[int, int] = (2, 3),
            birth: tuple[int, ...] = (3,),
            num_of_runs: int = 0,
            ):
        """

        Args:
            no_of_cells (int): Number of cells across or down on the board.
            live_conditions (tuples[int, int]): the number of neighbours around a cell where you live.
            birth (int): number of neighbours which a cell is born.
        """
        self.num_of_runs = num_of_runs
        self.board_size = no_of_cells
        self.board = [
            [Cell(i, j, no_of_cells).set_neighbours() for i in range(no_of_cells)]
            for j in range(no_of_cells)
            ]
        self.birth = birth
        self.live_conditions = live_conditions

    def __len__(self):
        return len(self.board) * len(self.board[0])

    def set_random_board(self, random_seed: Optional[int] = None) -> Board:
        """
        Sets every cell in the board to a random state.

        Args:
            random_seed (int, Optional): Random seed value, if no seed is given will use a random value.
                                         Default is None.

        Returns:
            Self
        """
        if not random_seed:
            random_seed = randint(0, 100_000_000)

        random = Random(random_seed)
        for row in self.board:
            for cell in row:
                if random.choice((True, False)):
                    cell.toggle()
        return self

    # @Timer.time
    def generation(self) -> Board:
        """
        One generation.

        Returns:
            Self
        """
        self.check_state()
        self.update_state()
        return self

    def run_for_set_amount(self):
        for _ in tqdm.trange(self.num_of_runs):
            self.generation()

    def check_state(self) -> Board:
        """
        Checks the neighbours and updates each cell's count.
        Returns:
            Self
        """
        for j, row in enumerate(self.board):
            for i, cell in enumerate(row):
                neighbours = cell.neighbours
                alive_neighbours = 0
                for pos in neighbours:
                    if self.board[pos.y][pos.x].state is State.ALIVE:
                        alive_neighbours += 1
                cell.alive_neighbours = alive_neighbours
        return self

    def update_state(self) -> Board:
        """
        Update the state of every cell.

        Returns:
            Self
        """
        for j, row in enumerate(self.board):
            for i, cell in enumerate(row):
                no_alive: int = cell.alive_neighbours
                if cell.state == State.ALIVE and (
                        no_alive < self.live_conditions[0]
                        or no_alive > self.live_conditions[1]
                ):
                    cell.toggle()
                elif cell.state == State.DEAD and no_alive in self.birth:
                    cell.toggle()
        return self

    def toggle_cell(self, cell: Position) -> Board:
        self.board[cell.y][cell.x].toggle()
        return self
