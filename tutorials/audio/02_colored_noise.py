"""
Colored noise
-------------

A noise signal is produced by a stocahstic process. The color of noise, also
called the noise spectrum, refers to the power spectrum of a noise signal.

The practice of naming kinds of noise after colors started with white noise,
a signal whose spectrum has equal power within any equal interval of
frequencies. That name was given by analogy with white light, which was
(incorrectly) assumed to have such a flat power spectrum over the visible
range. Other color names, such as ``pink``, ``red``, and ``blue`` were then
given to noise with other spectral profiles, often (but not always) in
reference to the color of light with similar spectra. Some of those names
have standard definitions in certain disciplines, while others are very
informal and poorly defined.

Source: `Wikipedia <https://en.wikipedia.org/wiki/Colors_of_noise>`_
"""

#%%

import numpy as np
from matplotlib import pyplot as plt

from stimuli.audio import Noise

#%%
# In this tutorial, we will create and plot the power spectrum of different
# noise colors. ``simple-stimuli`` implements several noise color in
# :class:`stimuli.audio.Noise`. Refer to the documentation of the ``color``
# argument for available colors.

colors = ("white", "pink", "blue", "violet", "brown")
sounds = dict()
for color in colors:
    # identical volume on all audio channels
    sounds[color] = Noise(volume=10, color=color)

#%%
# We can listen to each individual noise by playing each sound with
# :meth:`stimuli.audio.Noise.play`.

for sound in sounds.values():
    sound.play(blocking=True)

#%%
# The underlying signal is stored in the ``signal`` attribute. The returned
# numpy array has 2 dimensions: ``(n_samples, n_channels)``. As the volume has
# been set identicaly on all audio channels, we can disregard the second
# dimension and select only the first channel.

plt.figure(figsize=(10, 10))
for color in colors:
    signal = sounds[color].signal[:, 0]  # retrieve the signal
    # compute the one-dimensional discrete fourier transform
    frequencies = np.fft.rfftfreq(signal.size)
    dft = np.abs(np.fft.rfft(signal))
    # plot with log scaling on both X and Y axis
    plt.loglog(frequencies, dft)
plt.legend(colors)
plt.ylim([1e-3, None])
