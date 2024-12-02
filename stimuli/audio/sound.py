from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from scipy.io import wavfile

from ..time import Clock
from ..utils._checks import ensure_path
from ..utils._docs import copy_doc, fill_doc
from ..utils.logs import warn
from ._base import BaseSound

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    import numpy as np
    from numpy.typing import NDArray


_SUPPORTED: tuple[str, ...] = (".wav",)


@fill_doc
class Sound(BaseSound):
    """Auditory stimulus loaded from a file.

    Parameters
    ----------
    fname : str | Path
        Path to the supported audio file to load.
    %(audio_device)s
    %(audio_backend)s
    %(clock)s
    %(audio_kwargs)s
    """

    def __init__(
        self,
        fname: str | Path,
        device: int | None = None,
        *,
        backend: str = "sounddevice",
        clock: Callable = Clock,
        **kwargs,
    ) -> None:
        fname = ensure_path(fname, must_exist=True)
        if fname.suffix not in _SUPPORTED:
            raise ValueError(f"Unsupported file extension {fname.suffix}.")
        self._fname = fname
        sample_rate, original_signal = wavfile.read(self._fname)
        original_signal = original_signal.astype(np.float32)
        _check_signal(original_signal)
        volume = _extract_volume(original_signal)
        self._original_signal = _ensure_signal(original_signal)
        duration = self._original_signal.shape[0] / sample_rate
        super().__init__(
            volume,
            duration,
            sample_rate,
            device,
            self._original_signal.shape[1] if self._original_signal.ndim == 2 else 1,
            backend=backend,
            clock=clock,
            **kwargs,
        )

    def __repr__(self) -> str:
        """Representation of the object."""
        return f"<Sound @ {self.fname}>"

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        super()._set_signal(self._original_signal)

    @BaseSound.duration.setter
    def duration(self, duration: float):  # noqa: D102
        warn(
            "The duration property of a loaded sound can not be changed. Skipping.",
        )

    @property
    def fname(self) -> Path:
        """The sound's original file name.

        :type: :class:`~pathlib.Path`
        """
        return self._fname


def _check_signal(signal: NDArray[np.float32]) -> None:
    """Check the loaded signal is valid."""
    if signal.ndim not in (1, 2):
        raise ValueError(
            "The signal must be a 1D array of shape (n_samples,) or a 2D array of "
            "shape (n_samples, n_channels)."
        )


def _extract_volume(signal: NDArray[np.float32]) -> NDArray[np.float32]:
    """Extract the volume from the signal."""
    if signal.ndim == 1:
        signal = signal[:, np.newaxis]  # add a channel dimension
    # normalize to retrieve the volume per channel
    max_ = np.max(np.abs(signal))
    if max_ == 0:
        raise RuntimeError("The loaded sound is silent.")
    signal /= max_
    volume = np.max(np.abs(signal, dtype=np.float32), axis=0) * 100
    assert any(elt == 100 for elt in volume)  # sanity-check
    return volume


def _ensure_signal(signal: NDArray[np.float32]) -> NDArray[np.float32]:
    """Ensure the signal is valid."""
    if signal.ndim == 2 and signal.shape[1] == 1:
        signal = signal.squeeze()
    signal /= np.max(np.abs(signal, dtype=np.float32), axis=0)
    np.nan_to_num(signal, copy=False, nan=0.0)  # sanity-check
    return signal
