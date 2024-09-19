from itertools import product

import numpy as np
import pytest
from numpy.testing import assert_allclose

from stimuli.audio import Noise, SoundAM, Tone
from stimuli.audio._base import _check_duration, _ensure_volume


def test_check_duration():
    """Test duration validation."""
    _check_duration(0.1)
    _check_duration(10)
    with pytest.raises(TypeError, match="must be an instance of"):
        _check_duration(None)
    with pytest.raises(TypeError, match="must be an instance of"):
        _check_duration("10")
    with pytest.raises(ValueError, match="a strictly positive number"):
        _check_duration(-10)
    with pytest.raises(ValueError, match="a strictly positive number"):
        _check_duration(0)


@pytest.mark.parametrize(("volume", "n_channels"), product((0, 50, 100), (1, 2)))
def test_ensure_volume_valid(volume, n_channels):
    """Test volume validation."""
    vol = _ensure_volume(volume, n_channels)
    assert vol.ndim == 1
    assert vol.shape == (n_channels,)
    assert all(vol == volume)


def test_ensure_volume_invalid():
    """Test volume validation."""
    with pytest.raises(TypeError, match="must be an instance of"):
        _ensure_volume(None, 1)
    with pytest.raises(TypeError, match="must be an instance of"):
        _ensure_volume("10", 1)
    with pytest.raises(ValueError, match="The volume must be a percentage"):
        _ensure_volume(-10, 1)
    with pytest.raises(ValueError, match="The volume must be a percentage"):
        _ensure_volume(110, 1)


@pytest.mark.parametrize(
    ("durations", "sound"),
    product(
        ((1, 0.05), (0.1, 2)),
        (
            # don't test noise as the resampling can lead to lengths off by 1 sample
            (Tone, dict(frequency=440)),
            (
                SoundAM,
                dict(frequency_carrier=1000, frequency_modulation=40, method="dsbsc"),
            ),
        ),
    ),
)
def test_duration_setter(durations, sound):
    """Test changing the duration of the sound."""
    sound = sound[0](volume=10, duration=durations[0], **sound[1])
    len_data_backend = len(sound._backend._data)
    sound.duration = durations[1]
    assert sound.duration == durations[1]
    assert sound.times.size == int(sound.sample_rate * durations[1])
    assert sound.signal.shape == (sound.times.size, 1)
    assert len(sound._backend._data) == len_data_backend / (durations[0] / durations[1])


@pytest.mark.parametrize(
    ("volumes", "sound"),
    product(
        ((10, 50), (70, 20)),
        (
            (Tone, dict(frequency=440)),
            (Noise, dict(color="white")),
            (
                SoundAM,
                dict(frequency_carrier=1000, frequency_modulation=40, method="dsbsc"),
            ),
        ),
    ),
)
def test_volume_setter(volumes, sound):
    """Test changing the volume of the sound."""
    sound = sound[0](volume=volumes[0], duration=1, **sound[1])
    assert_allclose(np.max(np.abs(sound.signal)), volumes[0] / 100)
    data_orig = sound._backend._data
    sound.volume = volumes[1]
    assert_allclose(np.max(np.abs(sound.signal)), volumes[1] / 100)
    assert data_orig != sound._backend._data


def test_save(tmp_path):
    """Test saving a sound."""
    sound = Tone(volume=10, duration=0.1, frequency=440)
    sound.save(tmp_path / "test.wav")
    assert (tmp_path / "test.wav").exists()
    with pytest.raises(FileExistsError, match="already exists"):
        sound.save(tmp_path / "test.wav")
    sound.save(tmp_path / "test.wav", overwrite=True)
    assert (tmp_path / "test.wav").exists()
    with pytest.raises(ValueError, match="extension must be"):
        sound.save(tmp_path / "test.mp3")
    assert not (tmp_path / "test.mp3").exists()
