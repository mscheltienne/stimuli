from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

import numpy as np
import sounddevice as sd

from ...time import sleep
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
        # store data, device and open the output stream
        self._data = data
        self._device = device
        self._stream = sd.OutputStream(
            samplerate=sample_rate,
            blocksize=block_size,
            device=device_idx,
            channels=data.shape[1] if data.ndim == 2 else 1,
            dtype=data.dtype,
        )
        self._stream.start()
        self._executor = ThreadPoolExecutor(max_workers=1)

    def play(self, when: float = 0) -> None:
        """Play the audio data.

        Parameters
        ----------
        when : float
            Delay in seconds before the audio data is played. The 'when' argument can be
            used to schedule the sound delivery.
        """
        self._executor.submit(self._play, when)

    def _play(self, when: float) -> None:
        """Play the audio data."""
        sleep(when)
        self._stream.write(self._data)

    def __del__(self) -> None:
        """Make sure that we kill the stream and the threadpool during deletion."""
        if hasattr(self, "_executor"):
            self._executor.shutdown(wait=True, cancel_futures=True)
        if hasattr(self, "_stream"):
            self._stream.stop()
            self._stream.close()
