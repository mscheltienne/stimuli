"""
=============================
Synchronize sound and trigger
=============================

Often, a trigger must be emitted simultenously with a sound onset, with as little delay
and jitter as possible. With ``stimuli``, similarly to ``psychtoolbox``, the key concept
is to schedule the sound.

First, let's have a look at our default device latency.
"""

# sphinx_gallery_thumbnail_path = '_static/performance.png'

import sounddevice as sd

from stimuli.audio import SoundAM
from stimuli.time import sleep
from stimuli.trigger import MockTrigger

idx = sd.default.device["output"]
print(f"Low-latency (s): {sd.query_devices()[idx]['default_low_output_latency']}")

# %%
# Next, we can schedule a sound with the argument ``when`` which will use the clock
# provided in the argument ``clock`` to schedule the sound. Then, we wait for this
# duration to elapse before sending the trigger.

trigger = MockTrigger()  # replace with your trigger object
sound = SoundAM(
    frequency_carrier=1000,
    frequency_modulation=40,
    method="dsbsc",
    volume=10,
    duration=1,
)
sound.play(when=0.5, blocking=False)
sleep(0.5)
trigger.signal(1)

# %%
# A quick measurement on a dual-boot Windows/Linux computer connected to a USB Crimson 3
# soundcard shows that the delay and jitter of ``stimuli`` are similar to
# ``psychtoolbox`` on linux.
#
# .. image:: ../../_static/performance.png
#    :align: center
#
# On different computers with different soundcards, the performance may vary. For
# instance, with on-board soundcards on Linux, both psychtoolbox and stimuli are usually
# perfectly synchronized with the trigger. In the end, the performance should always be
# measured on the target system.
#
# .. code-block:: python
#
#     from stimuli.audio import Tone
#     from stimuli.time import sleep
#     from stimuli.trigger import ParallelPortTrigger
#
#     sound = Tone(frequency=440, volume=100, duration=0.3)
#     trigger = ParallelPortTrigger("/dev/parport0")
#
#     for k in range(10):
#         sound.play(when=0.2)
#         sleep(0.2)
#         trigger.signal(1)
#         sleep(0.5)
