from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from ..time import Clock
from ..utils._checks import check_type, check_value, ensure_int
from ..utils._docs import copy_doc
from .backend import BACKENDS
from .backend._base import BaseBackend

if TYPE_CHECKING:
    from collections.abc import Sequence

    from numpy.typing import NDArray

    from ..time import BaseClock


class BaseSound(ABC):
    """Base audio stimulus class."""

    @abstractmethod
    def __init__(
        self,
        duration: float | NDArray[np.float32 | np.float64],
        sample_rate: int | None,
        device: int | None,
        n_channels: int = 1,
        *,
        backend: str,
        clock: BaseClock,
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
        self._n_channels = ensure_int(n_channels, "n_channels")
        if self._n_channels < 1:
            raise ValueError(
                "The number of channels must be at least 1. Provided "
                f"'{self._n_channels}' is invalid."
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


class Tone(BaseSound):
    """Pure ton stimulus at the frequency ``f`` (Hz)."""

    def __init__(
        self,
        frequency: float,
        volume: float | Sequence[float],
        duration: float,
        sample_rate: int | None = None,
        device: int | None = None,
        n_channels: int = 1,
        *,
        backend: str = "sounddevice",
        clock: BaseClock = Clock,
        **kwargs,
    ) -> None:
        _check_frequency(frequency)
        self._frequency = frequency
        _check_volume(volume)
        self._volume = volume
        super().__init__(
            duration,
            sample_rate,
            device,
            n_channels,
            backend=backend,
            clock=clock,
            **kwargs,
        )

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        tone_arr = np.sin(2 * np.pi * self._frequency * self._times)
        tone_arr /= np.max(np.abs(tone_arr))  # normalize
        self._signal = np.vstack((tone_arr, tone_arr)).T * self._volume / 100
        if self._window is not None:
            self._signal = np.multiply(self._window, self._signal.T).T
        self._signal = self._signal.astype(np.float32)


def _check_frequency(frequency: float) -> None:
    """Check that the frequency is valid."""
    check_type(frequency, ("numeric",), item_name="frequency")
    if frequency <= 0:
        raise ValueError(
            f"The frequency must be a strictly positive number. Provided '{frequency}' "
            "is invalid."
        )


def _check_volume(volume) -> None:
    """Check that the volume is valid."""
