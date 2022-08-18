"""
===========
Base sounds
===========

``simple-stimuli`` provides a common API across audio stimuli. The audio
stimuli can be either generated or loaded. A generated stimuli can be exported.
The volume, duration and other properties can be set when creating the stimuli
or updated between plays.
"""

#%%

from matplotlib import pyplot as plt

from stimuli.audio import Sound, Tone

#%%
#
# In this tutorial, we will create, edit, save and load a pure tone auditory
# stimuli. A pure tone is a signal with a sinusoidal waveform, that is a sine
# wave of any frequency, phase-shift and amplitude.
#
# Source: `Wikipedia <https://en.wikipedia.org/wiki/Pure_tone>`_

#%%
# Create and edit a pure tone
# ---------------------------
#
# To create the stimuli, we create a :class:`~stimuli.audio.Tone` object with
# a given volume and frequency.

sound = Tone(volume=10, frequency=440)  # La - A440

#%%
# We can listen to the sound we created with :meth:`~stimuli.audio.Tone.play`.

sound.play(blocking=True)

#%%
# We can edit the sound properties by replacing the value in the attributes.
# For instance, let's consider a stereo system and set the volume to ``10`` on
# the left channel and to ``30`` on the right channel.

sound.volume = (10, 30)  # 0 to 100

#%%
# We can also change the frequency to 1 kHz.

sound.frequency = 1000  # Hz

#%%
# The sound is updated each time an attribute is changed.

sound.play(blocking=True)

#%%
# Export/Load a sound
# -------------------
#
# We can export a sound with :meth:`~stimuli.audio.Tone.save`.

sound.save("my_pure_tone.wav")

#%%
# We can load a sound with :class:`~stimuli.audio.Sound`.

sound_loaded = Sound("my_pure_tone.wav")
sound_loaded.play(blocking=True)

#%%
# However, a loaded sound can be any type of sound. ``simple-stimuli`` does not
# know that the sound was exported with the ``save()`` method of one of its
# class. As such, the attributes that were specific to the original sound are
# not present anymore and can not be updated anymore.

print(hasattr(sound_loaded, "frequency"))

#%%
# Visualize a sound
# -----------------
#
# Finally, the underlying signal is stored in the ``signal`` attribute. The
# returned numpy array has 2 dimensions: ``(n_samples, n_channels)``. We can
# plot the signal of each channel.

f, ax = plt.subplots(2, 1, sharex=True, sharey=True)
ax[0].plot(sound.signal[:, 0])
ax[0].set_title("Right channel")
ax[1].plot(sound.signal[:, 1])
ax[1].set_title("Left channel")
