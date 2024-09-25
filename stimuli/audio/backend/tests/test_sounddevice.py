from __future__ import annotations

import os
from time import sleep
from typing import TYPE_CHECKING

import numpy as np
import pytest
import sounddevice as sd

from stimuli.audio.backend import SoundSD

if TYPE_CHECKING:
    from numpy.typing import NDArray


@pytest.fixture(scope="module")
def device() -> dict[str, str | int | float]:
    """Device used for testing."""
    return sd.query_devices(sd.default.device["output"])


@pytest.fixture(scope="module")
def duration() -> float:
    """Duration of the sound."""
    return 0.2


@pytest.fixture(scope="module")
def frequency() -> int:
    """Frequency of the sound."""
    return 440


@pytest.fixture(scope="module")
def data(
    device: dict[str, str | int | float], duration: float, frequency: int
) -> NDArray[np.float32]:
    """Sinusoid mono sound data."""
    sfreq = int(device["default_samplerate"])
    times = np.linspace(0, duration, int(duration * sfreq), endpoint=False)
    data = np.sin(2 * np.pi * frequency * times)
    data /= 10 * np.max(np.abs(data))  # normalize and lower volume
    return data.astype(np.float32)


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS", "") == "true", reason="Unreliable on CIs."
)
def test_backend_mono(
    device: dict[str, str | int | float], data: NDArray[np.float32], duration: float
) -> None:
    """Test the sounddevice backend with mono sounds."""
    sound = SoundSD(device["index"], int(device["default_samplerate"]))
    sound.initialize(data, 128)
    assert sound._target_time is None
    sound.play()
    assert sound._target_time is not None
    sleep(1.1 * duration)
    assert sound._target_time is None

    sound.play(when=5 * duration)
    assert sound._target_time is not None
    sleep(2 * duration)
    assert sound._target_time is not None
    sleep(3 * duration)
    assert sound._target_time is not None
    sleep(1.1 * duration)
    assert sound._target_time is None


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS", "") == "true", reason="Unreliable on CIs."
)
def test_backend_stereo(
    device: dict[str, str | int | float], data: NDArray[np.float32], duration: float
) -> None:
    """Test the sounddevice backend with stereo sounds."""
    if device["max_output_channels"] < 2:
        pytest.skip("Stereo output is not available.")
    data = np.ascontiguousarray(np.vstack((data, data)).T)
    sound = SoundSD(device["index"], int(device["default_samplerate"]))
    sound.initialize(data, 128)
    assert sound._target_time is None
    sound.play()
    assert sound._target_time is not None
    sleep(1.1 * duration)
    assert sound._target_time is None


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS", "") == "true", reason="Unreliable on CIs."
)
def test_backend_interrupt(
    device: dict[str, str | int | float], data: NDArray[np.float32]
) -> None:
    """Test interrupting a sound output."""
    sound = SoundSD(device["index"], int(device["default_samplerate"]))
    sound.initialize(data, 128)
    assert sound._target_time is None
    sound.play()
    sound.stop()
    with pytest.warns(RuntimeWarning, match="The audio playback was not on-going."):
        sound.stop()


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS", "") == "true", reason="Unreliable on CIs."
)
def test_backend_invalid_play(
    device: dict[str, str | int | float], data: NDArray[np.float32], duration: float
) -> None:
    """Test running a play twice."""
    sound = SoundSD(device["index"], int(device["default_samplerate"]))
    sound.initialize(data, 128)
    sound.play()
    with pytest.raises(RuntimeError, match="The audio playback is already on-going."):
        sound.play()
    sleep(1.1 * duration)
    sound.play(when=3 * duration)
    with pytest.raises(RuntimeError, match="The audio playback is already on-going."):
        sound.play()
    sound.stop()
    sound.play()
    sound.stop()


def test_invalid_data(
    device: dict[str, str | int | float], data: NDArray[np.float32]
) -> None:
    """Test invalid data types and C-contiguousness."""
    sound = SoundSD(device["index"], int(device["default_samplerate"]))
    with pytest.raises(ValueError, match="Invalid value for the 'dtype' parameter"):
        sound.initialize(data.astype(np.float64), 128)
    data = np.hstack((data, data)).reshape(-1, data.size).T
    assert not data.flags["C_CONTIGUOUS"]
    with pytest.warns(
        RuntimeWarning, match="The data array provided .* is not C-contiguous"
    ):
        sound.initialize(data, 128)
    data = np.ascontiguousarray(data)[:, np.newaxis]
    assert data.ndim == 3
    with pytest.raises(ValueError, match="must be 1D or 2D"):
        sound.initialize(data, 128)


def test_invalid_number_of_channels(
    device: dict[str, str | int | float], data: NDArray[np.float32]
) -> None:
    """Test invalid number of channels."""
    n_channels = device["max_output_channels"]
    data = np.ascontiguousarray(np.vstack([data] * (n_channels + 1)).T)
    sound = SoundSD(device["index"], int(device["default_samplerate"]))
    with pytest.raises(
        ValueError, match="does not support the number of output channels"
    ):
        sound.initialize(data, 128)


def test_invalid_device_inex() -> None:
    """Test invalid device index."""
    devices = sd.query_devices()
    with pytest.raises(ValueError, match="Invalid device index"):
        SoundSD(len(devices), 44100)
    with pytest.raises(ValueError, match="Invalid device index"):
        SoundSD(len(devices) + 101, 44100)


def test_invalid_block_size(
    device: dict[str, str | int | float], data: NDArray[np.float32], duration: float
) -> None:
    """Test invalid block size."""
    sound = SoundSD(device["index"], int(device["default_samplerate"]))
    with pytest.raises(ValueError, match="greater or equal than 0"):
        sound.initialize(data, -1)
    sound.initialize(data, 0)
    sound.play()
    assert sound._target_time is not None
    sleep(2 * duration)
    assert sound._target_time is None


def test_invalid_sample_rate(device: dict[str, str | int | float]) -> None:
    """Test invalid sample rate."""
    with pytest.raises(ValueError, match="greater than 0"):
        SoundSD(device["index"], 0)
    sfreq = int(device["default_samplerate"])
    with pytest.warns(RuntimeWarning, match="differs from the default sample rate"):
        SoundSD(device["index"], sfreq + 101)
