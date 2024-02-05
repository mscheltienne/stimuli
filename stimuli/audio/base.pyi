from abc import ABC, abstractmethod
from pathlib import Path

from _typeshed import Incomplete
from numpy.typing import NDArray

from ..utils._checks import check_type as check_type
from ..utils._checks import ensure_path as ensure_path
from ..utils._docs import fill_doc as fill_doc
from ..utils.logs import logger as logger

class BaseSound(ABC):
    """Base audio stimulus class.

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
    """

    _volume: Incomplete
    _sample_rate: Incomplete
    _duration: Incomplete
    _window: Incomplete

    @abstractmethod
    def __init__(
        self,
        volume: float | tuple[float, float],
        sample_rate: float = 44100,
        duration: float = 1,
    ): ...
    _times: Incomplete

    def _set_times(self) -> None:
        """Update the time array and the ._signal variable."""
    _signal: Incomplete

    @abstractmethod
    def _set_signal(self) -> None:
        """Set the signal in the numpy array ._signal played by sounddevice."""

    def copy(self, deep: bool = True):
        """Copy the sound.

        Parameters
        ----------
        deep : bool
            If ``True``, :func:`~copy.deepcopy` is used instead of
            :func:`~copy.copy`.
        """

    def play(self, blocking: bool = False) -> None:
        """Play the sound.

        This function creates and terminates an audio stream.

        Parameters
        ----------
        blocking : bool
            If True, playing the sounds blocks the interpreter.
        """

    def save(self, fname: str | Path, overwrite: bool = False) -> None:
        """Save a sound signal into a .wav file.

        The saving is handled by :func:`scipy.io.wavfile.write`.

        Parameters
        ----------
        fname : str | Path
            Path to the file where the sound signal is saved. The extension
            should be '.wav'.
        overwrite : bool
            If True, file with the same name are overwritten.
        """

    def stop(self) -> None:
        """Stop the sounds played on the active audio stream."""

    @staticmethod
    def _check_volume(volume: float | tuple[float, float]) -> NDArray[float]:
        """Check that the volume provided by the user is valid."""

    @staticmethod
    def _check_sample_rate(sample_rate: float) -> float:
        """Check if the sample rate is a positive number."""

    @staticmethod
    def _check_duration(duration: float) -> float:
        """Check if the duration is positive."""

    @property
    def volume(self) -> float | tuple[float, float]:
        """Sound's volume(s) [AU]."""

    @volume.setter
    def volume(self, volume: float | tuple[float, float]):
        """Sound's volume(s) [AU]."""

    @property
    def sample_rate(self) -> int:
        """Sound's sampling rate [Hz]."""

    @sample_rate.setter
    def sample_rate(self, sample_rate: int):
        """Sound's sampling rate [Hz]."""

    @property
    def duration(self) -> float:
        """Sound's duration [seconds]."""

    @duration.setter
    def duration(self, duration: float):
        """Sound's duration [seconds]."""

    @property
    def signal(self) -> NDArray[float]:
        """Sound's signal."""

    @property
    def times(self) -> NDArray[float]:
        """Times array."""

    @property
    def window(self) -> NDArray[float] | None:
        """Window applied to the signal."""

    @window.setter
    def window(self, window: NDArray[float] | None):
        """Window applied to the signal."""

    @property
    def n_samples(self) -> int:
        """Number of samples."""
