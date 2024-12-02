import pytest

from stimuli.time import Clock


@pytest.mark.xfail(reason="Depends on the system clock.")
def test_clock():
    """Test the clock object."""
    # test t0 with 20 microseconds headroom
    clock = Clock()
    assert clock.get_time_ns() <= 2e4
    clock = Clock()
    assert clock.get_time_us() <= 20
    clock = Clock()
    assert clock.get_time_ms() <= 0.02
    clock = Clock()
    assert clock.get_time() <= 2e-5
    # test consecutive calls
    clock = Clock()
    t1 = clock.get_time_ns()
    t2 = clock.get_time_ns()
    assert t1 < t2


def test_reset():
    """Test the clock reset method."""
    clock = Clock()
    t0 = clock.t0
    assert isinstance(t0, float)
    clock.reset()
    assert t0 < clock.t0
