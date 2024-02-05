"""Amplitude modulated sound."""

import numpy as np

from ..utils._checks import check_type, check_value
from ..utils._docs import copy_doc, fill_doc
from ..utils.logs import logger
from .base import BaseSound


@fill_doc
class SoundAM(BaseSound):
    """Amplitude modulated sound.

    Composed of a carrier frequency ``fc`` which is amplitude modulated at
    ``fm``. By default, an Auditory Steady State Response stimuli composed of
    a ``1000`` Hz carrier frequency modulated at ``40`` Hz through conventional
    modulation is created.

    Parameters
    ----------
    %(audio_volume)s
    %(audio_sample_rate)s
    %(audio_duration)s
    frequency_carrier : int
        Carrier frequency in Hz.
    frequency_modulation : int
        Modulatiom frequency in Hz.
    method : ``'conventional'`` | ``'dsbsc'``
        ``'conventional'`` is also called classical AM, the eq. used is::

                signal = (1 - M(t)) * cos(2*pi*fc*t)
                M(t) = cos(2*pi*fm*t)

        ``'dsbsc'`` is also called double side band suppressed carrier, the eq.
        used is::

                signal = M(t)*cos(2*pi*fc*t)
                M(t) = sin(2*pi*fm*t)
    """

    def __init__(
        self,
        volume: float | tuple[float, float],
        sample_rate: int = 44100,
        duration: float = 1,
        frequency_carrier: float = 1000,
        frequency_modulation: float = 40,
        method: str = "conventional",
    ):
        self._frequency_carrier = SoundAM._check_frequency_carrier(frequency_carrier)
        self._frequency_modulation = SoundAM._check_frequency_modulation(
            frequency_modulation
        )
        check_type(method, (str,), "method")
        check_value(method, ("conventional", "dsbsc"), "AM method")
        self._method = method
        self.name = f"AM {self._method}"
        super().__init__(volume, sample_rate, duration)

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        if self._method == "conventional":
            amplitude = 1 - np.cos(2 * np.pi * self._frequency_modulation * self._times)
            arr = amplitude * np.cos(2 * np.pi * self._frequency_carrier * self._times)

        elif self._method == "dsbsc":
            amplitude = np.sin(2 * np.pi * self._frequency_modulation * self._times)
            arr = amplitude * np.sin(2 * np.pi * self._frequency_carrier * self._times)
        arr /= np.max(np.abs(arr))  # normalize
        self._signal = np.vstack((arr, arr)).T * self._volume / 100
        super()._set_signal()

    # --------------------------------------------------------------------
    @staticmethod
    def _check_frequency_carrier(frequency_carrier: float) -> float:
        """Check if the carrier frequency is positive."""
        check_type(frequency_carrier, ("numeric",), item_name="frequency_carrier")
        assert 0 < frequency_carrier
        return frequency_carrier

    @staticmethod
    def _check_frequency_modulation(frequency_modulation: float) -> float:
        """Check if the modulation frequency is positive."""
        check_type(
            frequency_modulation,
            ("numeric",),
            item_name="frequency_modulation",
        )
        assert 0 < frequency_modulation
        return frequency_modulation

    # --------------------------------------------------------------------
    @property
    def frequency_carrier(self) -> float:
        """Sound's carrier frequency [Hz]."""
        logger.debug(
            "'self._frequency_carrier' is set to %.2f [Hz].",
            self._frequency_carrier,
        )
        return self._frequency_carrier

    @frequency_carrier.setter
    def frequency_carrier(self, frequency_carrier: float):
        logger.debug("Setting 'frequency_carrier' to %.2f [Hz].", frequency_carrier)
        self._frequency_carrier = SoundAM._check_frequency_carrier(frequency_carrier)
        self._set_signal()

    @property
    def frequency_modulation(self) -> float:
        """Sound's modulation frequency [Hz]."""
        logger.debug(
            "'self._frequency_modulation' is set to %.2f [Hz].",
            self._frequency_modulation,
        )
        return self._frequency_modulation

    @frequency_modulation.setter
    def frequency_modulation(self, frequency_modulation: float):
        logger.debug(
            "Setting 'frequency_modulation' to %.2f [Hz].",
            frequency_modulation,
        )
        self._frequency_modulation = SoundAM._check_frequency_modulation(
            frequency_modulation
        )
        self._set_signal()

    @property
    def method(self) -> str:
        """Sound's modulation method."""
        logger.debug("'self._method' is set to %s.", self._method)
        return self._method

    @method.setter
    def method(self, method: str):
        logger.debug("Setting 'method' to %s.", method)
        check_type(method, (str,), "method")
        check_value(method, ("conventional", "dsbsc"), "AM method")
        self._method = method
        self._set_signal()
