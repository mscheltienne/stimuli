"""White Noise sound."""

from typing import Tuple, Union

import numpy as np

from ..utils._docs import copy_doc, fill_doc
from .base import BaseSound


@fill_doc
class WhiteNoise(BaseSound):
    """White noise stimulus.

    Parameters
    ----------
    %(audio_volume)s
    %(audio_sample_rate)s
    %(audio_duration)s
    """

    def __init__(
        self,
        volume: Union[float, Tuple[float, float]],
        sample_rate: int = 44100,
        duration: float = 1,
    ):
        self._rng = np.random.default_rng()
        self.name = "whitenoise"
        super().__init__(volume, sample_rate, duration)

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        # mean: 0, sigma: 0.33
        wn_arr = self._rng.normal(loc=0, scale=1 / 3, size=self._time_arr.size)
        self._signal = np.vstack((wn_arr, wn_arr)).T * self._volume / 100
