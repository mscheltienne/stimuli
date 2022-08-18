from itertools import product

import numpy as np
import pytest

from .. import Tone
from .test_base import _test_base, _test_no_volume, _test_window


def _check_frequency(signal, sample_rate, target):
    """Check frequency of the tone."""
    frequencies = np.fft.rfftfreq(signal.shape[0], 1 / sample_rate)
    fftval = np.abs(np.fft.rfft(signal, axis=0))
    idx = np.argmax(fftval, axis=0)
    assert np.allclose(frequencies[idx], np.array([target, target]))


@pytest.mark.parametrize(
    "volume, sample_rate, duration", product((10, 100), (44100, 48000), (1, 5))
)
def test_tone(volume, sample_rate, duration):
    """Test a tone sound."""
    sound = Tone(volume, sample_rate, duration)
    assert sound.volume == volume
    assert sound.sample_rate == sample_rate
    assert sound.duration == duration
    assert sound.times.size == sound.sample_rate * sound.duration
    assert sound.signal.shape == (sound.times.size, 2)
    assert np.isclose(np.max(np.abs(sound.signal)), volume / 100)
    assert sound.frequency == 440
    _check_frequency(sound.signal, sound.sample_rate, 440)


@pytest.mark.parametrize("frequency", (101, 440, 1000))
def test_tone_frequency(frequency):
    """Test tone with different frequencies."""
    sound = Tone(volume=10, frequency=frequency)
    assert sound.frequency == frequency
    _check_frequency(sound.signal, sound.sample_rate, frequency)


@pytest.mark.parametrize("frequency", (101, 440, 1000))
def test_tone_frequency_setter(frequency):
    """Test tone frequency setter."""
    sound = Tone(volume=10, frequency=10)
    assert sound.frequency == 10
    sound.frequency = frequency
    assert sound.frequency == frequency
    _check_frequency(sound.signal, sound.sample_rate, frequency)


def test_base():
    """Test base functionalities with a tone."""
    _test_base(Tone)


def test_no_volume():
    """Test signal if volume is set to 0."""
    _test_no_volume(Tone)


def test_window():
    """Test application of a window."""
    _test_window(Tone)
