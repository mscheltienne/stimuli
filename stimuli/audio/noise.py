from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..time import Clock
from ..utils._checks import check_type, check_value
from ..utils._docs import copy_doc
from ..utils.logs import logger
from ._base import BaseSound

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from ..time import BaseClock


_PSDS: dict[str, Callable] = {
    "white": lambda f: 1,
    "blue": lambda f: np.sqrt(f),
    "violet": lambda f: f,
    "pink": lambda f: 1 / np.where(f == 0, np.inf, np.sqrt(f)),
    "brown": lambda f: 1 / np.where(f == 0, np.inf, f),
}


class Noise(BaseSound):
    """Colored noise stimulus.

    Parameters
    ----------
    color : ``'white'`` | ``'pink'`` | ``'blue'`` | ``'violet'`` | ``'brown'``
        The name of the noise color.
    """

    def __init__(
        self,
        color: str,
        volume: float | Sequence[float],
        duration: float,
        sample_rate: int | None = None,
        device: int | None = None,
        n_channels: int = 1,
        *,
        backend: str = "sounddevice",
        clock: BaseClock = Clock,
        **kwargs,
    ) -> None:
        check_type(color, (str,), "color")
        color = color.lower().strip()
        check_value(color, _PSDS, "color")
        self._color = color
        self._rng = np.random.default_rng()
        super().__init__(
            volume,
            duration,
            sample_rate,
            device,
            n_channels,
            backend=backend,
            clock=clock,
            **kwargs,
        )

    def __repr__(self) -> str:
        """Representation of the object."""
        return f"<{self._color.capitalize()} noise @ {self.duration:.2f} s>"

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        white = self._rng.standard_normal(size=self._times.size, dtype=np.float32)
        dft = np.fft.rfft(white)
        S = _PSDS[self._color](np.fft.rfftfreq(self._times.size))
        # nornalize to preserve the energy from the white noise
        S /= np.sqrt(np.mean(S**2))
        signal = np.fft.irfft(dft * S)
        signal /= np.max(np.abs(signal))  # normalize
        super()._set_signal(signal)

    @property
    def color(self) -> str:
        """The color of the noise."""
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        logger.debug("Setting 'color' to %s.", color)
        check_type(color, (str,), "color")
        color = color.lower().strip()
        check_value(color, _PSDS, "color")
        self._color = color
        self._set_signal()
