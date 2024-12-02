from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from ...time import BaseClock
from ...utils._checks import check_type
from ...utils._docs import fill_doc
from ...utils.logs import warn

if TYPE_CHECKING:
    from collections.abc import Callable

    from numpy.typing import NDArray


@fill_doc
class BaseBackend(ABC):
    """Base backend class for audio stimuli.

    Parameters
    ----------
    device : int | None
        Device identifier. If None, the default output device is used.
    sample_rate : int
        The sample rate of the audio data, which should match the sample rate of the
        output device. If None, the default sample rate of the device is used.
    %(clock)s
    """

    @abstractmethod
    def __init__(
        self,
        device: int | None,
        sample_rate: int | None,
        clock: Callable,
    ) -> None:
        check_type(clock, ("callable",), "clock")
        self._clock = clock()
        check_type(self._clock, (BaseClock,), "clock")

    def __del__(self) -> None:
        """Make sure that we kill the stream during deletion."""
        self.close()  # no-op if already closed

    @abstractmethod
    def close(self) -> None:
        """Close the backend and release the resources."""

    @abstractmethod
    def initialize(self, data: NDArray) -> None:
        """Initialize the backend with audio data.

        Parameters
        ----------
        data : :class:`~numpy.ndarray` of shape (n_frames, n_channels)
            The audio data to play provided as a 2 dimensional array of shape
            ``(n_frames, n_channels)``. The array layout must be C-contiguous. A one
            dimensional :class:`~numpy.ndarray` of shape ``(n_frames,)`` is also
            accepted for mono audio.
        """
        check_type(data, (np.ndarray,), "data")
        if data.ndim not in (1, 2):
            raise ValueError(
                "The data array must be 1D or 2D of shape (n_frames, n_channels). "
                f"The provided array has {data.ndim} dimensions."
            )
        if not data.flags["C_CONTIGUOUS"]:
            warn(
                "The data array provided to the 'SoundSD' backend is not C-contiguous."
            )
            data = np.ascontiguousarray(data)
        self._data = data if data.ndim == 2 else data[:, np.newaxis]
        self._duration = self._data.shape[0] / self._sample_rate

    @abstractmethod
    def play(self, when: float | None = None, *, blocking: bool = False) -> None:
        """Play the audio data.

        Parameters
        ----------
        when : float | None
            The relative time in seconds when to start playing the audio data. For
            instance, ``0.2`` will start playing in 200 ms. If ``None``, the audio data
            is played as soon as possible. A duration superior to the device latency is
            recommended.
        blocking : bool
            If True, the function blocks until the audio playback is finished.
        """
        self._check_initialized()
        if when is not None:  # quick input validation
            assert 0 < when, "The 'when' parameter must be a positive float."

    @abstractmethod
    def stop(self) -> None:
        """Interrupt immediately the playback of the audio data."""
        self._check_initialized()

    def _check_initialized(self) -> None:
        """Check if the backend is initialized with audio data."""
        if not hasattr(self, "_data"):
            raise RuntimeError("The backend is not initialized with sound data.")

    @property
    def clock(self) -> BaseClock:
        """The clock object used for time measurement."""
        return self._clock

    @property
    def duration(self) -> float:
        """The duration of the audio data, in seconds."""
        return self._duration

    @property
    def sample_rate(self) -> int:
        """The sample rate of the audio data."""
        return self._sample_rate
