from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..time import Clock
from ..utils._checks import check_type, check_value
from ..utils._docs import copy_doc, fill_doc
from ..utils.logs import logger
from ._base import BaseSound

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


@fill_doc
class SoundAM(BaseSound):
    """Amplitude modulated sound.

    This sound is composed of a carrier frequency ``fc`` which is amplitude modulated at
    ``fm``.

    Parameters
    ----------
    frequency_carrier : float
        Carrier frequency in Hz.
    frequency_modulation : float
        Modulation frequency in Hz.
    method : ``'conventional'`` | ``'dsbsc'``
        ``'conventional'`` is also called classical AM, the equation used is::

                signal = (1 - M(t)) * cos(2*pi*fc*t)
                M(t) = cos(2*pi*fm*t)

        ``'dsbsc'`` is also called double side band suppressed carrier, the equation
        used is::

                signal = M(t)*cos(2*pi*fc*t)
                M(t) = sin(2*pi*fm*t)
    %(audio_volume)s
    %(audio_duration)s
    %(audio_sample_rate)s
    %(audio_device)s
    %(audio_n_channels)s
    %(audio_backend)s
    %(clock)s
    %(audio_kwargs)s
    """

    def __init__(
        self,
        frequency_carrier: float,
        frequency_modulation: float,
        method: str,
        volume: float | Sequence[float],
        duration: float,
        sample_rate: int | None = None,
        device: int | None = None,
        n_channels: int = 1,
        *,
        backend: str = "sounddevice",
        clock: Callable = Clock,
        **kwargs,
    ) -> None:
        _check_frequency(frequency_carrier, "carrier")
        self._frequency_carrier = frequency_carrier
        _check_frequency(frequency_modulation, "modulation")
        self._frequency_modulation = frequency_modulation
        check_type(method, (str,), "method")
        method = method.lower().strip()
        check_value(method, ("conventional", "dsbsc"), "AM method")
        self._method = method
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
        return (
            f"<{self._method}-AM sound @ {self._frequency_carrier:.2f} % "
            f"{self._frequency_modulation:.2f} Hz - {self.duration:.2f} s>"
        )

    @copy_doc(BaseSound._set_signal)
    def _set_signal(self) -> None:
        if self._method == "conventional":
            amplitude = 1 - np.cos(2 * np.pi * self._frequency_modulation * self._times)
            signal = amplitude * np.cos(
                2 * np.pi * self._frequency_carrier * self._times
            )

        elif self._method == "dsbsc":
            amplitude = np.sin(2 * np.pi * self._frequency_modulation * self._times)
            signal = amplitude * np.sin(
                2 * np.pi * self._frequency_carrier * self._times
            )
        signal /= np.max(np.abs(signal))  # normalize
        signal = np.vstack([signal] * self._n_channels).T
        super()._set_signal(signal)

    @property
    def frequency_carrier(self) -> float:
        """Sound's carrier frequency in Hz.

        :type: :class:`float`
        """
        return self._frequency_carrier

    @frequency_carrier.setter
    def frequency_carrier(self, frequency_carrier: float) -> None:
        logger.debug("Setting 'frequency_carrier' to %.2f [Hz].", frequency_carrier)
        _check_frequency(frequency_carrier, "carrier")
        self._frequency_carrier = frequency_carrier
        self._set_signal()

    @property
    def frequency_modulation(self) -> float:
        """Sound's modulation frequency in Hz.

        :type: :class:`float`
        """
        return self._frequency_modulation

    @frequency_modulation.setter
    def frequency_modulation(self, frequency_modulation: float) -> None:
        logger.debug(
            "Setting 'frequency_modulation' to %.2f [Hz].", frequency_modulation
        )
        _check_frequency(frequency_modulation, "modulation")
        self._frequency_modulation = frequency_modulation
        self._set_signal()

    @property
    def method(self) -> str:
        """The amplitude modulation method.

        :type: :class:`str`
        """
        return self._method

    @method.setter
    def method(self, method: str) -> None:
        logger.debug("Setting 'method' to %s.", method)
        check_type(method, (str,), "method")
        method = method.lower().strip()
        check_value(method, ("conventional", "dsbsc"), "AM method")
        self._method = method
        self._set_signal()


def _check_frequency(frequency: float, ftype: str) -> None:
    """Check that the given frequency is valid."""
    check_type(frequency, ("numeric",), item_name=f"frequency_{ftype}")
    if frequency <= 0:
        raise ValueError(
            f"The {ftype} frequency must be a strictly positive number. Provided "
            f"'{frequency}' is invalid."
        )
