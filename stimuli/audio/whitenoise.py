"""White Noise sound."""

from typing import Tuple, Union

import numpy as np

from ..utils._docs import copy_doc, fill_doc
from ._sound import _Sound


@fill_doc
class WhiteNoise(_Sound):
    """White noise stimuli.

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

    @copy_doc(_Sound._set_signal)
    def _set_signal(self) -> None:
        # mean: 0, sigma: 0.33
        wn_arr = self._rng.normal(loc=0, scale=1 / 3, size=self._time_arr.size)

        self._signal[:, 0] = wn_arr * 0.1 * self._volume[0] / 100
        if len(self._volume) == 2:
            self._signal[:, 1] = wn_arr * 0.1 * self._volume[1] / 100
