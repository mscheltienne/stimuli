from itertools import product

import numpy as np
import pytest
from scipy.signal import find_peaks

from .. import ASSR
from .test_base import _test_base, _test_no_volume


def _check_frequency(signal, sample_rate, carrier, modulation, method):
    """Check frequency of the ASSR with conventional modulation."""
    frequencies = np.fft.rfftfreq(signal.shape[0], 1 / sample_rate)
    fftval = np.abs(np.fft.rfft(signal, axis=0))
    height = 0.1 * np.max(fftval)
    peaks1 = find_peaks(fftval[:, 0], height=height)[0]
    peaks1 = peaks1.astype(int)
    peaks2 = find_peaks(fftval[:, 1], height=height)[0]
    peaks2 = peaks2.astype(int)
    assert (peaks1 == peaks2).all()
    if method == "conventional":
        peaks = peaks1
        assert peaks.size == 3
        idx = np.argmax(fftval, axis=0)
        assert np.allclose(frequencies[idx], np.array([carrier, carrier]))
        # remove carrier from peaks
        peaks = [elt for elt in peaks1 if elt not in idx]
    elif method == "dsbsc":
        peaks = peaks1
        assert peaks.size == 2
        assert carrier not in frequencies[peaks]
    assert np.allclose(
        frequencies[peaks],
        np.array([carrier - modulation, carrier + modulation]),
    )


@pytest.mark.parametrize(
    "volume, sample_rate, duration, method",
    product((10, 100), (44100, 48000), (1, 5), ("conventional", "dsbsc")),
)
def test_assr(volume, sample_rate, duration, method):
    """Test an ASSR sound."""
    sound = ASSR(volume, sample_rate, duration, method=method)
    assert sound.volume == volume
    assert sound.sample_rate == sample_rate
    assert sound.duration == duration
    assert sound.times.size == sound.sample_rate * sound.duration
    assert sound.signal.shape == (sound.times.size, 2)
    assert np.isclose(np.max(np.abs(sound.signal)), volume / 100)
    assert sound.frequency_carrier == 1000
    assert sound.frequency_modulation == 40
    _check_frequency(sound.signal, sound.sample_rate, 1000, 40, method)


@pytest.mark.parametrize(
    "carrier, modulation, method",
    product((300, 1000, 5000), (20, 50), ("conventional", "dsbsc")),
)
def test_assr_frequencies(carrier, modulation, method):
    """Test ASSR with different frequencies."""
    sound = ASSR(
        volume=10,
        frequency_carrier=carrier,
        frequency_modulation=modulation,
        method=method,
    )
    assert sound.frequency_carrier == carrier
    assert sound.frequency_modulation == modulation
    _check_frequency(
        sound.signal,
        sound.sample_rate,
        carrier,
        modulation,
        method,
    )


@pytest.mark.parametrize(
    "carrier, modulation, method",
    product((300, 1000, 5000), (20, 50), ("conventional", "dsbsc")),
)
def test_assr_frequencies_setter(carrier, modulation, method):
    """Test ASSR frequency setter."""
    sound = ASSR(
        volume=10,
        frequency_carrier=200,
        frequency_modulation=10,
        method=method,
    )
    assert sound.frequency_carrier == 200
    assert sound.frequency_modulation == 10
    sound.frequency_carrier = carrier
    assert sound.frequency_carrier == carrier
    assert sound.frequency_modulation == 10
    _check_frequency(
        sound.signal,
        sound.sample_rate,
        carrier,
        sound.frequency_modulation,
        method,
    )
    sound.frequency_modulation = modulation
    assert sound.frequency_carrier == carrier
    assert sound.frequency_modulation == modulation
    _check_frequency(
        sound.signal,
        sound.sample_rate,
        carrier,
        modulation,
        method,
    )


def test_assr_method_setter():
    """Test ASSR method setter."""
    method = "conventional"
    sound = ASSR(10, method=method)
    assert sound.method == method
    _check_frequency(sound.signal, sound.sample_rate, 1000, 40, method)
    method = "dsbsc"
    sound.method = method
    assert sound.method == method
    _check_frequency(sound.signal, sound.sample_rate, 1000, 40, method)
    method = "conventional"
    sound.method = method
    assert sound.method == method
    _check_frequency(sound.signal, sound.sample_rate, 1000, 40, method)


def test_base():
    """Test base functionalities with an ASSR."""
    _test_base(ASSR)


def test_no_volume():
    """Test signal if volume is set to 0."""
    _test_no_volume(ASSR)
