"""
ui_args.py



Author: Zack Hankin
Started: 6/02/2023
"""
from __future__ import annotations
import sys
import argparse
from argparse import ArgumentParser
import loguru
from loguru import logger

from icecream import ic

logger.success(f"{__name__} importing...")


def arg_parser() -> ArgumentParser:
    """
    Argument parser constructor for CLI interface.

    Returns:
        ArgumentParser for use.
    """
    parser = argparse.ArgumentParser(prog="Conway's Game of Life")
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="Start with all cells set to random states. Default: False",
        )
    ui_group = parser.add_argument_group("UI Choice")
    ui_choice = ui_group.add_mutually_exclusive_group(required=False)
    ui_choice.add_argument("-p", action="store_true", help="Use Pygame as UI")
    ui_choice.add_argument("-c", action="store_true", help="CLI only")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument(
        "-n", help="Number of iterations to run.", type=int, metavar="int", default=0
        )
    parser.add_argument(
        "-w", "--width", help="Width of grid.", type=int, metavar="int", default=50
        )
    parser.add_argument(
        "-f", "--fps", help="Max FPS", type=int, metavar="int", default=60
        )
    parser.add_argument(
        "-l", "--loading", help="Enable loading bar for set number of iterations.", action="store_true"
        )

    return parser


class Options:
    """
    Object to hold the arguments passed in via the CLI.
    """
    fps: int
    width: int
    random: bool
    loading: bool
    p: bool
    c: bool
    n: int
    verbose: int
    log_level: loguru.Level
    ui: str | None = None
    verbose_dict: dict[int, str] = {0: "SUCCESS", 1: "INFO", 2: "DEBUG", 3: "TRACE"}

    def __init__(self):
        self.parser = arg_parser()
        self.parser.parse_args(namespace=Options)
        self.set_ui()
        self.set_log_level()

    def set_ui(self) -> Options:
        if self.c:
            self.ui = "CLI"
        if self.p | (self.ui is None):
            self.ui = "pygame"
        return self

    def set_log_level(self) -> Options:
        if self.verbose > 3:
            self.verbose = 3
        level = self.verbose_dict[self.verbose]
        self.log_level = logger.level(level)
        try:
            logger.remove()
        except ValueError:
            ...
        logger.add(sys.stdout, level=self.log_level.name)
        logger.success(f"Log level set to {self.log_level.name.lower()}")
        return self
