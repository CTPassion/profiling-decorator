"""Inputs validation methods

VALID SORTS - set of extracted valid sorting criteria for profile statistics
"""

import logging
import os
from pathlib import Path
from pstats import SortKey
from typing import Sequence, Union

VALID_SORTS = set(map(str, SortKey))


def validate_sort_by(sort_by) -> Union[str, Sequence[str]]:
    """
    Validates the sort_by parameter to ensure it is valid with the pstats module.
    Raises a ValueError with appropriate message if validation fails.

    :param sort_by: The sort_by value to validate. Can be a str or sequence of
                    str corresponding to valid pstats sort by options.
    :return: Sequence: The sort_by provided as was, or put into a list if initally
                       a string.
    :raises: ValueError: If the str is not a valid sort by option, or any of the
                         str in a sequence are not valid sort by options.
    """
    if isinstance(sort_by, str):
        sort_by = [sort_by]
    if not sort_by:
        raise ValueError("sort_by cannot be None or empty.")
    invalid_sorts = set(sort_by) - VALID_SORTS
    if invalid_sorts:
        raise ValueError(
            f"Invalid sort_by options: {invalid_sorts}."
            f" Valid options are: {VALID_SORTS}."
        )
    return sort_by


def validate_destination(destination) -> None:
    """
    Validates the destination parameter to ensure it is of an appropriate type.
    Raises a ValueError with an appropriate message if the validation fails.

    :param destination: The destination to validate. Can be None, a string or Path
                        representing a file path, a logging.Logger object, or an IO
                        object like sys.stdout or sys.stderr.
    :return: None
    :raises: ValueError: If the destination is not a valid type or if a specified path
                         does not exist or is not writable as required.
    """

    # Allow None for default behavior (e.g., sys.stdout)
    if destination is None:
        return

    # Check for IO objects by attempting to access a 'write' method
    if hasattr(destination, "write"):
        return

    # Check for logging.Logger instance
    if isinstance(destination, logging.Logger):
        return

    # Validate paths (string or Path)
    if isinstance(destination, (str, Path)):
        destination_path = Path(destination)  # Convert to Path object if not already
        if not destination_path.parent.exists() or not destination_path.parent.is_dir():
            raise ValueError(
                f"Directory for the given path does not exist or is not a directory:"
                f" {destination_path.parent}"
            )

        # Additional check: If the file exists, check it is writable
        if destination_path.exists() and not os.access(destination_path, os.W_OK):
            raise ValueError(f"The file at {destination_path} is not writable.")
        return
    # If none of the above checks pass, the destination is invalid
    raise ValueError(
        "Invalid destination. Must be a path (str or Path), a logging.Logger,"
        " an IO object, or None."
    )
