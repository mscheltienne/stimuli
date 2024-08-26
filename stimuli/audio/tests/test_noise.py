from itertools import product

import numpy as np
import pytest

from .. import Noise
from ..noise import _PSDS
from .test_base import _test_base, _test_no_volume


@pytest.mark.parametrize(
    ("volume", "sample_rate", "duration", "color"),
    product((10, 100), (44100, 48000), (1, 5), _PSDS.keys()),
)
def test_noise(volume, sample_rate, duration, color):
    """Test a noise sound."""
    sound = Noise(volume, sample_rate, duration, color)
    assert sound.volume == volume
    assert sound.sample_rate == sample_rate
    assert sound.duration == duration
    assert sound.color == color
    assert sound.times.size == sound.sample_rate * sound.duration
    assert sound.signal.shape == (sound.times.size, 2)
    assert np.isclose(np.max(np.abs(sound.signal)), volume / 100)


def test_color_setter():
    """Test color setter."""
    sound = Noise(10, color="white")
    assert sound.color == "white"
    sound.color = "pink"
    assert sound.color == "pink"


def test_base():
    """Test base functionalities with a noise."""
    _test_base(Noise)


def test_no_volume():
    """Test signal if volume is set to 0."""
    _test_no_volume(Noise)
