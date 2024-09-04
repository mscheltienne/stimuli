from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from ..time import Clock
from ..utils._checks import check_type, check_value
from ..utils._docs import copy_doc
from .backend import BACKENDS
from .backend._base import BaseBackend

if TYPE_CHECKING:
    from ..time import BaseClock


class BaseSound(ABC):
    """Base audio stimulus class."""

    @abstractmethod
    def __init__(
        self,
        sample_rate: float,
        duration: float,
        device: int,
        *,
        backend: str = "sounddevice",
        clock: BaseClock = Clock,
        **kwargs,
    ) -> None:
        check_type(backend, ("str",), "backend")
        check_value(backend, BACKENDS, "backend")
        check_type(duration, ("numeric",), "duration")
        if duration <= 0:
            raise ValueError(
                "The argument 'duration' must be a strictly positive number defining "
                f"the length of the sound in seconds. Provided '{duration}' is invalid."
            )
        self._set_times()
        self._set_signal()
        # the arguments sample_rate, device, clock, and backend_kwargs are checked in
        # the backend initialization.
        self._backend = BACKENDS[backend](
            self._data,
            self._sample_rate,
            self._device,
            clock=clock,
            **kwargs,
        )

    def _set_times(self) -> None:
        """Set the timestamp array."""
        self._times = np.linspace(
            0, self._duration, int(self._duration * self._sample_rate), endpoint=True
        )

    @abstractmethod
    def _set_signal(self) -> None:
        """Set the signal array."""

    @copy_doc(BaseBackend.play)
    def play(self, when: float | None = None) -> None:
        self._backend.play(when=when)

    @copy_doc(BaseBackend.stop)
    def stop(self) -> None:
        self._backend.stop()
