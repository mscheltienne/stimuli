from __future__ import annotations

from itertools import product
from typing import TYPE_CHECKING

import numpy as np
import pytest
from matplotlib import pyplot as plt
from numpy.testing import assert_allclose

from stimuli.audio import Tone
from stimuli.audio.tone import _check_frequency

if TYPE_CHECKING:
    from numpy.typing import NDArray


def _assert_frequency(signal: NDArray, sample_rate: float, target: float) -> None:
    """Check frequency of the tone."""
    frequencies = np.fft.rfftfreq(signal.shape[0], 1 / sample_rate)
    fftval = np.abs(np.fft.rfft(signal, axis=0))
    idx = np.argmax(fftval, axis=0)
    assert_allclose(frequencies[idx], target)


@pytest.mark.parametrize(
    ("volume", "duration", "frequency"), product((10, 100), (1, 5), (440, 1000))
)
def test_tone(volume: float, duration: float, frequency: float) -> None:
    """Test a tone sound."""
    sound = Tone(frequency, volume, duration)
    assert sound.volume.ndim == 1
    assert all(sound.volume == volume)
    assert sound.duration == duration
    assert sound.times.size == int(sound.sample_rate * sound.duration)
    assert sound.signal.shape == (sound.times.size, 1)
    assert_allclose(np.max(np.abs(sound.signal)), volume / 100)
    assert sound.frequency == frequency
    _assert_frequency(sound.signal, sound.sample_rate, frequency)
    # test representation
    assert "Pure tone" in repr(sound)
    assert f"{frequency:.2f} Hz" in repr(sound)


def test_frequency_setter() -> None:
    """Test changing the frequency of the sound."""
    sound = Tone(frequency=440, volume=10, duration=1)
    _assert_frequency(sound.signal, sound.sample_rate, 440)
    data_orig = sound._backend._data
    sound.frequency = 1000
    _assert_frequency(sound.signal, sound.sample_rate, 1000)
    assert data_orig != sound._backend._data


def test_check_frequency() -> None:
    """Test validation of frequency."""
    _check_frequency(440)
    with pytest.raises(ValueError, match="The frequency must be a strictly positive"):
        _check_frequency(0)
    with pytest.raises(ValueError, match="The frequency must be a strictly positive"):
        _check_frequency(-440)
    with pytest.raises(TypeError, match="must be an instance of"):
        _check_frequency("440")


def test_tone_plot() -> None:
    """Test plotting a tone."""
    sound = Tone(frequency=440, volume=10, duration=1)
    f, ax = sound.plot()
    assert isinstance(f, plt.Figure)
    assert isinstance(ax, plt.Axes)
    plt.close("all")
