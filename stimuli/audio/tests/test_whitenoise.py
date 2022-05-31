from itertools import product

import numpy as np
import pytest

from .. import WhiteNoise
from .test_base import _test_base, _test_no_volume


@pytest.mark.parametrize(
    "volume, sample_rate, duration", product((10, 100), (44100, 48000), (1, 5))
)
def test_whitenoise(volume, sample_rate, duration):
    """Test a whitenoise sound."""
    sound = WhiteNoise(volume, sample_rate, duration)
    assert sound.volume == volume
    assert sound.sample_rate == sample_rate
    assert sound.duration == duration
    assert sound.times.size == sound.sample_rate * sound.duration
    assert sound.signal.shape == (sound.times.size, 2)
    assert np.isclose(np.max(np.abs(sound.signal)), volume / 100)


def test_base():
    """Test base functionalities with a whitenoise."""
    _test_base(WhiteNoise)


def test_no_volume():
    """Test signal if volume is set to 0."""
    _test_no_volume(WhiteNoise)
