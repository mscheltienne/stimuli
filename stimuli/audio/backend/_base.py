from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from ...time import BaseClock
from ...utils._checks import check_type
from ...utils.logs import warn

if TYPE_CHECKING:
    from numpy.typing import NDArray


class BaseBackend(ABC):
    """Base backend class for audio stimuli.

    Parameters
    ----------
    data : array of shape (n_frames, n_channels)
        The audio data to play provided as a 2 dimensional array of shape ``(n_frames,
        n_channels)``. The array layout must be C-contiguous. A one dimensional array of
        shape ``(n_frames,)`` is also accepted for mono audio.
    device : int
        Device identifier.
    sample_rate : int
        The sample rate of the audio data, which should match the sample rate of the
        output device.
    clock : BaseClock
        Clock object to use for time measurement. By default, the
        :class:`stimuli.time.Clock` class is used.
    """

    @abstractmethod
    def __init__(
        self,
        data: NDArray,
        device: int | None,
        sample_rate: int | None,
        clock: BaseClock,
    ) -> None:
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

        self._clock = clock()
        check_type(self._clock, (BaseClock,), "clock")

    @abstractmethod
    def play(self, when: float | None = None) -> None:
        """Play the audio data.

        Parameters
        ----------
        when : float | None
            The relative time in seconds when to start playing the audio data. For
            instance, ``0.2`` will start playing in 200 ms. If ``None``, the audio data
            is played as soon as possible.
        """

    @abstractmethod
    def stop(self) -> None:
        """Interrupt immediately the playback of the audio data."""
