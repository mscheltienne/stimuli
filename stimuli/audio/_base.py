from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from ..utils._checks import check_type, check_value, ensure_int
from ..utils._docs import copy_doc
from .backend import BACKENDS
from .backend._base import BaseBackend

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from ..time import BaseClock


class BaseSound(ABC):
    """Base audio stimulus class.

    Parameters
    ----------
    duration : float
        Duration of the sound in seconds, used to generate the time array.
    sample_rate : int | None
        Sample rate of the sound. If None, the default sample rate of the device
        provided by the backend is used.
    device : int | None
        Device index to use for sound playback. If None, the default device provided
        by the backend is used.
    n_channels : int
        Number of channels of the sound.
    backend : ``"sounddevice"``
        The backend to use for sound playback.
    clock : BaseClock
        Clock object to use for timing measurements.
    **kwargs
        Additional keyword arguments passed to the backend initialization.
    """

    @abstractmethod
    def __init__(
        self,
        duration: float,
        sample_rate: int | None,
        device: int | None,
        n_channels: int = 1,
        *,
        backend: str,
        clock: BaseClock,
        **kwargs,
    ) -> None:
        check_type(backend, (str,), "backend")
        check_value(backend, BACKENDS, "backend")
        check_type(duration, ("numeric",), "duration")
        if duration <= 0:
            raise ValueError(
                "The argument 'duration' must be a strictly positive number defining "
                f"the length of the sound in seconds. Provided '{duration}' is invalid."
            )
        self._duration = duration
        self._n_channels = ensure_int(n_channels, "n_channels")
        if self._n_channels < 1:
            raise ValueError(
                "The number of channels must be at least 1. Provided "
                f"'{self._n_channels}' is invalid."
            )
        # the arguments sample_rate, device, clock, and **kwargs are checked in
        # the backend initialization.
        self._backend_kwargs = kwargs
        self._backend = BACKENDS[backend](sample_rate, device, clock=clock)
        self._set_times()
        self._set_signal()

    def _set_times(self) -> None:
        """Set the timestamp array."""
        self._times = np.linspace(
            0, self.duration, int(self.duration * self.sample_rate), endpoint=True
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

    @property
    def duration(self) -> float:
        """The duration of the audio stimulus."""
        return self._duration

    @property
    def sample_rate(self) -> int:
        """The sample rate of the audio stimulus."""
        return self._backend.sample_rate

    @property
    def _signal(self) -> NDArray[np.float32]:
        """The audio signal."""
        return self._signal_array

    @_signal.setter
    def _signal(self, signal: NDArray[np.float32]) -> None:
        self._signal_array = signal
        self._backend.initialize(self._signal_array, **self._backend_kwargs)


def _check_volume(volume) -> None:
    """Check that the volume is valid."""
