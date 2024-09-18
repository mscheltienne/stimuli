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
