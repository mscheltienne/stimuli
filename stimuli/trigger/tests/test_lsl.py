from __future__ import annotations

import numpy as np
import pytest


def test_trigger_lsl() -> None:
    """Testing for LSL trigger."""
    pytest.importorskip("mne_lsl")

    from mne_lsl.lsl import StreamInfo, StreamInlet, StreamOutlet, resolve_streams

    from stimuli.trigger import LSLTrigger

    name = "test-trigger-lsl"
    trigger = LSLTrigger(name)
    assert trigger.name == name
    streams = resolve_streams(name=name)
    assert len(streams) == 1
    sinfo = streams[0]
    del streams
    inlet = StreamInlet(sinfo)
    inlet.open_stream()
    assert inlet.samples_available == 0
    sinfo = inlet.get_sinfo()
    assert sinfo.get_channel_names() == ["STI"]
    assert sinfo.get_channel_types() == ["stim"]
    assert sinfo.get_channel_units() == ["none"]
    trigger.signal(1)
    data, ts = inlet.pull_sample(timeout=10)
    assert data.dtype == np.int8
    assert data.size == 1
    assert data[0] == 1
    assert ts is not None
    trigger.signal(127)
    data, ts = inlet.pull_sample(timeout=10)
    assert data.dtype == np.int8
    assert data.size == 1
    assert data[0] == 127
    assert ts is not None
    with pytest.raises(ValueError, match="between 1 and 127 included"):
        trigger.signal(255)
    assert isinstance(trigger.outlet, StreamOutlet)
    assert isinstance(trigger.sinfo, StreamInfo)
