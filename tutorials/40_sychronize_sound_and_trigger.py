"""
=============================
Synchronize sound and trigger
=============================

Often, a trigger must be emitted simultenously with a sound onset, with as little delay
and jitter as possible. With ``stimuli``, similarly to ``psychtoolbox``, the key concept
is to schedule the sound.

First, let's have a look at our default device latency.
"""

import sounddevice as sd

from stimuli.audio import SoundAM
from stimuli.time import sleep
from stimuli.triggers import MockTrigger

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
