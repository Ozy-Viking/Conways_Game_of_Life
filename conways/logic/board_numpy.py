"""
board

Author: Zack Hankin
Started: 3/02/2023
"""
from __future__ import annotations

from itertools import count
from random import randint, Random
from typing import Any, Generator, Optional
import numpy as np
import pandas as pd
import tqdm as tqdm
from icecream import ic

from conways.performance import Timer
from .util import NEIGHBOURS_DEFAULT, Position, State, logger
from .cell import Cell

logger.success(f"{__name__} importing...")


class Board:
    """
    board[pos.y][pos.x]
    """

    neighbours = np.array(list(NEIGHBOURS_DEFAULT))
    neighbours_dict: dict[Cell, list[Cell]] = dict()

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
        self.board: np.ndarray = np.array(
            [
                [Cell(i, j, no_of_cells) for i in range(no_of_cells)]
                for j in range(no_of_cells)
                ]
            )
        self.set_neighbours()
        self.state_board = np.zeros(shape=(no_of_cells, no_of_cells))
        self.state_board = self.get_state_board()
        self.birth = birth
        self.live_conditions = live_conditions

    def __len__(self):
        return len(self.board) * len(self.board[0])

    def get_state_board(self) -> pd.DataFrame:
        self.state_board = pd.DataFrame(self.board).applymap(lambda x: x.alive)
        for pos, cell in iter(self):
            self.state_board[pos.y][pos.x] = cell.alive
        return self.state_board

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

    def run_for_set_amount(self, runs: Optional[int] = None):
        runs = self.num_of_runs if runs is None else runs
        for _ in tqdm.trange(runs):
            self.generation()

    def check_state(self) -> Board:
        """
        Checks the neighbours and updates each cell's count.
        Returns:
            Self
        """
        # state_board = np.array(self.get_state_board())

        # for cell, neighbours in self.neighbours_dict.items():
        # logger.trace(f'{cell}: {neighbours = }') # taxing on time
        # alive_neighbours = 0
        # for neighbour in neighbours:
        #     if neighbour.alive:
        #         alive_neighbours += 1
        # cell.alive_neighbours = alive_neighbours
        for _, cell in np.ndenumerate(self.board):
            cell.set_alive_neighbours()
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

    def __iter__(self) -> Generator[tuple[Position, Cell], None, None]:
        for pos, cell in np.ndenumerate(self.board):
            yield Position(*pos), cell

    def set_neighbours(self):
        for _, cell in iter(self):
            neighbours = set()
            for pos in cell.neighbour_position():
                neighbours.add(self.board[pos.y][pos.x])
            self.neighbours_dict[cell] = neighbours
            cell.neighbours = neighbours
        # todo: try storing the uncalled property of alive then call it.
