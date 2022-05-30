"""Sound loaded from a file."""

from pathlib import Path
from typing import Tuple, Union

import numpy as np
from numpy.typing import NDArray
from scipy.io import wavfile
from scipy.signal import resample

from ..utils._checks import _check_type
from ..utils._docs import copy_doc
from ._sound import _Sound


class Sound(_Sound):
    """Auditory stimulus loaded from a file.

    Parameters
    ----------
    fname : str | Path
        Path to the supported audio file to load.
    """

    def __init__(self, fname: Union[str, Path]):
        self._fname = Sound._check_file(fname)

        _original_sample_rate, _original_signal = wavfile.read(self._fname)
        self._original_sample_rate = _Sound._check_sample_rate(
            _original_sample_rate
        )
        self._original_signal, volume = Sound._check_signal(_original_signal)
        self._original_duration = (
            self._original_signal.shape[0] / self._original_sample_rate
        )

        self._trim_samples = None
        super().__init__(
            volume, self._original_sample_rate, self._original_duration
        )

    @copy_doc(_Sound._set_signal)
    def _set_signal(self) -> None:
        assert self._signal.ndim == 2
        slc = (slice(None, self._trim_samples), slice(None))
        self._signal = self._original_signal[slc] * self._volume / 100

    # TODO: Replace with a crop method with tmin and tmax
    def trim(self, duration: float) -> None:
        """Trim the original sound to the new duration."""
        duration = _Sound._check_duration(duration)
        if self._original_duration <= duration:
            return None
        self._duration = duration
        self._trim_samples = int(self._duration * self._sample_rate)
        self._set_signal()

    def resample(self, sample_rate: int) -> None:
        """Resample the current sound to the new sampling rate."""
        self._sample_rate = _Sound._check_sample_rate(sample_rate)
        self._signal = resample(
            self._signal, int(self._sample_rate * self._duration), axis=0
        )

    def reset(self) -> None:
        """Reset the current sound to the original loaded sound."""
        self._duration = self._original_duration
        self._trim_samples = None
        self._sample_rate = self._original_sample_rate
        self._set_signal()

    # --------------------------------------------------------------------
    @staticmethod
    def _check_file(fname: Union[str, Path]) -> Path:
        """Check if the file is supported and exists."""
        SUPPORTED = ".wav"

        _check_type(fname, ("path-like",))
        fname = Path(fname)
        assert fname.suffix in SUPPORTED and fname.exists()
        return fname

    @staticmethod
    def _check_signal(
        signal: NDArray[float],
    ) -> Tuple[NDArray[float], Tuple[float, float]]:
        """Check that the sound is either mono or stereo."""
        assert signal.ndim in (1, 2)
        if signal.ndim == 2:
            assert signal.shape[1] in (1, 2)
            if signal.shape[1] == 1:
                signal = signal[:, 0]
        if signal.ndin == 1:
            signal = np.vstack((signal, signal)).T
        # normalize signal
        max_ = np.max(np.abs(signal))
        signal /= max_
        return signal, (100, 100)

    # --------------------------------------------------------------------
    @_Sound.sample_rate.setter
    def sample_rate(self, sample_rate: int):
        self.resample(sample_rate)

    @_Sound.duration.setter
    def duration(self, duration: float):
        self.trim(duration)

    @property
    def fname(self) -> Path:
        """The sound's original file name."""
        return self._fname
