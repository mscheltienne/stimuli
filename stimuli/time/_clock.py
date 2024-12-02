from __future__ import annotations

import time
from abc import ABC, abstractmethod

from ..utils._docs import copy_doc


class BaseClock(ABC):
    """Base class for high precision clocks.

    If you want to implement a custom clock, you should subclass this class and define
    the abstract method :meth:`stimuli.time.BaseClock.get_time_ns` which should return
    the time elapsed since instantiation in nanoseconds.
    """

    @abstractmethod
    def __init__(self) -> None:
        # the variable 'self._t0' needs to be defined by the end of the __init__ method.
        pass

    @abstractmethod
    def get_time_ns(self) -> int:
        """Return the current time in nanoseconds.

        Returns
        -------
        time : int
            The current time in nanoseconds.
        """

    def get_time_us(self) -> float:
        """Return the current time in microseconds.

        Returns
        -------
        time : float
            The current time in microseconds.
        """
        return self.get_time_ns() / 1e3

    def get_time_ms(self) -> float:
        """Return the current time in milliseconds.

        Returns
        -------
        time : float
            The current time in milliseconds.
        """
        return self.get_time_ns() / 1e6

    def get_time(self) -> float:
        """Return the current time in seconds.

        Returns
        -------
        time : float
            The current time in seconds.
        """
        return self.get_time_ns() / 1e9

    @abstractmethod
    def reset(self) -> None:
        """Reset the clock to zero."""

    @property
    def t0(self) -> float:
        """The time of instantiation of the clock in seconds.

        :type: :class:`float`
        """
        return self._t0 / 1e9


class Clock(BaseClock):
    """Clock which keeps track of time in nanoseconds.

    The origin ``t=0`` corresponds to the instantiation of the
    :class:`stimuli.time.Clock` object. The time is measured either through the
    monotonic :func:`time.monotonic_ns` function or through the performance counter
    :func:`time.perf_counter` function, depending on which one has the highest
    resolution.
    """

    def __init__(self) -> None:
        if (
            time.get_clock_info("perf_counter").resolution
            < time.get_clock_info("monotonic").resolution
        ):
            self._function = time.perf_counter_ns
        else:
            self._function = time.monotonic_ns
        self.reset()

    @copy_doc(BaseClock.get_time_ns)
    def get_time_ns(self) -> int:
        return self._function() - self._t0

    def reset(self) -> None:
        """Reset the clock to zero."""
        self._t0 = self._function()
