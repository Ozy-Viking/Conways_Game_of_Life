"""
pygame_ui.py



Author: Zack Hankin
Started: 3/02/2023
"""
from __future__ import annotations

import os
import sys
import time
from typing import Generator, Optional, Protocol

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = os.environ.get(
    "PYGAME_HIDE_SUPPORT_PROMPT", "1"
    )

import pygame
from pygame.event import Event
from pygame.font import Font

from conways.logic import Position, logger, ALIVE_COLOUR, DEAD_COLOUR

logger.success(f"{__name__} importing...")


# noinspection PyMissingOrEmptyDocstring
class Cell(Protocol):
    x: int
    y: int
    is_alive: bool
    alive_neighbours: int


# noinspection PyMissingOrEmptyDocstring
class Board(Protocol):
    board: list[list[Cell]]
    board_size: int
    num_of_runs: int

    def generation(self) -> Board: ...

    def toggle_cell(self, cell: Position) -> Board: ...

    def run_for_set_amount(self): ...

    def reset(self) -> Board: ...

    def __iter__(self) -> Generator[tuple[Position, Cell], None, None]: ...

    def set_random_board(self, random_seed: Optional[int] = None) -> Board: ...


class PygameFont(Font):
    """
    Returns a pygame Font object.
    """

    def __init__(
            self,
            name: str = "calibri",
            size: int = 12,
            bold: bool = False,
            italic: bool = False,
            position: Position = Position(0, 0),
            ):
        if not pygame.font.get_init():
            pygame.font.init()
        if name in pygame.font.get_fonts():
            font = pygame.font.match_font(name, bold, italic)
        else:
            raise ValueError(f"name: '{name}' not a valid font.")
        super().__init__(font, size)
        self.__position: Position = Position(0, 0)
        self.position = position

    @property
    def position(self) -> Position:
        """
        Position of the font on the window.

        Returns:
            Position
        """
        return self.__position

    @position.setter
    def position(self, value: tuple[int, int] | Position):
        self.__position = value


class PygameUI:
    """
    Pygame UI for Conways Game of life.
    """

    __UI: PygameUI | None = None

    def __new__(cls, *args, **kwargs):
        if not cls.__UI:
            return super().__new__(cls)
        else:
            return cls.__UI

    def __init__(self, board: Board, *, height: int = 800, width: int = 800, fps: int = 60):
        self.num_of_runs = board.num_of_runs
        self.running = True
        if not pygame.get_init():
            pygame.init()

        pygame.display.set_caption("Conway's Game of Life")
        self.fps = fps
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        self._board: Board = board
        self.paused: bool = True if self.num_of_runs == 0 else False
        self.clock = pygame.time.Clock()
        self.background = pygame.color.Color(10, 10, 10)
        self.cell_size = width // self._board.board_size
        self.toggle_cells: set[Position] = set()
        self.timer_font = PygameFont(position=Position(10, 10))
        self.board: dict[Position, dict[str, Cell | pygame.rect.Rect]] = dict()
        self.set_board()

    def run(self):
        count = 0
        if self.num_of_runs != 0:
            my_iter = self.run_set_times()
            next(my_iter)
        while self.running:
            count += 1
            event_list = pygame.event.get()
            for event in event_list:
                self.event_handler(event)
            if not self.paused:
                self.clock.tick(self.fps)
                self._board.generation()
            else:
                self.clock.tick()
                self.toggle()
            self.update_display()
            if (self.num_of_runs != 0) and (count > self.num_of_runs):
                next(my_iter)
                self.running = False
                logger.info(f"FPS: {self.clock.get_fps()}")

    def event_handler(self, event: Event):
        match event.type:
            case pygame.QUIT:
                logger.debug(f"Pygame Event: {pygame.event.event_name(event.type)}")
                self.quit()
            case pygame.KEYDOWN:
                logger.debug(f"Pygame Event: {pygame.event.event_name(event.type)}")
                self.event_keydown(event)
            case pygame.MOUSEMOTION:
                if 1 in event.buttons and self.paused:
                    self.mouse_moved_clicked(event)
            case pygame.MOUSEBUTTONDOWN:
                logger.debug(f"Pygame Event: {pygame.event.event_name(event.type)}")
                if self.paused:
                    self.click(event)

    def event_keydown(self, event):
        match event.key:
            case pygame.K_ESCAPE:
                logger.info(f"Escape Key: Quiting")
                self.quit()
            case pygame.K_SPACE:

                self.paused = False if self.paused else True
                logger.info(f'State: {"Paused" if self.paused else "Playing"}')
            case pygame.K_n:
                logger.info("Resetting Board")
                self._board.reset()
            case pygame.K_r:
                logger.info(f"Setting board to new random state.")
                self._board.set_random_board()

    def quit(self):
        logger.debug(f"pygame quiting.")
        pygame.quit()
        sys.exit()

    def update_display(self):
        self.window.fill(self.background)
        self.draw_cells()
        pygame.display.update()

    def draw_cells(self):
        for cell in self.board.values():

            colour = ALIVE_COLOUR if cell['cell'].is_alive else DEAD_COLOUR

            pygame.draw.rect(
                surface=self.window,
                color=colour,
                rect=cell['rect']
                )

    def run_set_times(self):
        logger.info(f"Starting {self.num_of_runs:,} generation/s.")
        start = time.perf_counter_ns()
        yield 1
        # self._board.run_for_set_amount()
        end = time.perf_counter_ns()
        logger.success(f"Finished {self.num_of_runs:,} generation/s.")
        time_to_run = end - start
        logger.success(f"Time taken: {time_to_run * 10 ** -6:,.2f} ms")
        logger.success(f"Time taken/run: {(time_to_run * 10 ** -6) / self.num_of_runs:,.2f} ms/run")
        yield 2

    def mouse_moved_clicked(self, event: Event):
        if event.buttons == (1, 0, 0):
            cell = self.cell_clicked(event.pos)
            if cell not in self.toggle_cells:
                self.toggle_cells.add(cell)

    def click(self, event: Event):
        if event.button == 1:
            pos = Position(*event.pos)
            cell = self.cell_clicked(pos)
            if cell not in self.toggle_cells:
                self.toggle_cells.add(cell)
            else:
                self.toggle_cells.remove(cell)

    def cell_clicked(self, position: Position) -> Position:
        if not isinstance(position, Position):
            position = Position(*position)
        return Position(
            int(position.x // self.cell_size), int(position.y // self.cell_size)
            )

    def toggle(self):
        for cell in self.toggle_cells:
            self._board.toggle_cell(cell)
        self.toggle_cells.clear()

    def set_board(self):
        position: Position
        cell: Cell
        for position, cell in iter(self._board):
            self.board[position] = {
                "cell": cell,
                "rect": pygame.Rect(
                    self.cell_size * cell.x,
                    self.cell_size * cell.y,
                    self.cell_size,
                    self.cell_size,
                    )
                }
