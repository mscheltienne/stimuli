"""Sound loaded from a file."""

from pathlib import Path
from typing import Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray
from scipy.io import wavfile

from .. import logger
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

        sample_rate, original_signal = wavfile.read(self._fname)
        self._original_signal, volume = Sound._check_signal(original_signal)
        self._original_duration = self._original_signal.shape[0] / sample_rate

        self._tmin = None  # idx
        self._tmax = None  # idx
        super().__init__(volume, sample_rate, self._original_duration)

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        assert self._signal.ndim == 2
        slc = (slice(self._tmin, self._tmax), slice(None))
        self._signal = self._original_signal[slc] * self._volume / 100

    def crop(
        self, tmin: Optional[float] = None, tmax: Optional[float] = None
    ) -> None:
        """Crop the sound between tmin and tmax.

        Parameters
        ----------
        tmin : float | None
            Left-edge of the crop. If None, the beginning of the sound.
        tmax : float | None
            Right-edge of the crop. If None, the end of the sound.

        Notes
        -----
        The time-based selection selects the samples in the closed interval
        [tmin, tmax].
        """
        self._tmin, self._tmax = Sound._check_tmin_tmax(
            tmin, tmax, self._time_arr
        )
        self._time_arr = self._time_arr[self._tmin, self._tmax]
        self._duration = self._tmax - self._tmin
        self._set_signal()

    def reset(self) -> None:
        """Reset the signal to the original loaded signal."""
        self._tmin = None
        self._tmax = None
        self._duration = self._original_duration
        self._volume = np.array([100.0, 100.0])
        self._set_time_arr()
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

    @staticmethod
    def _check_tmin_tmax(
        tmin: Optional[float], tmax: Optional[float], times: NDArray[float]
    ) -> Tuple[int, int]:
        """Check tmin/tmax and convert to idx."""
        _check_type(tmin, ("numeric", None), "tmin")
        _check_type(tmax, ("numeric", None), "tmax")
        tmin = 0 if tmin is None else tmin
        tmin = tmin if np.isfinite(tmin) else 0
        tmax = times[-1] if tmax is None else tmax
        tmax = tmax if np.isfinite(tmax) else times[-1]
        assert 0 <= tmin
        assert tmax <= times[-1]
        idx = np.where((tmin <= times) & (times <= tmax))[0]
        return idx[0], idx[-1]

    # --------------------------------------------------------------------
    @BaseSound.sample_rate.setter
    def sample_rate(self, sample_rate: int):
        logger.warning(
            "The sampling rate of a loaded sound can not be "
            "changed. Skipping."
        )

    @BaseSound.duration.setter
    def duration(self, duration: float):
        logger.warning(
            "The duration property of a loaded sound can not be "
            "changed. Use the method .crop(tmin, tmax) to trim "
            "a loaded sound."
        )

    @property
    def fname(self) -> Path:
        """The sound's original file name."""
        return self._fname

    @property
    def tmin(self) -> float:
        """Left-edge of the signal crop [seconds]."""
        if self._tmin is None:
            logger.debug("'self._tmin' is set to None. Returning 0 seconds.")
            return 0.0
        tmin = self._tmin / self._sample_rate
        logger.debug(
            "'self._tmin' is set to %i. Returning %.2f seconds.",
            self._tmin,
            tmin,
        )
        return tmin

    @tmin.setter
    def tmin(self, tmin):
        self.crop(tmin=tmin, tmax=self.tmax)

    @property
    def tmax(self) -> float:
        """Right-edge of the signal crop [seconds]."""
        if self._tmax is None:
            tmax = self._time_arr[-1]
            logger.debug(
                "'self._tmax' is set to None. Returning %.2f seconds.", tmax
            )
            return tmax
        tmax = self._tmax / self._sample_rate
        logger.debug(
            "'self._tmax' is set to %i. Returning %.2f seconds.",
            self._tmax,
            tmax,
        )
        return tmax

    @tmax.setter
    def tmax(self, tmax):
        self.crop(tmin=self.tmin, tmax=tmax)
