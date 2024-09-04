from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from ..time import Clock
from ..utils._checks import check_value
from .backend import BACKENDS

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
    ) -> None:
        check_value(backend, BACKENDS, "backend")

        self._backend = BACKENDS[backend]

    def _set_times(self) -> None:
        """Set the timestamp array."""
        self._times = np.linspace(
            0, self._duration, int(self._duration * self._sample_rate), endpoint=True
        )

    @abstractmethod
    def _set_signal(self) -> None:
        """Set the signal array."""

    def init_backend(self) -> None:
        """Initialize the backend."""
        self._backend.init_backend(self._signal, self._sample_rate)
        self._backend.start()
