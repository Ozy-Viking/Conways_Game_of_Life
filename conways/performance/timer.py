"""
timer.py



Author: Zack Hankin
Started: 4/02/2023
"""
from __future__ import annotations
import time
from typing import Any, Callable
import functools
from conways.logic.util import logger
from icecream import ic

logger.success(f"{__name__} importing...")


class Timer:
    """
    Timer decorator for measuring runtimes in nanoseconds.

    Access times through 'times' property of the function/method.
    """

    cached_time: dict[str, list[int]] = dict()

    def __init__(self, function: Callable[[...], ...]):
        self.name = function.__name__
        self.cached_time[self.name] = list()
        self.function: Callable[[...], ...] = function
        functools.update_wrapper(self, function)

    def __call__(self, *args, **kwargs) -> Any:
        ic(*args, **kwargs)
        start = time.perf_counter_ns()

        result = self.function(*args, **kwargs)
        end = time.perf_counter_ns()
        self.cached_time[self.name].append(end - start)
        return result

    # Todo: Fix this hack. Maybe run as a generator function or run the init. Or change to def then class.
    @staticmethod
    def time(function):
        Timer.cached_time[function.__name__] = list()

        def wrapper(slf, *args, **kwargs):
            start = time.perf_counter_ns()
            result = function(slf, *args, **kwargs)
            end = time.perf_counter_ns()
            Timer.cached_time[function.__name__].append(end - start)
            return result

        return wrapper

    @property
    def times(self) -> list[int]:
        """
        Returns:
            List of run times in order.
        """
        return self.cached_time[self.name]


# class Demo:
#
#     @Timer
#     def timeme(self):
#         time.sleep(1)
#
#
# d = Demo()
#
# d.timeme()
