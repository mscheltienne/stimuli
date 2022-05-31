from itertools import product

import numpy as np
import pytest

from ... import logger
from .. import ASSR, Sound, Tone, WhiteNoise

logger.propagate = True

SoundClasses = (ASSR, Tone, WhiteNoise)


@pytest.mark.parametrize("SoundClass", SoundClasses)
def test_io(tmp_path, SoundClass):
    """Test save/load for all sound classes."""
    fname = tmp_path / f"sound-{SoundClass.__name__}-1.wav"
    sound = SoundClass(volume=100)
    sound.save(fname, overwrite=False)
    sound_loaded = Sound(fname)
    assert sound_loaded.volume == 100
    assert np.allclose(sound.signal, sound_loaded.signal)

    fname = tmp_path / f"sound-{SoundClass.__name__}-2.wav"
    sound = SoundClass(volume=10)
    sound.save(fname, overwrite=False)
    sound_loaded = Sound(fname)
    assert sound_loaded.volume == 100
    sound_loaded.volume = 10
    assert np.allclose(sound.signal, sound_loaded.signal)

    fname = tmp_path / f"sound-{SoundClass.__name__}-3.wav"
    sound = SoundClass(volume=(50, 25))
    sound.save(fname, overwrite=False)
    sound_loaded = Sound(fname)
    assert sound_loaded.volume == 100
    sound_loaded.volume = (50, 25)
    assert np.allclose(sound.signal, sound_loaded.signal)


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.parametrize("SoundClass", SoundClasses)
def test_io_with_muted_channel(tmp_path, SoundClass):
    """Test save/load for all sound classes with a muted channel."""
    fname = tmp_path / f"sound-{SoundClass.__name__}-1.wav"
    sound = SoundClass(volume=(50, 0))
    sound.save(fname, overwrite=True)
    sound_loaded = Sound(fname)
    assert np.allclose(sound_loaded.volume, (100, 0))
    sound_loaded.volume = (50, 0)
    assert np.allclose(sound.signal, sound_loaded.signal)


@pytest.mark.parametrize("SoundClass", SoundClasses)
def test_overwrite(tmp_path, SoundClass):
    """Test the overwrite argument."""
    fname = tmp_path / f"sound-{SoundClass.__name__}-1.wav"
    sound = SoundClass(volume=100)
    sound.save(fname, overwrite=True)
    sound2 = SoundClass(volume=100, duration=2)
    with pytest.raises(RuntimeError, match="already exist"):
        sound2.save(fname, overwrite=False)
    sound2.save(fname, overwrite=True)
    sound_loaded = Sound(fname)
    assert sound_loaded.volume == 100
    assert sound.signal.shape != sound_loaded.signal.shape
    assert np.allclose(sound2.signal, sound_loaded.signal)


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.parametrize("SoundClass", SoundClasses)
def test_reset(tmp_path, SoundClass):
    """Test the reset method."""
    # with a change of volume
    fname = tmp_path / f"sound-{SoundClass.__name__}-1.wav"
    sound = SoundClass(volume=100)
    sound.save(fname, overwrite=True)
    sound_loaded = Sound(fname)
    assert sound_loaded.volume == 100
    sound_loaded.volume = 5
    assert sound_loaded.volume == 5
    assert not np.allclose(sound_loaded.signal, sound.signal)
    sound_loaded.reset()
    assert np.allclose(sound_loaded.signal, sound.signal)
    assert sound_loaded.volume == 100

    # with a channel muted
    fname = tmp_path / f"sound-{SoundClass.__name__}-2.wav"
    sound = SoundClass(volume=(100, 0))
    sound.save(fname, overwrite=True)
    sound_loaded = Sound(fname)
    assert np.allclose(sound_loaded.volume, (100, 0))
    sound_loaded.volume = (5, 0)
    assert np.allclose(sound_loaded.volume, (5, 0))
    assert not np.allclose(sound_loaded.signal, sound.signal)
    sound_loaded.reset()
    assert np.allclose(sound_loaded.signal, sound.signal)
    assert np.allclose(sound_loaded.volume, (100, 0))

    # with a crop
    fname = tmp_path / f"sound-{SoundClass.__name__}-3.wav"
    sound = SoundClass(volume=100, duration=10)
    sound.save(fname, overwrite=True)
    sound_loaded = Sound(fname)
    assert sound_loaded.volume == 100
    sound_loaded.crop(tmin=1, tmax=5)
    assert sound_loaded.signal.shape != sound.signal.shape
    sound_loaded.reset()
    assert sound_loaded.signal.shape == sound.signal.shape


