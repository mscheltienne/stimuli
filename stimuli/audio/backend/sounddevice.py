from __future__ import annotations

from typing import TYPE_CHECKING

import sounddevice as sd

from ...time import Clock, sleep
from ...utils._checks import check_value, ensure_int
from ...utils._docs import copy_doc, fill_doc
from ...utils.logs import logger, warn
from ._base import BaseBackend

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from ...time import BaseClock


@fill_doc
class SoundSD(BaseBackend):
    """Sounddevice backend for audio playback.

    Parameters
    ----------
    device : int
        Device index of the output device as provided by
        :func:`sounddevice.query_devices()`. If None, the default output device is used.
    sample_rate : int
        The sample rate of the audio data, which should match the sample rate of the
        output device. If None, the default sample rate of the device is used.
    %(clock)s
    """

    def __init__(
        self,
        device: int | None,
        sample_rate: int | None,
        *,
        clock: BaseClock = Clock,
    ) -> None:
        super().__init__(sample_rate, device, clock)
        self._device = _ensure_device(device)
        self._sample_rate = _ensure_sample_rate(sample_rate, self._device)
        if self._sample_rate != self._device["default_samplerate"]:
            warn(
                "The sample rate provided to the 'SoundSD' backend "
                f"({self._sample_rate}) differs from the default sample rate of the "
                f"device ({self._device['default_samplerate']})."
            )

    @copy_doc(BaseBackend.close)
    def close(self) -> None:
        if hasattr(self, "_target_time") and self._target_time is not None:
            warn("The audio playback was on-going.")
        if hasattr(self, "_stream"):
            self._stream.stop()
            self._stream.close()

    @copy_doc(BaseBackend.initialize)
    def initialize(self, data: NDArray, block_size: int = 32) -> None:
        # fmt: off
        """block_size : int
            The number of frames passed to the stream callback function, or the
            preferred block granularity for a blocking read/write stream. The special
            value ``blocksize=0`` may be used to request that the stream callback will
            receive an optimal (and possibly varying) number of frames based on host
            requirements and the requested latency settings.
        """
        # fmt: on
        super().initialize(data)
        if (
            self._data.ndim == 2
            and self._device["max_output_channels"] < self._data.shape[1]
        ):
            raise ValueError(
                f"Device '{self._device['index']}: {self._device['name']}' does not "
                f"support the number of output channels ({self._data.shape[1]})."
            )
        block_size = _ensure_block_size(block_size)
        # convert the data array to a supported byte representation
        check_value(self._data.dtype.name, sd._sampleformats, "dtype")
        self._bytes_per_frame = self._data.shape[1] * self._data.itemsize
        n_channels = self._data.shape[1]
        dtype = self._data.dtype
        self._data = self._data.tobytes(order="C")
        # store callback variables
        self._current_frame = 0
        self._target_time = None
        # create and open the output stream
        self._stream = sd.RawOutputStream(
            blocksize=block_size,
            callback=self._callback,
            channels=n_channels,
            device=self._device["index"],
            dtype=dtype,
            latency="low",
            samplerate=self._sample_rate,
            prime_output_buffers_using_stream_callback=True,
        )
        self._stream.start()

    def _callback(self, outdata, frames, time_info, status):
        """Callback audio function."""  # noqa: D401
        if self._target_time is None:
            outdata[:] = b"\x00" * frames * self._bytes_per_frame
            return
        delta_ns = int((time_info.outputBufferDacTime - time_info.currentTime) * 1e9)
        if self._clock.get_time_ns() + delta_ns < self._target_time:
            outdata[:] = b"\x00" * frames * self._bytes_per_frame
            return
        start = self._current_frame * self._bytes_per_frame
        end = start + frames * self._bytes_per_frame
        if end <= len(self._data):
            outdata[:] = self._data[start:end]
            self._current_frame += frames
        else:
            remaining_bytes = len(self._data) - start
            outdata[:remaining_bytes] = self._data[start:]
            outdata[remaining_bytes:] = b"\x00" * (end - len(self._data))
            # reset for the next playback
            self._current_frame = 0
            self._target_time = None

    @copy_doc(BaseBackend.play)
    def play(self, when: float | None = None, *, blocking: bool = False) -> None:
        super().play(when, blocking=blocking)
        if self._target_time is not None:
            raise RuntimeError("The audio playback is already on-going.")
        self._target_time = (
            self._clock.get_time_ns()
            if when is None
            else self._clock.get_time_ns() + int(when * 1e9)
        )
        if blocking:
            wait = self._duration
            if when is not None:
                wait += when
            sleep(0.95 * wait)  # 5% margin
            while self._target_time is not None:
                # hog CPU for the last blocking part, based on _target_time and not on
                # an estimated duration as sleep(...) does.
                pass

    @copy_doc(BaseBackend.stop)
    def stop(self) -> None:
        super().stop()
        if self._target_time is None:
            warn("The audio playback was not on-going.")
        self._target_time = None


def _ensure_block_size(block_size: int) -> int:
    """Ensure the block_size argument is valid."""
    block_size = ensure_int(block_size, "block_size")
    if block_size < 0:
        raise ValueError(
            f"Argument 'block_size' must be greater or equal than 0. '{block_size}' is "
            "invalid."
        )
    return block_size


def _ensure_device(device: int | None) -> dict[str, str | int | float]:
    """Ensure the device argument is valid."""
    if device is None:
        idx = sd.default.device["output"]
        devices = sd.query_devices()
        if len(devices) == 0:
            raise RuntimeError("No audio devices found.")
        logger.debug("Selected device: %s\nAvailable devices\n%s", idx, devices)
        return devices[idx]
    device_idx = ensure_int(device, "device")
    devices = sd.query_devices()
    if len(devices) <= device_idx:
        raise ValueError(
            f"Invalid device index. There are only {len(devices)} devices."
        )
    device = devices[device_idx]
    if device["max_output_channels"] <= 0:
        raise ValueError(
            f"Device '{device_idx}: {device['name']}' does not support output "
            "channels. Please select a different device."
        )
    assert device_idx == device["index"]  # sanity-check
    return device


def _ensure_sample_rate(
    sample_rate: int | None, device: dict[str, str | int | float]
) -> int:
    """Ensure the sample_rate argument is valid."""
    if sample_rate is None:
        return int(device["default_samplerate"])
    sample_rate = ensure_int(sample_rate, "sample_rate")
    if sample_rate <= 0:
        raise ValueError(
            f"Argument 'sample_rate' must be greater than 0. '{sample_rate}' "
            "is invalid."
        )
    return sample_rate
