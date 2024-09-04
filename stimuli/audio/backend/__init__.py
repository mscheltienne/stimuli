from __future__ import annotations

from typing import TYPE_CHECKING

from . import sounddevice
from .sounddevice import SoundSD

if TYPE_CHECKING:
    from ._base import BaseBackend

BACKENDS: dict[str, BaseBackend] = {"sounddevice": SoundSD}
