"""
pygame_ui.py



Author: Zack Hankin
Started: 3/02/2023
"""
from __future__ import annotations

import os
import sys
from typing import Protocol

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = os.environ.get(
    "PYGAME_HIDE_SUPPORT_PROMPT", "1"
)

import pygame
from pygame.event import Event
from pygame.font import Font

from conways.logic import State, Position, logger

logger.success(f"{__name__} importing...")


# noinspection PyMissingOrEmptyDocstring
class Cell(Protocol):
    x: int
    y: int
    state: State


# noinspection PyMissingOrEmptyDocstring
class Board(Protocol):
    board: list[list[Cell]]
    board_size: int

    def generation(self) -> Board:
        ...

    def toggle_cell(self, cell: Position) -> Board:
        ...


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

    def __init__(self, board, *, height: int = 800, width: int = 800, fps: int = 60):
        if not pygame.get_init():
            pygame.init()

        pygame.display.set_caption("Conway's Game of Life")
        self.fps = fps
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        self.board: Board = board
        self.paused: bool = True
        self.clock = pygame.time.Clock()
        self.background = pygame.color.Color(10, 10, 10)
        self.cell_size = width // self.board.board_size
        self.toggle_cells: set[Position] = set()
        self.timer_font = PygameFont(position=Position(10, 10))

    def run(self):
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                self.event_handler(event)
            if not self.paused:
                self.clock.tick(self.fps)
                self.board.generation()
            else:
                self.clock.tick()
                self.toggle()
            self.update_display()

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

    def quit(self):
        logger.debug(f"pygame quiting.")
        pygame.quit()
        sys.exit()

    def update_display(self):
        self.window.fill(self.background)
        self.draw_cells()
        pygame.display.update()

    def draw_cells(self):
        for row in self.board.board:
            for cell in row:
                rect = pygame.Rect(
                    self.cell_size * cell.x,
                    self.cell_size * cell.y,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(surface=self.window, color=cell.state.value, rect=rect)

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
            self.board.toggle_cell(cell)
        self.toggle_cells.clear()
