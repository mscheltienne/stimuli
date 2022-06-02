"""Colored noise sound."""

from typing import Tuple, Union

import numpy as np

from .. import logger
from ..utils._checks import _check_type, _check_value
from ..utils._docs import copy_doc, fill_doc
from .base import BaseSound

_PSDS = {
    "white": lambda f: 1,
    "blue": lambda f: np.sqrt(f),
    "violet": lambda f: f,
    "pink": lambda f: 1 / np.where(f == 0, np.inf, np.sqrt(f)),
    "brown": lambda f: 1 / np.where(f == 0, np.inf, f),
}


@fill_doc
class Noise(BaseSound):  # noqa: E501
    """Colored noise stimulus.

    This class is based on the StackOverflow answer from Bob:
    https://stackoverflow.com/questions/67085963/generate-colors-of-noise-in-python/67127726#67127726

    Parameters
    ----------
    %(audio_volume)s
    %(audio_sample_rate)s
    %(audio_duration)s
    color : str
        The noise color. Available colors are: "white", "pink",
        "blue", "violet" and "brown".
    """

    def __init__(
        self,
        volume: Union[float, Tuple[float, float]],
        sample_rate: int = 44100,
        duration: float = 1,
        color: str = "white",
    ):
        _check_type(color, (str,), "color")
        _check_value(color, _PSDS)
        self._color = color
        self._rng = np.random.default_rng()
        self.name = f"{color} noise"
        super().__init__(volume, sample_rate, duration)

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        noise_arr = Noise._noise_psd(self._rng, self._times.size, self._color)
        noise_arr /= np.max(np.abs(noise_arr))  # normalize
        self._signal = np.vstack((noise_arr, noise_arr)).T * self._volume / 100

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
        _check_type(color, (str,), "color")
        _check_value(color, _PSDS)
        self._color = color
        self._set_signal()
