"""Sound loaded from a file."""

from pathlib import Path
from typing import Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray
from scipy.io import wavfile
from scipy.signal import resample

from ..utils._checks import _check_type
from ..utils._docs import copy_doc
from .base import BaseSound


class Sound(BaseSound):
    """Auditory stimulus loaded from a file.

    Parameters
    ----------
    fname : str | Path
        Path to the supported audio file to load.
    """

    def __init__(self, fname: Union[str, Path]):
        self._fname = Sound._check_file(fname)

        original_sample_rate, original_signal = wavfile.read(self._fname)
        self._original_sample_rate = BaseSound._check_sample_rate(
            original_sample_rate
        )
        self._original_signal, volume = Sound._check_signal(original_signal)
        self._original_duration = (
            self._original_signal.shape[0] / self._original_sample_rate
        )

        self._trim_samples = None
        super().__init__(
            volume, self._original_sample_rate, self._original_duration
        )

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        assert self._signal.ndim == 2
        slc = (slice(None, self._trim_samples), slice(None))
        self._signal = self._original_signal[slc] * self._volume / 100

    def crop(self, tmin: Optional[float] = None, tmax: Optional[float] = None) -> None:
        """Crop the sound between tmin and tmax.

        Parameters
        ----------
        tmin : float | None
            Left-edge of the crop. If None, the beginning of the sound.
        tmax : float | None
            Right-edge of the crop. If None, the end of the sound.
        """
        tmin, tmax = Sound._check_tmin_tmax(tmin, tmax, self._original_duration)

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

    @staticmethod
    def _check_tmin_tmax(tmin: Optional[float], tmax: Optional[float], duration: float) -> Tuple[int, int]:
        """Check tmin/tmax and convert to idx."""
        pass

    # --------------------------------------------------------------------
    @BaseSound.sample_rate.setter
    def sample_rate(self, sample_rate: int):
        self.resample(sample_rate)

    @BaseSound.duration.setter
    def duration(self, duration: float):
        self.trim(duration)

    @property
    def fname(self) -> Path:
        """The sound's original file name."""
        return self._fname
