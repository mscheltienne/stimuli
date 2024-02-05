"""Colored noise sound."""

import numpy as np

from ..utils._checks import check_type, check_value
from ..utils._docs import copy_doc, fill_doc
from ..utils.logs import logger
from .base import BaseSound

_PSDS = {
    "white": lambda f: 1,
    "blue": lambda f: np.sqrt(f),
    "violet": lambda f: f,
    "pink": lambda f: 1 / np.where(f == 0, np.inf, np.sqrt(f)),
    "brown": lambda f: 1 / np.where(f == 0, np.inf, f),
}


@fill_doc
class Noise(BaseSound):
    """Colored noise stimulus.

    Parameters
    ----------
    %(audio_volume)s
    %(audio_sample_rate)s
    %(audio_duration)s
    color : str
        The noise color. Available colors are: ``'white'``, ``'pink'``,
        ``'blue'``, ``'violet'`` and ``'brown'``.
    """

    def __init__(
        self,
        volume: float | tuple[float, float],
        sample_rate: int = 44100,
        duration: float = 1,
        color: str = "white",
    ):
        check_type(color, (str,), "color")
        check_value(color, _PSDS)
        self._color = color
        self._rng = np.random.default_rng()
        self.name = f"{color} noise"
        super().__init__(volume, sample_rate, duration)

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        noise_arr = Noise._noise_psd(self._rng, self._times.size, self._color)
        noise_arr /= np.max(np.abs(noise_arr))  # normalize
        self._signal = np.vstack((noise_arr, noise_arr)).T * self._volume / 100
        super()._set_signal()

    # --------------------------------------------------------------------
    @staticmethod
    def _noise_psd(rng: np.random.Generator, N: int, color: str):
        """Compute the noise signal 1D array."""
        white = rng.standard_normal(size=N)
        dft = np.fft.rfft(white)
        S = _PSDS[color](np.fft.rfftfreq(N))
        # nornalize to preserve the energy from the white noise
        S /= np.sqrt(np.mean(S**2))
        return np.fft.irfft(dft * S)

    # --------------------------------------------------------------------
    @property
    def color(self) -> str:
        """The noise color."""
        logger.debug("'self._color' is set to %s.", self._color)
        return self._color

    @color.setter
    def color(self, color: str):
        logger.debug("Setting 'color' to %s.", color)
        check_type(color, (str,), "color")
        check_value(color, _PSDS)
        self._color = color
        self._set_signal()
