from __future__ import annotations

import time
from typing import TYPE_CHECKING

import pytest

from stimuli.time import sleep

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.fixture(scope="module")
def time_func_ns() -> Callable:
    """Return the time measurement function."""
    if (
        time.get_clock_info("perf_counter").resolution
        < time.get_clock_info("monotonic").resolution
    ):
        return lambda: time.perf_counter() * 1e9
    else:
        return time.monotonic_ns


@pytest.mark.xfail(reason="Depends on the system clock.")
@pytest.mark.parametrize("duration", [-1, 0, 0.1, 0.5, 1.0])
def test_sleep(duration, time_func_ns):
    """Test sleeping function."""
    start = time_func_ns()
    sleep(duration)
    stop = time_func_ns()
    # test in seconds with 500 microsecond headroom
    assert (stop - start) * 1e-9 <= max(duration, 0) + 5e-4
