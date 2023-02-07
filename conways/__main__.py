"""
Conways Game of Life

Author: Zack Hankin
Started: 2/02/2023
"""
from __future__ import annotations

import os
import sys
from typing import Protocol

from icecream import ic
from conways import Board, CLI, PygameUI, Timer, Options
from conways.logic import logger, Condition


# noinspection PyMissingOrEmptyDocstring
class UIType(Protocol):
    _board: Board

    def run(self):
        ...


def setup_ui(args: Options, board: Board) -> UIType:
    ui: UIType
    match args.ui:
        case None:
            args.set_ui()
            return setup_ui(args, board)
        case "pygame":
            ui = PygameUI(board=board, fps=args.fps)
        case "CLI":
            ui = CLI(board, number_of_generations=args.n)
    return ui


def main() -> int:
    try:
        logger.success("Started Conway's Game of Life")
        options = Options()
        logger.debug(f"UI: {options.ui}")
        board = Board(options.width, num_of_runs=options.n, loading_bar=options.loading)
        logger.info(f"Total number of cells: {len(board):,}")
        ui = setup_ui(options, board)
        if options.random:
            board.set_random_board()
        ui.run()
    except KeyboardInterrupt:
        logger.success('Exited Program via KeyboardInterrupt')
    except Exception as error:
        logger.exception(f'{error.__class__.__name__}: {error.args[0]}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
