from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..time import Clock
from ..utils._checks import check_type
from ..utils._docs import copy_doc, fill_doc
from ..utils.logs import logger
from ._base import BaseSound

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


@fill_doc
class Tone(BaseSound):
    """Pure tone stimulus at a given frequency.

    Parameters
    ----------
    frequency : float
        Frequency of the tone in Hz.
    %(audio_volume)s
    %(audio_duration)s
    %(audio_sample_rate)s
    %(audio_device)s
    %(audio_n_channels)s
    %(audio_backend)s
    %(clock)s
    %(audio_kwargs)s
    """

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
        clock: Callable = Clock,
        **kwargs,
    ) -> None:
        _check_frequency(frequency)
        self._frequency = frequency
        super().__init__(
            volume,
            duration,
            sample_rate,
            device,
            n_channels,
            backend=backend,
            clock=clock,
            **kwargs,
        )

    def __repr__(self) -> str:
        """Representation of the object."""
        return f"<Pure tone @ {self.frequency:.2f} Hz - {self.duration:.2f} s>"

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        signal = np.sin(2 * np.pi * self._frequency * self._times, dtype=np.float32)
        signal /= np.max(np.abs(signal))  # normalize
        signal = np.vstack([signal] * self._n_channels).T
        super()._set_signal(signal)

    @property
    def frequency(self) -> float:
        """The frequency of the tone in Hz.

        :type: :class:`float`
        """
        return self._frequency

    @frequency.setter
    def frequency(self, frequency: float) -> None:
        logger.debug("Setting 'frequency' to %.2f [Hz].", frequency)
        _check_frequency(frequency)
        self._frequency = frequency
        self._set_signal()


def _check_frequency(frequency: float) -> None:
    """Check that the frequency is valid."""
    check_type(frequency, ("numeric",), item_name="frequency")
    if frequency <= 0:
        raise ValueError(
            f"The frequency must be a strictly positive number. Provided '{frequency}' "
            "is invalid."
        )
