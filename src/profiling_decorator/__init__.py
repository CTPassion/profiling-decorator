"""profiling decorator definition

DEFAULT_ROWS = The default number of rows to limit output of CProfile to.
"""

import sys

assert sys.version_info >= (3, 8)

import asyncio
import cProfile
import io
import logging
import pstats
from functools import wraps
from pathlib import Path
from typing import IO, Any, Callable, Sequence, Union

from .validation import validate_destination, validate_sort_by

DEFAULT_ROWS = 50


def profile(
    n_rows: int = DEFAULT_ROWS,
    sort_by: Union[str, Sequence[str]] = "cumulative",
    destination: Union[str, Path, logging.Logger, IO] = sys.stdout,
) -> Callable[..., Any]:
    """
    Decorator to profile a function.

    Args:
        n_rows: Number of rows to reduce profile output to.
        sort_by: What statistic(s) to sort by in the results.
        destination: The output destination, which can be a file path
                     (string or Path object), sys.stdout, sys.stderr,
                     or a custom-configured logger.
    Returns:
        func return

    Raises:
        ValueError: Invalid value for parameter.
        IOError: Error writing to file.
    """

    # Initial validation
    validate_destination(destination)
    sort_by = validate_sort_by(sort_by)

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            with cProfile.Profile() as pr:
                # Directly await the async function here
                result = await func(*args, **kwargs)
                process_profiling_results(pr)

            return result

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            with cProfile.Profile() as pr:
                result = func(*args, **kwargs)
                process_profiling_results(pr)

            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    def process_profiling_results(pr: cProfile.Profile) -> None:
        s = io.StringIO()

        ps = pstats.Stats(pr, stream=s).sort_stats(*sort_by)
        ps.print_stats(n_rows)

        # Now, handle the different types of destinations
        if isinstance(destination, (str, Path)):
            # When destination is a string or Path, treat it as a file path
            destination_path = str(destination)  # Ensure it's a string for open()
            try:
                with open(destination_path, "w+", encoding="utf-8") as f:
                    f.write(s.getvalue())
            except IOError as e:
                raise IOError(f"Error writing to file {destination_path}: {e}") from e
        elif isinstance(destination, logging.Logger):
            # When destination is a Logger, log the profiling results
            destination.info(s.getvalue())
        else:
            # For file-like objects (including sys.stdout and sys.stderr),
            # directly write to them
            destination.write(s.getvalue())

    # Enable the decorator to be used without parentheses if no arguments are provided
    if callable(n_rows):
        temp_func = n_rows
        return decorator(temp_func)

    return decorator