@pytest.mark.parametrize(
    "SoundClass, tmin, tmax", product(SoundClasses, (1, None), (5, None))
)
def test_crop(tmp_path, SoundClass, tmin, tmax):
    """Test the crop method."""
    fname = tmp_path / f"sound-{SoundClass.__name__}-1.wav"
    sound = SoundClass(volume=100, duration=10)
    sound.save(fname, overwrite=True)
    sound_loaded = Sound(fname)
    assert sound_loaded.duration == sound.duration
    sound_loaded.crop(tmin=tmin, tmax=tmax)
    tmin = sound_loaded.times[0] if tmin is None else tmin
    tmax = sound_loaded.times[-1] if tmax is None else tmax
    assert np.isclose(
        sound_loaded.duration, tmax - tmin, atol=2 / sound_loaded.sample_rate
    )
    assert np.isclose(
        sound_loaded.times[-1] - sound_loaded.times[0],
        sound_loaded.duration,
        atol=2 / sound_loaded.sample_rate,
    )
    assert np.isclose(
        sound_loaded._times[-1] - sound_loaded._times[0],
        sound_loaded.duration,
        atol=2 / sound_loaded.sample_rate,
    )
    assert sound_loaded.times.size == sound_loaded.signal.shape[0]


@pytest.mark.parametrize("SoundClass", SoundClasses)
def test_successive_crop(tmp_path, SoundClass):
    """Test successive crops."""
    fname = tmp_path / f"sound-{SoundClass.__name__}-1.wav"
    sound = SoundClass(volume=100, duration=10)
    sound.save(fname, overwrite=True)
    sound_loaded = Sound(fname)
    assert sound_loaded.tmin == 0
    assert sound_loaded.tmax == 10
    sound_loaded.crop(tmin=1, tmax=8)
    assert np.isclose(sound_loaded.tmin, 1, atol=2 / sound_loaded.sample_rate)
    assert np.isclose(sound_loaded.tmax, 8, atol=2 / sound_loaded.sample_rate)
    sound_loaded.crop(tmin=1, tmax=None)
    assert np.isclose(sound_loaded.tmin, 1, atol=2 / sound_loaded.sample_rate)
    assert np.isclose(sound_loaded.tmax, 10, atol=2 / sound_loaded.sample_rate)
    sound_loaded.crop(tmin=1, tmax=5)
    assert np.isclose(sound_loaded.tmin, 1, atol=2 / sound_loaded.sample_rate)
    assert np.isclose(sound_loaded.tmax, 5, atol=2 / sound_loaded.sample_rate)


@pytest.mark.parametrize("SoundClass", SoundClasses)
def test_sample_rate(tmp_path, caplog, SoundClass):
    """Test the sample-rate property."""
    fname = tmp_path / f"sound-{SoundClass.__name__}-1.wav"
    sound = SoundClass(volume=100)
    sound.save(fname, overwrite=True)
    sound_loaded = Sound(fname)
    assert sound_loaded.sample_rate == sound.sample_rate
    caplog.clear()
    sound_loaded.sample_rate = 101
    assert "The sampling rate property" in caplog.text
    assert sound_loaded.sample_rate == sound.sample_rate


@pytest.mark.parametrize("SoundClass", SoundClasses)
def test_duration(tmp_path, caplog, SoundClass):
    """Test the duration property."""
    fname = tmp_path / f"sound-{SoundClass.__name__}-1.wav"
    sound = SoundClass(volume=100)
    sound.save(fname, overwrite=True)
    sound_loaded = Sound(fname)
    assert sound_loaded.duration == sound.duration
    caplog.clear()
    sound_loaded.duration = 101
    assert "The duration property" in caplog.text
    assert sound_loaded.duration == sound.duration
