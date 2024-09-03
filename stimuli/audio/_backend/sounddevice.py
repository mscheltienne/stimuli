from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import sounddevice as sd

from ...time import Clock
from ...utils._checks import check_type, check_value, ensure_int
from ...utils.logs import warn

if TYPE_CHECKING:
    from numpy.typing import NDArray


class SoundSD:
    """Sounddevice backend for audio playback.

    Parameters
    ----------
    data : array of shape (n_frames, n_channels)
        The audio data to play provided as a 2 dimensional array of shape ``(n_frames,
        n_channels)``. The array layout must be C-contiguous. A one dimensional array of
        shape ``(n_frames,)`` is also accepted for mono audio.
    sample_rate : int
        The sample rate of the audio data, which should match the sample rate of the
        output device.
    device : int
        Device index of the output device as provided by
        :func:`sounddevice.query_devices()`.
    block_size : int
        he number of frames passed to the stream callback function, or the preferred
        block granularity for a blocking read/write stream. The special value
        ``blocksize=0`` may be used to request that the stream callback will receive an
        optimal (and possibly varying) number of frames based on host requirements and
        the requested latency settings.
    """

    def __init__(
        self,
        data: NDArray,
        sample_rate: float,
        device: int,
        block_size: int,
    ) -> None:
        check_type(data, (np.ndarray,), "data")
        sample_rate = ensure_int(sample_rate, "sample_rate")
        if sample_rate <= 0:
            raise ValueError(
                f"Argument 'sample_rate' must be greater than 0. '{sample_rate}' is "
                "invalid."
            )
        block_size = ensure_int(block_size, "block_size")
        if block_size < 0:
            raise ValueError(
                "Argument 'block_size' must be greater or equal than 0. "
                f"'{block_size}' is invalid."
            )
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
        if data.ndim == 2 and device["max_output_channels"] < data.shape[1]:
            raise ValueError(
                f"Device '{device_idx}: {device['name']}' does not support the number "
                f"of output channels ({data.shape[1]})."
            )
        if sample_rate != device["default_samplerate"]:
            warn(
                f"The sample rate provided to the 'SoundSD' backend ({sample_rate}) "
                "differs from the default sample rate of the device "
                f"({device['default_samplerate']})."
            )
        # convert the data array to a supported byte representation
        check_value(data.dtype.name, sd._sampleformats, "dtype")
        data = data if data.ndim == 2 else data[:, np.newaxis]
        self._data = data.tobytes(order="C")
        self._bytes_per_frame = data.shape[1] * data.itemsize
        # store device and callback variables
        self._device = device
        self._current_frame = 0
        self._clock = Clock()
        self._target_time = None
        # create and open the output stream
        self._stream = sd.RawOutputStream(
            blocksize=block_size,
            callback=self._callback,
            channels=data.shape[1] if data.ndim == 2 else 1,
            device=device_idx,
            dtype=data.dtype,
            latency="low",
            samplerate=sample_rate,
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

    def play(self, when: float | None = None) -> None:
        """Play the audio data.

        Parameters
        ----------
        when : float | None
            The relative time in seconds when to start playing the audio data. For
            instance, ``0.2`` will start playing in 200 ms. If ``None``, the audio data
            is played as soon as possible.
        """
        if self._target_time is not None:
            raise RuntimeError("The audio playback is already on-going.")
        self._target_time = (
            self._clock.get_time_ns()
            if when is None
            else self._clock.get_time_ns() + int(when * 1e9)
        )

    def stop(self) -> None:
        """Interrupt immediately the playback of the audio data."""
        if self._target_time is None:
            warn("The audio playback was not on-going.")
        self._target_time = None

    def __del__(self) -> None:
        """Make sure that we kill the stream during deletion."""
        if hasattr(self, "_stream"):
            self._stream.stop()
            self._stream.close()
