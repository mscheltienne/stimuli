from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..time import Clock
from ..utils._checks import check_type
from ..utils._docs import copy_doc
from ..utils.logs import logger
from ._base import BaseSound, _check_volume

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..time import BaseClock


class Tone(BaseSound):
    """Pure tone stimulus at a given frequency."""

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
        tone_arr = np.sin(2 * np.pi * self._frequency * self._times, dtype=np.float32)
        tone_arr /= np.max(np.abs(tone_arr))  # normalize
        signal = np.vstack([tone_arr] * self._n_channels).T * self._volume / 100
        signal = np.ascontiguousarray(signal)  # C-contiguous array
        signal.astype(np.float32)  # sanity-check
        self._signal = signal

    @property
    def frequency(self) -> float:
        """The frequency of the tone in Hz."""
        return self._frequency

    @frequency.setter
    def frequency(self, frequency: float) -> None:
        logger.debug("Setting 'frequency' to %.2f [Hz].", frequency)
        _check_frequency(frequency)
        self._frequency = frequency
        self._backend.close()
        self._set_signal()


def _check_frequency(frequency: float) -> None:
    """Check that the frequency is valid."""
    check_type(frequency, ("numeric",), item_name="frequency")
    if frequency <= 0:
        raise ValueError(
            f"The frequency must be a strictly positive number. Provided '{frequency}' "
            "is invalid."
        )
