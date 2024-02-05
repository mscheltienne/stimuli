from _typeshed import Incomplete

from ..utils._checks import check_type as check_type
from ..utils._checks import check_value as check_value
from ..utils._docs import copy_doc as copy_doc
from ..utils._docs import fill_doc as fill_doc
from ..utils.logs import logger as logger
from .base import BaseSound as BaseSound

class SoundAM(BaseSound):
    """Amplitude modulated sound.

    Composed of a carrier frequency ``fc`` which is amplitude modulated at
    ``fm``. By default, an Auditory Steady State Response stimuli composed of
    a ``1000`` Hz carrier frequency modulated at ``40`` Hz through conventional
    modulation is created.

    Parameters
    ----------
    volume : float | tuple
        If an int or a float is provided, the sound will use only one channel
        (mono). If a 2-length tuple is provided, the sound will use 2
        channels (stereo). The volume of each channel is given between 0 and 100.
        For stereo, the volume is given as (L, R).
    sample_rate : float
        Sampling frequency of the sound. The default is 44100 Hz.
    duration : float
        Duration of the sound. The default is 1 second.
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

    _frequency_carrier: Incomplete
    _frequency_modulation: Incomplete
    _method: Incomplete
    name: Incomplete

    def __init__(
        self,
        volume: float | tuple[float, float],
        sample_rate: int = 44100,
        duration: float = 1,
        frequency_carrier: float = 1000,
        frequency_modulation: float = 40,
        method: str = "conventional",
    ) -> None: ...
    _signal: Incomplete

    def _set_signal(self) -> None:
        """Set the signal in the numpy array ._signal played by sounddevice."""

    @staticmethod
    def _check_frequency_carrier(frequency_carrier: float) -> float:
        """Check if the carrier frequency is positive."""

    @staticmethod
    def _check_frequency_modulation(frequency_modulation: float) -> float:
        """Check if the modulation frequency is positive."""

    @property
    def frequency_carrier(self) -> float:
        """Sound's carrier frequency [Hz]."""

    @frequency_carrier.setter
    def frequency_carrier(self, frequency_carrier: float):
        """Sound's carrier frequency [Hz]."""

    @property
    def frequency_modulation(self) -> float:
        """Sound's modulation frequency [Hz]."""

    @frequency_modulation.setter
    def frequency_modulation(self, frequency_modulation: float):
        """Sound's modulation frequency [Hz]."""

    @property
    def method(self) -> str:
        """Sound's modulation method."""

    @method.setter
    def method(self, method: str):
        """Sound's modulation method."""
