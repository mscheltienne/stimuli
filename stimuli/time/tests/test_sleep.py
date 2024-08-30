import time

import pytest

from stimuli.time import sleep


@pytest.mark.parametrize("duration", [-1, 0, 0.1, 0.5, 1.0])
def test_sleep(duration):
    """Test sleeping function."""
    start = time.monotonic_ns()
    sleep(duration)
    stop = time.monotonic_ns()
    # test in seconds with 200 microsecond headroom
    assert (stop - start) * 1e-9 <= max(duration, 0) + 2e-4
