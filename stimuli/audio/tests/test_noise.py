from itertools import product

import numpy as np
import pytest
from numpy.testing import assert_allclose

from stimuli.audio import Noise
from stimuli.audio.noise import _PSDS


@pytest.mark.parametrize(
    ("color", "volume", "duration"), product(_PSDS.keys(), (10, 100), (1, 5))
)
def test_noise(color, volume, duration):
    """Test a noise sound."""
    sound = Noise(color=color, volume=volume, duration=duration)
    assert sound.volume.ndim == 1
    assert all(sound.volume == volume)
    assert sound.duration == duration
    assert sound.times.size == int(sound.sample_rate * sound.duration)
    assert sound.signal.shape == (sound.times.size, 1)
    assert_allclose(np.max(np.abs(sound.signal)), volume / 100)
    assert sound.color == color


def test_color_setter():
    """Test changing the color of the noise."""
    sound = Noise(color="white", volume=10, duration=1)
    assert sound.color == "white"
    data_orig = sound._backend._data
    sound.color = "pink"
    assert sound.color == "pink"
    assert data_orig != sound._backend._data


def test_duration_setter():
    """Test changing the duration of the sound."""
    sound = Noise(volume=10, duration=1, color="white")
    sound.duration = 0.05
    assert_allclose(sound.duration, 0.05, atol=1 / sound.sample_rate)
    assert_allclose(sound.times.size, sound.sample_rate * sound.duration, atol=1)
    assert sound.signal.shape == (sound.times.size, 1)
