import numpy as np
import pytest

from stimuli.audio import BaseSound


def test_check_volume():
    """Check the volume static checker."""
    volume = BaseSound._check_volume(50)
    assert np.allclose(volume, np.array([50, 50]))
    volume = BaseSound._check_volume((25, 50))
    assert np.allclose(volume, np.array([25, 50]))
    volume = BaseSound._check_volume((0, 100))
    assert np.allclose(volume, np.array([0, 100]))
    with pytest.raises(TypeError, match="must be an instance of numeric or tuple"):
        BaseSound._check_volume([25, 50])
    with pytest.raises(AssertionError):
        volume = BaseSound._check_volume((25, 50, 75))
    with pytest.raises(TypeError, match="must be an instance of numeric"):
        volume = BaseSound._check_volume(("25", 50))
    with pytest.raises(AssertionError):
        volume = BaseSound._check_volume((25, 101))
    with pytest.raises(AssertionError):
        volume = BaseSound._check_volume((-25, 100))


def test_check_sample_rate():
    """Check the sample rate static checker."""
    fs = BaseSound._check_sample_rate(44100)
    assert fs == 44100
    with pytest.raises(TypeError, match="must be an instance of int"):
        BaseSound._check_sample_rate(44100.0)
    with pytest.raises(AssertionError):
        BaseSound._check_sample_rate(-101)


def test_check_duration():
    """Check the duration static checker."""
    duration = BaseSound._check_duration(101)
    assert duration == 101
    duration = BaseSound._check_duration(101.01)
    assert duration == 101.01
    with pytest.raises(TypeError, match="must be an instance of numeric"):
        BaseSound._check_duration([101])
    with pytest.raises(AssertionError):
        BaseSound._check_sample_rate(-101)
