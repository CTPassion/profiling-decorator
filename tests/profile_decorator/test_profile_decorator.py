"""Unit tests using pytest for profiling decorator"""

import asyncio
import logging
import os
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

    @profile(output="file", filename=filename)
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

        @profile(output="invalid_option")
        def test_func():
            pass

        test_func()


def test_logging_output(caplog):
    """Test logging output functionality."""

    @profile(output="log")
    def test_func():
        return sum(range(10))

    with caplog.at_level(logging.INFO):
        test_func()

    # Check if logging captured profile output
    assert len(caplog.records) > 0, "No logging output captured."
    assert "function calls" in caplog.text, "Profile output not captured in logs."
