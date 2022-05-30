"""Sound loaded from a file."""

from pathlib import Path
from typing import Tuple, Union

from numpy.typing import NDArray
from scipy.io import wavfile
from scipy.signal import resample

from ..utils._checks import _check_type
from ..utils._docs import copy_doc
from ._sound import _Sound


class Sound(_Sound):
    """Sound loaded from file.

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
        self._original_signal = Sound._check_signal(_original_signal)
        self._original_duration = Sound._compute_duration(
            self._original_signal, self._original_sample_rate
        )

        _volume = Sound._compute_volume(self._original_signal)
        self._trim_samples = None
        super().__init__(
            _volume, self._original_sample_rate, self._original_duration
        )

    @copy_doc(_Sound._set_signal)
    def _set_signal(self) -> None:
        assert len(self._signal.shape) in (1, 2)
        slc = (
            slice(None, self._trim_samples)
            if len(self._original_signal.shape) == 1
            else (slice(None, self._trim_samples), slice(None))
        )
        self._signal = self._original_signal[slc]

    def trim(self, duration: float) -> None:
        """Trim the original sound to the new duration."""
        if Sound._valid_trim_duration(duration, self._original_duration):
            self._duration = _Sound._check_duration(duration)
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
    def _check_signal(signal: NDArray[float]) -> NDArray[float]:
        """Check that the sound is either mono or stereo."""
        assert signal.ndim in (1, 2)
        if signal.ndim == 2:
            assert signal.shape[1] in (1, 2)
            if signal.shape[1] == 1:
                signal = signal[:, 0]
        return signal

    @staticmethod
    def _compute_duration(signal: NDArray[float], sample_rate: int) -> float:
        """Compute the sounds duration."""
        return signal.shape[0] / sample_rate

    @staticmethod
    def _compute_volume(signal) -> Tuple[float, ...]:
        """Volume modifications is not supported for loaded sounds.

        Returns [1] * number of channels.
        """
        return tuple([1.0] * len(signal.shape))

    @staticmethod
    def _valid_trim_duration(
        trim_duration: float, sound_duration: float
    ) -> bool:
        """Return True if trim_duration is smaller than sound_duration."""
        if sound_duration <= trim_duration:
            return False
        return True

    # --------------------------------------------------------------------
    @_Sound.volume.setter
    def volume(self, volume: Union[float, Tuple[float, float]]):
        pass

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
