import numpy as np
from _typeshed import Incomplete

from ..utils._checks import check_type as check_type
from ..utils._checks import check_value as check_value
from ..utils._docs import copy_doc as copy_doc
from ..utils._docs import fill_doc as fill_doc
from ..utils.logs import logger as logger
from .base import BaseSound as BaseSound

_PSDS: Incomplete

class Noise(BaseSound):
    """Colored noise stimulus.

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
    color : str
        The noise color. Available colors are: ``'white'``, ``'pink'``,
        ``'blue'``, ``'violet'`` and ``'brown'``.
    """

    _color: Incomplete
    _rng: Incomplete
    name: Incomplete

    def __init__(
        self,
        volume: float | tuple[float, float],
        sample_rate: int = 44100,
        duration: float = 1,
        color: str = "white",
    ) -> None: ...
    _signal: Incomplete

    def _set_signal(self) -> None:
        """Set the signal in the numpy array ._signal played by sounddevice."""

    @staticmethod
    def _noise_psd(rng: np.random.Generator, N: int, color: str):
        """Compute the noise signal 1D array."""

    @property
    def color(self) -> str:
        """The noise color."""

    @color.setter
    def color(self, color: str):
        """The noise color."""
