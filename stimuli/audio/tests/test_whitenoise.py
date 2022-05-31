import numpy as np
import pytest

from .. import WhiteNoise
from .test_base import _test_base


@pytest.mark.parametrize("volume", (10, 25, 70, 100))
def test_whitenoise(volume):
    """Test a whitenoise sound."""
    sound = WhiteNoise(volume)
    assert sound.times.size == sound.sample_rate * sound.duration
    assert sound.signal.shape == (sound.times.size, 2)
    assert sound.volume == volume
    assert np.isclose(np.max(np.abs(sound.signal)), volume / 100)


def test_base():
    """Test base functionalities with a whitenoise."""
    _test_base(WhiteNoise)
