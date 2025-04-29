"""
==============
Apply a window
==============

.. include:: ../../links.inc

In signal processing and statistics, a window function (also known as an
apodization function or tapering function) is a mathematical function that is
zero-valued outside of some chosen interval, normally symmetric around the
middle of the interval, usually near a maximum in the middle, and usually
tapering away from the middle. Mathematically, when another function or
waveform/data-sequence is "multiplied" by a window function, the product is
also zero-valued outside the interval: all that is left is the part where they
overlap, the "view through the window".

Source: `Wikipedia <https://en.wikipedia.org/wiki/Window_function>`_

A sound waveform might have an abrupt onset or offset. It is often preferred to
apply a window to ramp up and ramp down the volume.
"""

# %%

# sphinx_gallery_thumbnail_number = 3

import numpy as np
from matplotlib import pyplot as plt
from scipy.signal.windows import tukey

from stimuli.audio import Tone

# %%
#
# In this tutorial, we will create a pure tone auditory stimuli and apply a
# window with a linear ramp-up and a linear ramp-down to smooth the onset and
# offset.

# %%
# Create a pure tone
# ------------------
#
# To create the stimuli, we create a :class:`~stimuli.audio.Tone` object with
# a given volume and frequency.

sound = Tone(frequency=200, volume=10, duration=0.1)

# %%
# By default, a generated signal will have a rectangular window applied. A
# recctangular window is equal to 0 outside of the signal definition range, and
# to 1 inside. We can plot the waveform of one of the channels:

# draw the waveform
_, ax = sound.plot()
ax.set_title("Waveform - Rectangular window")

# overlay a rectangular window
# note: for demonstration purposes, we make the window 20% longer than the
# signal by extending it by 10% before and after the signal.
extension = int(0.1 * sound.times.size)
window = np.zeros(extension + sound.times.size + extension)
window[extension + 1 : extension + sound.times.size] = 1 / sound.volume
# determine the timestamps associated to each sample in the window (ms)
window_times = np.arange(0, 1 / sound.sample_rate * window.size, 1 / sound.sample_rate)
window_times -= extension / sound.sample_rate
# draw the window
ax.plot(window_times, window, color="crimson")
plt.show()

# %%
# Create a different window
# -------------------------
#
# For this tutorial, we will define a window with a ramp from ``0`` to ``1``
# during the first 10% of the total duration, and a ramp from ``1`` to ``0``
# during the last 10% of the total duration. A correctly defined window is a
# 1D `~numpy.array` with the same number of samples as the sound.

window = np.ones(sound.times.size)
n_samples_ramp = int(0.1 * sound.times.size)
ramp = np.linspace(start=0, stop=1, num=n_samples_ramp)
window[:n_samples_ramp] = ramp
window[-n_samples_ramp:] = ramp[::-1]

# %%
# Change the window
# -----------------
#
# We can change the applied window by setting the property ``window``.

sound.window = window

# draw the modified sound and the window
_, ax = sound.plot()
ax.set_title("Waveform - Ramp onset/offset window")
ax.plot(sound.times, window / sound.volume, color="crimson")  # overlay the window
plt.show()

# %%
# Scipy windows
# -------------
#
# `scipy`_ has many windows implemented in :mod:`scipy.signal.windows`. For instance
# we can use a Tukey window with the function `~scipy.signal.windows.tukey`.

window = tukey(sound.times.size)
sound.window = window

# draw the modified sound and the window
_, ax = sound.plot()
ax.set_title("Waveform - Tukey window")
ax.plot(sound.times, window / sound.volume, color="crimson")  # overlay the window
plt.show()
