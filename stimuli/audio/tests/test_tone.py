import numpy as np
import pytest

from .. import Tone
from .test_base import _test_base


@pytest.mark.parametrize("volume", (10, 25, 70, 100))
def test_tone(volume):
    """Test a tone sound."""
    sound = Tone(volume)
    assert sound.times.size == sound.sample_rate * sound.duration
    assert sound.signal.shape == (sound.times.size, 2)
    assert sound.volume == volume
    assert np.isclose(np.max(np.abs(sound.signal)), volume / 100)

    # retrieve frequency
    fftval = np.abs(np.fft.rfft(sound.signal, axis=0))
    idx = np.argmax(fftval, axis=0)
    frequencies = np.fft.rfftfreq(sound.signal.shape[0], 1 / sound.sample_rate)
    assert np.allclose(frequencies[idx], np.array([440, 440]))

    # test frequency setter
    sound.frequency = 1000
    fftval = np.abs(np.fft.rfft(sound.signal, axis=0))
    idx = np.argmax(fftval, axis=0)
    frequencies = np.fft.rfftfreq(sound.signal.shape[0], 1 / sound.sample_rate)
    assert np.allclose(frequencies[idx], np.array([1000, 1000]))


def test_base():
    """Test base functionalities with a whitenoise."""
    _test_base(Tone)
