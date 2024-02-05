"""Base class for sound delivery."""

import copy
from abc import ABC, abstractmethod
from os import makedirs
from pathlib import Path

import numpy as np
import sounddevice as sd
from numpy.typing import NDArray
from scipy.io import wavfile

from ..utils._checks import check_type, ensure_path
from ..utils._docs import fill_doc
from ..utils.logs import logger


@fill_doc
class BaseSound(ABC):
    """Base audio stimulus class.

    Parameters
    ----------
    %(audio_volume)s
    %(audio_sample_rate)s
    %(audio_duration)s
    """

    @abstractmethod
    def __init__(
        self,
        volume: float | tuple[float, float],
        sample_rate: float = 44100,
        duration: float = 1,
    ):
        self._volume = BaseSound._check_volume(volume)
        self._sample_rate = BaseSound._check_sample_rate(sample_rate)
        self._duration = BaseSound._check_duration(duration)
        self._window = None  # rectangular window applied by default
        self._set_times()
        self._set_signal()

    def _set_times(self) -> None:
        """Update the time array and the ._signal variable."""
        logger.debug(
            "Setting the 'times' array with the duration %.2f "
            "[seconds] and the sampling rate %.1f [Hz].",
            self._duration,
            self._sample_rate,
        )
        self._times = np.linspace(
            0,
            self._duration,
            int(self._duration * self._sample_rate),
            endpoint=True,
        )

    @abstractmethod
    def _set_signal(self) -> None:
        """Set the signal in the numpy array ._signal played by sounddevice."""
        # [:, 0] for left and [:, 1] for right
        if self._window is not None:
            self._signal = np.multiply(self._window, self._signal.T).T
        self._signal = self._signal.astype(np.float32)

    # --------------------------------------------------------------------
    def copy(self, deep: bool = True):
        """Copy the sound.

        Parameters
        ----------
        deep : bool
            If ``True``, :func:`~copy.deepcopy` is used instead of
            :func:`~copy.copy`.
        """
        check_type(deep, (bool,), "deep")
        if deep:
            return copy.deepcopy(self)
        else:
            return copy.copy(self)

    def play(self, blocking: bool = False) -> None:
        """Play the sound.

        This function creates and terminates an audio stream.

        Parameters
        ----------
        blocking : bool
            If True, playing the sounds blocks the interpreter.
        """
        check_type(blocking, (bool,), "blocking")
        logger.debug("Play requested with blocking set to %s.", blocking)
        sd.play(
            self._signal,
            samplerate=self._sample_rate,
            mapping=[1, 2],
            blocking=blocking,
        )

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
        fname = ensure_path(fname, must_exist=False)
        assert fname.suffix in (".wav",)
        if overwrite is False and fname.exists():
            raise RuntimeError(
                "The file %s already exist. Set argument "
                "'overwrite' to True if you want to overwrite "
                "the existing file.",
                fname,
            )
        if not fname.parent.exists():
            makedirs(fname.parent)
        logger.debug(
            "Writing sound to file %s with sampling frequency %.1f [Hz].",
            fname,
            self._sample_rate,
        )
        wavfile.write(fname, self._sample_rate, self._signal)

    def stop(self) -> None:
        """Stop the sounds played on the active audio stream."""
        logger.debug("Stop requested.")
        sd.stop()

    # --------------------------------------------------------------------
    @staticmethod
    def _check_volume(volume: float | tuple[float, float]) -> NDArray[float]:
        """Check that the volume provided by the user is valid."""
        check_type(volume, ("numeric", tuple), "volume")
        if not isinstance(volume, tuple):
            volume = (volume, volume)
        assert len(volume) in (1, 2)
        for vol in volume:
            check_type(vol, ("numeric",))
        assert all(0 <= v <= 100 for v in volume)
        return np.array(volume)

    @staticmethod
    def _check_sample_rate(sample_rate: float) -> float:
        """Check if the sample rate is a positive number."""
        check_type(sample_rate, ("numeric",), "sample_rate")
        assert 0 < sample_rate
        return sample_rate

    @staticmethod
    def _check_duration(duration: float) -> float:
        """Check if the duration is positive."""
        check_type(duration, ("numeric",), item_name="duration")
        assert 0 < duration
        return duration

    # --------------------------------------------------------------------
    @property
    def volume(self) -> float | tuple[float, float]:
        """Sound's volume(s) [AU]."""
        logger.debug("'self._volume' is set to %s [AU].", self._volume)
        volume = tuple(self._volume)
        if volume[0] == volume[1]:
            volume = volume[0]
        return volume

    @volume.setter
    def volume(self, volume: float | tuple[float, float]):
        logger.debug("Setting 'volume' to %s [AU].", volume)
        self._volume = BaseSound._check_volume(volume)
        self._set_signal()

    @property
    def sample_rate(self) -> int:
        """Sound's sampling rate [Hz]."""
        logger.debug("'self._sample_rate' is set to %.1f [Hz].", self._sample_rate)
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, sample_rate: int):
        logger.debug("Setting 'sample_rate' to %.1f [Hz].", sample_rate)
        self._sample_rate = BaseSound._check_sample_rate(sample_rate)
        self._set_times()
        self._set_signal()

    @property
    def duration(self) -> float:
        """Sound's duration [seconds]."""
        logger.debug("'self._duration' is set to %.2f [seconds].", self._duration)
        return self._duration

    @duration.setter
    def duration(self, duration: float):
        logger.debug("Setting 'duration' to %.2f [seconds].", duration)
        self._duration = BaseSound._check_duration(duration)
        self._set_times()
        self._set_signal()

    @property
    def signal(self) -> NDArray[float]:
        """Sound's signal."""
        return self._signal

    @property
    def times(self) -> NDArray[float]:
        """Times array."""
        return self._times

    @property
    def window(self) -> NDArray[float] | None:
        """Window applied to the signal."""
        return self._window

    @window.setter
    def window(self, window: NDArray[float] | None):
        check_type(window, (None, np.ndarray), "window")
        if window is not None:
            assert window.ndim == 1
            assert window.size == self._times.size
        self._window = window
        self._set_signal()

    @property
    def n_samples(self) -> int:
        """Number of samples."""
        return self._times.size
