from pathlib import Path

from _typeshed import Incomplete
from numpy.typing import NDArray

from ..utils._checks import check_type as check_type
from ..utils._checks import ensure_path as ensure_path
from ..utils._docs import copy_doc as copy_doc
from ..utils.logs import logger as logger
from .base import BaseSound as BaseSound

class Sound(BaseSound):
    """Auditory stimulus loaded from a file.

    Parameters
    ----------
    fname : str | Path
        Path to the supported audio file to load.
    """

    _fname: Incomplete
    _original_duration: Incomplete
    _tmin: Incomplete
    _tmax: Incomplete
    _original_times: Incomplete

    def __init__(self, fname: str | Path) -> None: ...
    _signal: Incomplete

    def _set_signal(self) -> None:
        """Set the signal in the numpy array ._signal played by sounddevice."""
    _duration: Incomplete
    _times: Incomplete

    def crop(self, tmin: float | None = None, tmax: float | None = None) -> None:
        """Crop the sound between ``tmin`` and ``tmax``.

        Parameters
        ----------
        tmin : float | None
            Left-edge of the crop. If None, the beginning of the sound.
        tmax : float | None
            Right-edge of the crop. If None, the end of the sound.

        Notes
        -----
        The time-based selection selects the samples in the closed interval
        ``[tmin, tmax]``.
        """
    _volume: Incomplete

    def reset(self) -> None:
        """Reset the signal to the original loaded signal."""

    @staticmethod
    def _check_signal(
        signal: NDArray[float],
    ) -> tuple[NDArray[float], tuple[float, float]]:
        """Check that the sound is either mono or stereo.

        Parameters
        ----------
        signal : array
            Raw signal loaded from the file.

        Returns
        -------
        signal : array
            Signal that has been normalized channel-wise and converted to
            float32.
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

    @staticmethod
    def _check_tmin_tmax(
        tmin: float | None, tmax: float | None, times: NDArray[float]
    ) -> tuple[int, int]:
        """Check tmin/tmax and convert to idx."""

    @BaseSound.sample_rate.setter
    def sample_rate(self, sample_rate: int):
        """Sound's sampling rate [Hz]."""

    @BaseSound.duration.setter
    def duration(self, duration: float):
        """Sound's duration [seconds]."""

    @property
    def fname(self) -> Path:
        """The sound's original file name."""

    @property
    def tmin(self) -> float:
        """Left-edge of the signal crop [seconds]."""

    @property
    def tmax(self) -> float:
        """Right-edge of the signal crop [seconds]."""
