"""
board

Author: Zack Hankin
Started: 3/02/2023
"""
from __future__ import annotations

from random import randint, Random
from typing import Generator, Optional
import tqdm as tqdm

from .util import Condition, NEIGHBOURS_DEFAULT, Position, logger
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
            num_of_cells: int,
            live_conditions: Condition = Condition(2, 3),
            birth_condition: Condition = Condition(3),
            num_of_runs: int = 0,
            loading_bar: bool = False
            ):
        """

        Args:
            num_of_cells (int): Number of cells across or down on the board.
            live_conditions (Condition): the number of neighbours around a cell where you live.
            birth_condition (Condition): number of neighbours which a cell is born.
        """

        self.num_of_runs = num_of_runs
        self.board_size = num_of_cells
        self.board: list[list[Cell]] = [
            [Cell(i, j) for i in range(num_of_cells)]
            for j in range(num_of_cells)
            ]
        self.set_neighbours()
        self.birth_condition = birth_condition
        self.birth_condition_set = self.birth_condition.contains
        logger.debug(f"Birth condition: {self.birth_condition_set}")
        self.live_condition = live_conditions
        self.live_condition_set = self.live_condition.contains
        logger.debug(f"Live condition: {self.live_condition_set}")
        self.loading_bar: bool = loading_bar
        logger.success("Board initialised: ")

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
            random_seed = randint(0, 100)
        logger.info(f"Random seed: {random_seed}")

        random = Random(random_seed)
        for row in self.board:
            for cell in row:
                if random.choice((True, False)):
                    cell.toggle()
        return self

    def reset(self) -> Board:
        for cell in self.neighbours_dict.keys():
            cell.is_alive = False
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
            cell.alive_neighbours = 0
            for neighbour in neighbours:
                if neighbour.is_alive:
                    cell.alive_neighbours += 1
        return self

    def update_state(self) -> Board:
        """
        Update the state of every cell.

        Returns:
            Self
        """
        for row in self.board:
            for cell in row:
                num_alive: int = cell.alive_neighbours
                if (((not cell.is_alive) and (num_alive in self.birth_condition_set))
                        or (cell.is_alive and (num_alive not in self.live_condition_set))):
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
        self.neighbours_dict = dict()
        for _, cell in iter(self):
            neighbours = list()
            for pos in self.neighbour_position(cell):
                neighbours.append(self.board[pos.y][pos.x])
            self.neighbours_dict[cell] = neighbours
        return self

    def neighbour_position(self, cell: Cell | Position) -> list[Position]:
        neighbours: list[Position] = list()
        pos: Position = Position(cell.x, cell.y)
        offset: Position
        for idx, offset in enumerate(NEIGHBOURS_DEFAULT):
            temp_pos: Position = Position(pos.x + offset.x, pos.y + offset.y)
            if temp_pos.x < 0 or temp_pos.x > self.board_size - 1:
                continue
            if temp_pos.y < 0 or temp_pos.y > self.board_size - 1:
                continue
            neighbours.append(temp_pos)
        return neighbours
