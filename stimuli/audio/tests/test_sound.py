import pytest
from numpy.testing import assert_allclose

from stimuli.audio import Noise, Sound


def test_sound_io_mono(tmp_path):
    """Test sound saving/loading."""
    sound = Noise("pink", volume=100, duration=0.5)
    sound.save(tmp_path / "test.wav")
    sound_loaded = Sound(tmp_path / "test.wav")
    assert_allclose(sound.signal, sound_loaded.signal)

    sound = Noise("pink", volume=50, duration=0.5)
    sound.save(tmp_path / "test.wav", overwrite=True)
    sound_loaded = Sound(tmp_path / "test.wav")
    sound_loaded.volume = 50
    assert_allclose(sound.signal, sound_loaded.signal)
    # test representation
    assert str(tmp_path / "test.wav") in repr(sound_loaded)
    # test duration setter
    duration = sound_loaded.duration
    with pytest.warns(RuntimeWarning, match="can not be changed"):
        sound_loaded.duration = 10
    assert duration == sound_loaded.duration


def test_invalid_sound(tmp_path):
    """Test invalid sound file."""
    fname = tmp_path / "test.txt"
    with open(fname, "w") as f:
        f.write("invalid")
    with pytest.raises(ValueError, match="Unsupported file extension"):
        Sound(fname)


def test_silent_sound(tmp_path):
    """Test loading a silent sound."""
    sound = Noise("pink", volume=0, duration=0.5)
    sound.save(tmp_path / "test.wav")
    with pytest.raises(RuntimeError, match="The loaded sound is silent."):
        Sound(tmp_path / "test.wav")
