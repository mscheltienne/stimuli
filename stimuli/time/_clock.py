import time


class Clock:
    """Clock which keeps track of time in nanoseconds.

    The 0 corresponds to the creation of the :class:`stimuli.time.Clock` object.
    """

    def __init__(self):
        self._t0 = time.monotonic_ns()

    def get_time_ns(self) -> int:
        """Return the current time in nanoseconds."""
        return time.monotonic_ns() - self._t0

    def get_time_us(self) -> float:
        """Return the current time in microseconds."""
        return self.get_time_ns() / 1e3

    def get_time_ms(self) -> float:
        """Return the current time in milliseconds."""
        return self.get_time_ns() / 1e6

    def get_time(self) -> float:
        """Return the current time in seconds."""
        return self.get_time_ns() / 1e9
