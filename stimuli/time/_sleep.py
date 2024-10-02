from __future__ import annotations

import time
from typing import TYPE_CHECKING

from ._clock import Clock

if TYPE_CHECKING:
    from . import BaseClock


def sleep(duration: float, *, clock: BaseClock = Clock) -> None:
    """High precision sleep function.

    Parameters
    ----------
    duration : float
        Duration to sleep in seconds. If the value is less than or equal to 0, the
        function returns immediately.
    clock : BaseClock
        Clock object to use for time measurement. By default, the
        :class:`stimuli.time.Clock` class is used.

    Notes
    -----
    On Windows, only python version 3.11 and above have good accuracy when sleeping.
    This accuracy limitation dictates the minimum version of ``stimuli``.
    """
    if duration <= 0:
        return
    clock = clock()
    duration = int(duration * 1e9)
    while True:
        remaining_time = duration - clock.get_time_ns()  # nanoseconds
        if remaining_time <= 0:
            break
        if remaining_time >= 200000:  # 200 microseconds
            time.sleep(remaining_time * 1e-9 / 2)
