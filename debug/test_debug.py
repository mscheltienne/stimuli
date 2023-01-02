import sounddevice as sd
import numpy as np

from stimuli.audio import Tone

def test_1():
    sd.play(np.random.randn(96000, 2), samplerate=48000, mapping=[1,2])


def test_2():
    sound = Tone(100)
    sound.play()
