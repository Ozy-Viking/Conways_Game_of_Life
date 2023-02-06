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

    neighbours = list(NEIGHBOURS_DEFAULT)
    neighbours_dict: dict[Cell, list[Cell]] = dict()

    def __init__(
            self,
            no_of_cells: int,
            live_conditions: tuple[int, int] = (2, 3),
            birth_condition: tuple[int, ...] = (3,),
            num_of_runs: int = 0,
            loading_bar: bool = False
            ):
        """

        Args:
            no_of_cells (int): Number of cells across or down on the board.
            live_conditions (tuples[int, int]): the number of neighbours around a cell where you live.
            birth_condition (tuple[int, ...]): number of neighbours which a cell is born.
        """

        self.num_of_runs = num_of_runs
        self.board_size = no_of_cells
        self.board: list[list[Cell]] = [
            [Cell(i, j, no_of_cells) for i in range(no_of_cells)]
            for j in range(no_of_cells)
            ]
        self.set_neighbours()
        self.birth_condition = birth_condition
        self.live_conditions = live_conditions
        self.loading_bar: bool = loading_bar

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
        match self.loading_bar:
            case True:
                for _ in tqdm.trange(runs):
                    self.generation()
            case False:
                for _ in range(runs):
                    self.generation()

    def check_state(self) -> Board:
        """
        Checks the neighbours and updates each cell's count.
        Returns:
            Self
        """
        # state_board = np.array(self.get_state_board())

        for cell, neighbours in self.neighbours_dict.items():
            # logger.trace(f'{cell}: {neighbours = }') # taxing on time only uncomment for tracing.
            alive_neighbours = 0
            for neighbour in neighbours:
                if neighbour.alive:
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
                elif cell.state == State.DEAD and no_alive in self.birth_condition:
                    cell.toggle()
        return self

    def toggle_cell(self, cell: Position) -> Board:
        self.board[cell.y][cell.x].toggle()
        return self

    def __iter__(self) -> Generator[tuple[Position, Cell], None, None]:
        for j, row in enumerate(self.board):
            for i, cell in enumerate(row):
                yield Position(i, j), cell

    def set_neighbours(self):
        for _, cell in iter(self):
            neighbours = list()
            for pos in self.neighbour_position(cell):
                neighbours.append(self.board[pos.y][pos.x])
            self.neighbours_dict[cell] = neighbours

    def neighbour_position(self, cell: Cell | Position) -> list[Position]:
        neighbours: list[Position] = list()
        pos: Position = cell.position
        offset: Position
        for idx, offset in enumerate(NEIGHBOURS_DEFAULT):
            temp_pos: Position = Position(pos.x + offset.x, pos.y + offset.y)
            if temp_pos.x < 0 or temp_pos.x > self.board_size - 1:
                continue
            if temp_pos.y < 0 or temp_pos.y > self.board_size - 1:
                continue
            neighbours.append(temp_pos)
        return neighbours
