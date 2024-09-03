from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import sounddevice as sd

from ...time import Clock
from ...utils._checks import check_type, ensure_int
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
    block_size : int
        he number of frames passed to the stream callback function, or the preferred
        block granularity for a blocking read/write stream. The special value
        ``blocksize=0`` may be used to request that the stream callback will receive an
        optimal (and possibly varying) number of frames based on host requirements and
        the requested latency settings.
    device : int
        Device index of the output device as provided by
        :func:`sounddevice.query_devices()`.
    """

    def __init__(
        self,
        data: NDArray,
        sample_rate: float,
        block_size: int,
        device: int,
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
        # store data, device and callback variables
        self._data = data if data.ndim == 2 else data[:, np.newaxis]
        self._device = device
        self._current_frame = 0
        self._clock = Clock()
        self._target_time = None
        # create and open the output stream
        self._stream = sd.OutputStream(
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
            outdata.fill(0)
            return
        delta_ns = int((time_info.outputBufferDacTime - time_info.currentTime) * 1e9)
        if self._clock.get_time_ns() + delta_ns < self._target_time:
            outdata.fill(0)
            return
        end = self._current_frame + frames
        if end <= self._data.shape[0]:
            outdata[:frames, :] = self._data[self._current_frame : end, :]
            self._current_frame += frames
        else:
            data = self._data[self._current_frame :, :]
            data = np.vstack(
                (
                    data,
                    np.zeros((frames - data.shape[0], data.shape[1]), dtype=data.dtype),
                )
            )
            outdata[:frames, :] = data
            # reset
            self._current_frame = 0
            self._target_time = None

    def play(self, when: float | None = None) -> None:
        """Play the audio data.

        Parameters
        ----------
        when : float | None
            The relative time in seconds when to start playing the audio data. For
            instance, ``0.2`` wil start playing in 200 ms. If ``None``, the audio data
            is played as soon as possible.
        """
        self._target_time = (
            self._clock.get_time_ns()
            if when is None
            else self._clock.get_time_ns() + int(when * 1e9)
        )

    def stop(self) -> None:
        """Interrupt immediately the playback of the audio data."""
        self._target_time = None

    def __del__(self) -> None:
        """Make sure that we kill the stream during deletion."""
        if hasattr(self, "_stream"):
            self._stream.stop()
            self._stream.close()
