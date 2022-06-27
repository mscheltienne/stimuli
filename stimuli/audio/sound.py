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
        self._fname = BaseSound._check_file(fname, must_exists=True)

        sample_rate, original_signal = wavfile.read(self._fname)
        self._original_signal, volume = Sound._check_signal(original_signal)
        self._original_duration = self._original_signal.shape[0] / sample_rate

        self._tmin = None  # idx
        self._tmax = None  # idx
        super().__init__(volume, sample_rate, self._original_duration)
        self._original_times = self._times.copy()

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        assert self._original_signal.ndim == 2
        tmax = None if self._tmax is None else self._tmax + 1  # +1 for slice
        slc = (slice(self._tmin, tmax), slice(None))
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
        logger.debug("Cropping the signal between %s and %s.", tmin, tmax)
        self._tmin, self._tmax = Sound._check_tmin_tmax(
            tmin, tmax, self._original_times
        )
        logger.debug(
            "'tmin' corresponds to the idx %i and 'tmax' corresponds "
            "to the idx %i.",
            self._tmin,
            self._tmax,
        )
        self._duration = (
            self._original_times[self._tmax] - self._original_times[self._tmin]
        )
        # tmax + 1 for slice
        self._times = self._original_times[self._tmin : self._tmax + 1]
        self._set_signal()

    def reset(self) -> None:
        """Reset the signal to the original loaded signal."""
        logger.debug("Resetting the loaded sound.")
        self._tmin = None
        self._tmax = None
        self._duration = self._original_duration
        self._volume = np.max(np.abs(self._original_signal), axis=0) * 100
        self._set_times()
        self._set_signal()

    # --------------------------------------------------------------------
    @staticmethod
    def _check_signal(
        signal: NDArray[float],
    ) -> Tuple[NDArray[float], Tuple[float, float]]:
        """Check that the sound is either mono or stereo.

        Parameters
        ----------
        signal : array
            Raw signal loaded from the file.

        Returns
        -------
        signal : array
            Signal that has been normalized channel-wise.
        volume : tuple
            A 2-float tuple representing the (L, R) volume before channel-wise
            normalization. The volume is normalized between 0 and 100.

        Notes
        -----
        The volume is retrieved after normalizing the signal with the max of
        both channels, thus preserving the difference between both channels.
        The returned signal, stored in _original_signal, is normalized channel-
        wise. Thus, it does not correspond to the returned volume.

        However, the set signal, stored in _signal, is scaled by the volume in
        the _set_signal method.
        """
        assert signal.ndim in (1, 2)
        if signal.ndim == 2:
            assert signal.shape[1] in (1, 2)
            if signal.shape[1] == 1:
                signal = signal[:, 0]
        if signal.ndim == 1:
            signal = np.vstack((signal, signal)).T
        # normalize to retrieve the volume of boh channels
        max_ = np.max(np.abs(signal))
        if max_ == 0:
            logger.warning("The loaded sound has 2 empty channels.")
            return signal(0, 0)
        signal = signal / max_
        volume = tuple(np.max(np.abs(signal), axis=0) * 100)
        assert len(volume) == 2  # sanity-check
        assert any(elt == 100 for elt in volume)  # sanity-check
        # normalize both channels
        if all(elt != 0 for elt in volume):
            signal /= np.max(np.abs(signal), axis=0)
            np.nan_to_num(signal, copy=False, nan=0.0)  # sanity-check
        return signal, volume

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
            "The sampling rate property of a loaded sound can not be "
            "changed. Skipping."
        )

    @BaseSound.duration.setter
    def duration(self, duration: float):
        logger.warning(
            "The duration property of a loaded sound can not be "
            "changed. Use the method .crop(tmin, tmax) to trim "
            "a loaded sound. Skipping."
        )

    @property
    def fname(self) -> Path:
        """The sound's original file name."""
        logger.debug("'self._fname' is set to %s.", self._fname)
        return self._fname

    @property
    def tmin(self) -> float:
        """Left-edge of the signal crop [seconds]."""
        logger.debug("'self._tmin' is set to %s [AU].", self._tmin)
        if self._tmin is None:
            return self._times[0]
        return self._original_times[self._tmin]

    @property
    def tmax(self) -> float:
        """Right-edge of the signal crop [seconds]."""
        logger.debug("'self._tmax' is set to %s [AU].", self._tmax)
        if self._tmax is None:
            return self._times[-1]
        return self._original_times[self._tmax]
