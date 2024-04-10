"""Unit tests using pytest for profiling decorator"""

import asyncio
import logging
import os
import time

import pytest

from src.profiling_decorator import profile

# Logger for capturing log output tests
logger = logging.getLogger("test_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)


def test_sync_function_profiling():
    """Test profiling of a synchronous function."""

    @profile
    def test_func():
        return sum(range(100))

    # The function should run without errors and return the correct result
    assert test_func() == sum(
        range(100)
    ), "The profiled function does not return the expected result."


@pytest.mark.asyncio
async def test_async_function_profiling():
    """Test profiling of an asynchronous function."""

    @profile
    async def test_async_func():
        await asyncio.sleep(0.1)  # Simulate async operation
        return "async result"

    # The function should run without errors and return the correct result
    assert (
        await test_async_func() == "async result"
    ), "The profiled async function does not return the expected result."


def test_output_to_file():
    """Test output to file functionality."""
    filename = "test_profile_output.txt"

    @profile(destination=filename)
    def test_func():
        return sum(range(10))

    test_func()

    # Check if the file was created and has content
    assert os.path.exists(filename), "Output file was not created."
    assert os.path.getsize(filename) > 0, "Output file is empty."

    # Cleanup
    os.remove(filename)


def test_invalid_output_option():
    """Test handling of invalid output option."""
    with pytest.raises(ValueError):

        @profile(destination=12)
        def test_func():
            pass

        test_func()

    with pytest.raises(ValueError):

        @profile(destination=logging.StreamHandler)
        def test_func():
            pass

        test_func()


def test_logging_output(caplog):
    """Test logging output functionality."""

    tlogger = logging.getLogger("test_logger")
    tlogger.setLevel(logging.INFO)

    @profile(destination=tlogger)
    def test_func():
        return sum(range(10))

    with caplog.at_level(logging.INFO):
        test_func()

    # Assert on the log messages captured by caplog
    assert len(caplog.records) == 1  # Check the number of log messages captured
    assert caplog.records[0].levelno == logging.INFO  # Check the log level
    assert caplog.records[0].name == "test_logger"  # Check the logger name
    assert 'test_func' in caplog.text
