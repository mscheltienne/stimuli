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
# The sampling rate can be changed. Typical values are 44.1 kHz and 48 kHz.

sound.sample_rate = 48000  # Hz

#%%
# Export/Load a sound
# -------------------
#
# We can export a sound with :meth:`~stimuli.audio.Tone.save`.

sound.save("my_pure_tone.wav", overwrite=True)

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
# Only the basic attributes are preserved: ``duration``, ``sample_rate``.

print(f"Duration of the original sound: {sound.duration} second.")
print(f"Duration of the loaded sound: {sound_loaded.duration} second.")
print(f"Sample rate of the original sound: {sound.sample_rate} Hz.")
print(f"Sample rate of the loaded sound: {sound_loaded.sample_rate} Hz.")

#%%
# The volume is normalized, with the loudest channel set to ``100``. The ratio
# between channels is preserved.

print(
    "Volume of the original sound: %s"
    % "({:.1f}, {:.1f})".format(*sound.volume)
)
print(
    "Volume of the loaded sound: %s"
    % "({:.1f}, {:.1f})".format(*sound_loaded.volume)
)

#%%
# Visualize a sound
# -----------------
#
# Finally, the underlying signal is stored in the ``signal`` attribute. The
# returned numpy array has 2 dimensions: ``(n_samples, n_channels)``. We can
# plot the signal of each channel.

samples_to_plot = 100  # number of samples to plot
times = sound.times[:samples_to_plot] * 1000  # ms

f, ax = plt.subplots(2, 1, sharex=True, sharey=True)
for k in range(2):  # 2 channels
    # draw data
    ax[k].plot(times, sound.signal[:samples_to_plot, k])
    # draw horizontal line through y=0
    ax[k].axhline(0, color="black")

# labels
ax[0].set_title("Right channel")
ax[1].set_title("Left channel")
ax[1].set_xlabel("Time (ms)")

# draw vertical line after each period
period = int(sound.sample_rate / sound.frequency)
for k in range(0, samples_to_plot, period):
    ax[0].axvline(times[k], color="lightgreen")
    ax[1].axvline(times[k], color="lightgreen")
