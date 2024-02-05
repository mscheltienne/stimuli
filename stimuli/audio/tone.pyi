from _typeshed import Incomplete

from ..utils._checks import check_type as check_type
from ..utils._docs import copy_doc as copy_doc
from ..utils._docs import fill_doc as fill_doc
from ..utils.logs import logger as logger
from .base import BaseSound as BaseSound

class Tone(BaseSound):
    """Pure tone stimulus at the frequency f (Hz).

    The equation is:

    .. code-block::

        sin(2*pi*f*time).

    Example: A 440 - La 440 - Tone(f=440)

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
    frequency : float
        Pure tone frequency. The default is 440 Hz (La - A440).

    Examples
    --------
    ``A 440``, also called ``La 440``, corresponds to a pure tone at a
    frequency of 440 Hz.
    """

    _frequency: Incomplete
    name: str

    def __init__(
        self,
        volume: float | tuple[float, float],
        sample_rate: int = 44100,
        duration: float = 1,
        frequency: float = 440,
    ) -> None: ...
    _signal: Incomplete

    def _set_signal(self) -> None:
        """Set the signal in the numpy array ._signal played by sounddevice."""

    @staticmethod
    def _check_frequency(frequency: float) -> float:
        """Check if the frequency is positive."""

    @property
    def frequency(self) -> float:
        """Sound's pure tone frequency [Hz]."""

    @frequency.setter
    def frequency(self, frequency: float):
        """Sound's pure tone frequency [Hz]."""
