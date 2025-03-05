from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..utils._checks import check_type
from ..utils._docs import copy_doc
from ..utils._imports import import_optional_dependency
from ._base import BaseTrigger

if TYPE_CHECKING:
    from mne_lsl.lsl import StreamInfo, StreamOutlet


class LSLTrigger(BaseTrigger):
    """Trigger sending values on an LSL outlet.

    Make sure you are recording the stream created by the
    :class:`~stimuli.trigger.LSLTrigger` alongside your data. e.g. if you use
    LabRecorder, update the stream list after creating the
    :class:`~stimuli.trigger.LSLTrigger`.

    .. warning::

        Make sure to close the :class:`~mne_lsl.lsl.StreamOutlet` by calling the
        :meth:`~stimuli.trigger.LSLTrigger.close` method or by deleting the trigger
        after use.

    Parameters
    ----------
    name : str
        Name of the trigger displayed on the LSL network.

    Notes
    -----
    The :class:`~mne_lsl.lsl.StreamOutlet` created has the following properties:

    * Name: ``f"{name}"``
    * Type: ``"Markers"``
    * Number of channels: 1
    * Sampling rate: Irregular
    * Data type: ``np.int8``
    * Source ID: ``f"HNP-{name}"``

    The values sent must be in the range of strictly positive integers defined
    by ``np.int8``, 1 to 127 included.
    """

    def __init__(self, name: str) -> None:
        import_optional_dependency("mne_lsl")

        from mne_lsl.lsl import StreamInfo, StreamOutlet

        check_type(name, (str,), "name")
        self._name = name
        # create outlet
        self._sinfo = StreamInfo(
            name=name,
            stype="Markers",
            n_channels=1,
            sfreq=0.0,
            dtype="int8",
            source_id=f"HNP-{name}",
        )
        self._sinfo.set_channel_names(["STI"])
        self._sinfo.set_channel_types(["stim"])
        self._sinfo.set_channel_units(["none"])
        self._outlet = StreamOutlet(self._sinfo, max_buffered=1)

    @copy_doc(BaseTrigger.signal)
    def signal(self, value: int) -> None:
        value = super().signal(value)
        if not (1 <= value <= 127):
            raise ValueError(
                "The argument 'value' of an LSL trigger must be an integer "
                "between 1 and 127 included."
            )
        self._outlet.push_sample(np.array([value], dtype=np.int8))

    def close(self) -> None:
        """Close the LSL outlet."""
        if hasattr(self, "_outlet"):
            try:
                del self._outlet
            except Exception:  # pragma: no cover
                pass

    def __del__(self) -> None:  # noqa: D105
        self.close()

    # --------------------------------------------------------------------
    @property
    def name(self) -> str:
        """Name of the trigger displayed on the LSL network.

        :type: str
        """
        return self._name

    @property
    def sinfo(self) -> StreamInfo:
        """Description of the trigger outlet.

        :type: `~mne_lsl.lsl.StreamInfo`
        """
        return self._sinfo

    @property
    def outlet(self) -> StreamOutlet:
        """Trigger outlet.

        :type: `~mne_lsl.lsl.StreamOutlet`
        """
        return self._outlet
