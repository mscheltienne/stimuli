"""Pure tone sound."""

from typing import Tuple, Union

import numpy as np

from ..utils._checks import _check_type
from ..utils._docs import copy_doc, fill_doc
from ._sound import _Sound


@fill_doc
class Tone(_Sound):
    """Pure tone stimulus at the frequency f (Hz).

    The equation is sin(2*pi*f*time).
    Example: A 440 - La 440 - Tone(f=440)

    Parameters
    ----------
    %(audio_volume)s
    %(audio_sample_rate)s
    %(audio_duration)s
    frequency : float
        Pure tone frequency. The default is 440 Hz (La - A440).
    """

    def __init__(
        self,
        volume: Union[float, Tuple[float, float]],
        sample_rate: int = 44100,
        duration: int = 1,
        frequency: float = 440,
    ):
        self._frequency = Tone._check_frequency(frequency)
        self.name = "tone"
        super().__init__(volume, sample_rate, duration)

    @copy_doc(_Sound._set_signal)
    def _set_signal(self) -> None:
        tone_arr = np.sin(2 * np.pi * self._frequency * self._time_arr)
        self._signal = np.vstack((tone_arr, tone_arr)).T * self._volume / 100

    # --------------------------------------------------------------------
    @staticmethod
    def _check_frequency(frequency: float) -> float:
        """Check if the frequency is positive."""
        _check_type(frequency, ("numeric",), item_name="frequency")
        assert 0 < frequency
        return frequency

    # --------------------------------------------------------------------
    @property
    def frequency(self) -> float:
        """Sound's pure tone frequency [Hz]."""
        return self._frequency

    @frequency.setter
    def frequency(self, frequency: float):
        self._frequency = Tone._check_frequency(frequency)
        self._set_signal()
