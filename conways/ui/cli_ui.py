"""
cli_ui.py



Author: Zack Hankin
Started: 6/02/2023
"""
from __future__ import annotations
import sys
import time

from icecream import ic
from conways import Board, logger

logger.success(f"{__name__} importing...")


class CLI:
    def __init__(self, board, *, number_of_generations: int):
        self.number_of_generations = number_of_generations
        self.board: Board = board
        self.time_to_run: int = 0

    def run(self):
        logger.info(f"Starting {self.number_of_generations:,} generation/s.")
        start = time.perf_counter_ns()
        self.board.run_for_set_amount()
        end = time.perf_counter_ns()
        logger.success(f"Finished {self.number_of_generations:,} generation/s.")
        self.time_to_run = end - start
        logger.success(f"Time taken: {self.time_to_run * 10 ** -6:,.2f} ms")
        logger.success(f"Time taken/run: {(self.time_to_run * 10 ** -6) / self.number_of_generations:,.2f} ms/run")
