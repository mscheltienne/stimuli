.. include:: ../links.inc

Audio
-----

The audio module provides classes for generating standard audio stimuli and for loading
existing files.

Sound generation
~~~~~~~~~~~~~~~~

Standard sounds can be generated like noise, amplitude modulated sounds or pure tones.

.. currentmodule:: stimuli.audio

.. autosummary::
    :toctree: ../generated/api

    Noise
    SoundAM
    Tone

Example usage::

    from stimuli.audio import Noise

    sound = Noise(color="pink", volume=50, duration=1)
    sound.play(when=0.2)  # schedule in 200 ms

Sound files
~~~~~~~~~~~

For more complex stimuli, the sounds can be loaded from files.

.. autosummary::
    :toctree: ../generated/api

    Sound

Example usage::

    from stimuli.audio import Sound

    sound = Sound("path/to/sound.wav")
    sound.play(when=0.2)  # schedule in 200 ms

Backend
~~~~~~~

The audio module uses the `sounddevice`_ library with a callback function to play the
sounds.

.. currentmodule:: stimuli.audio.backend

.. autosummary::
    :toctree: ../generated/api

    SoundSD
