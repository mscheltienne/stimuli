import time

from .clock import Clock


def sleep(duration: float) -> None:
    """High precision sleep function.

    Parameters
    ----------
    duration : float
        Duration to sleep in seconds. If the value is less than or equal to 0, the
        function returns immediately.
    """
    if duration <= 0:
        return
    clock = Clock()
    duration = int(duration * 1e9)
    while True:
        remaining_time = duration - clock.get_time_ns()  # nanoseconds
        if remaining_time <= 0:
            break
        if remaining_time >= 200000:  # 200 microseconds
            time.sleep(remaining_time * 1e-9 / 2)
