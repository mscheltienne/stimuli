import time

import numpy as np
import pytest

from stimuli.audio import WhiteNoise


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
    duration = 2
    sound = WhiteNoise(10, duration=duration)

    # test play/stop
    sound.play()
    time.sleep(duration)

    start = time.time()
    sound.play(blocking=True)
    assert np.isclose(duration, time.time() - start, atol=0.1)

    start = time.time()
    sound.play(blocking=False)
    sound.stop()
    assert time.time() - start <= duration

    # test volume setter
    assert np.isclose(np.max(np.abs(sound.signal)), sound.volume / 100)
    sound.volume = 20
    assert sound.volume == 20
    assert np.isclose(np.max(np.abs(sound.signal)), sound.volume / 100)
    sound.volume = (20, 100)
    assert sound.volume == (20, 100)
    assert np.allclose(
        np.max(np.abs(sound.signal), axis=0), np.array(sound.volume) / 100
    )

    # test sample rate and duration setter
    assert sound.sample_rate == 44100
    assert sound.duration == duration
    assert sound.times.size == sound.sample_rate * sound.duration
    sound.sample_rate = 48000
    assert sound.sample_rate == 48000
    assert sound.duration == duration
    assert sound.times.size == sound.sample_rate * sound.duration
    sound.duration = 1
    assert sound.sample_rate == 48000
    assert sound.duration == 1
    assert sound.times.size == sound.sample_rate * sound.duration
