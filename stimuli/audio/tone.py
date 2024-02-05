"""Pure tone sound."""

import numpy as np

from ..utils._checks import check_type
from ..utils._docs import copy_doc, fill_doc
from ..utils.logs import logger
from .base import BaseSound


@fill_doc
class Tone(BaseSound):
    """Pure tone stimulus at the frequency f (Hz).

    The equation is:

    .. code-block::

        sin(2*pi*f*time).

    Example: A 440 - La 440 - Tone(f=440)

    Parameters
    ----------
    %(audio_volume)s
    %(audio_sample_rate)s
    %(audio_duration)s
    frequency : float
        Pure tone frequency. The default is 440 Hz (La - A440).

    Examples
    --------
    ``A 440``, also called ``La 440``, corresponds to a pure tone at a
    frequency of 440 Hz.
    """

    def __init__(
        self,
        volume: float | tuple[float, float],
        sample_rate: int = 44100,
        duration: float = 1,
        frequency: float = 440,
    ):
        self._frequency = Tone._check_frequency(frequency)
        self.name = "tone"
        super().__init__(volume, sample_rate, duration)

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        tone_arr = np.sin(2 * np.pi * self._frequency * self._times)
        tone_arr /= np.max(np.abs(tone_arr))  # normalize
        self._signal = np.vstack((tone_arr, tone_arr)).T * self._volume / 100
        super()._set_signal()

    # --------------------------------------------------------------------
    @staticmethod
    def _check_frequency(frequency: float) -> float:
        """Check if the frequency is positive."""
        check_type(frequency, ("numeric",), item_name="frequency")
        assert 0 < frequency
        return frequency

    # --------------------------------------------------------------------
    @property
    def frequency(self) -> float:
        """Sound's pure tone frequency [Hz]."""
        logger.debug("'self._frequency' is set to %.2f [Hz].", self._frequency)
        return self._frequency

    @frequency.setter
    def frequency(self, frequency: float):
        logger.debug("Setting 'frequency' to %.2f [Hz].", frequency)
        self._frequency = Tone._check_frequency(frequency)
        self._set_signal()
