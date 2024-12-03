from __future__ import annotations

from dataclasses import dataclass, field

from pynput.keyboard import Key, KeyCode


@dataclass
class KeyEvent:
    """Object representing a keyboard event.

    Parameters
    ----------
    key : str
        The string representation of the key.
    press_time : float | None
        The time at which the key was pressed in seconds.
    release_time : float | None
        The time at which the key was released in seconds.

    Notes
    -----
    The parameters are accessible as attributes of the object.

    The time reference is ``t0``, the instantiation time of the
    :class:`~stimuli.keyboard.Keyboard` object or the reset with
    :meth:`~stimuli.keyboard.Keyboard.reset`.
    """

    key: str
    press_time: float | None
    release_time: float | None


@dataclass
class KeyBuffer:
    """Object representing the buffer of keyboard events."""

    events: list[KeyEvent] = field(default_factory=list)
    pressed_keys: set[str] = field(default_factory=set)

    def clear(self) -> None:
        """Clear the buffer of keyboard events."""
        self.events.clear()
        self.pressed_keys.clear()

    def get(self) -> list[KeyEvent]:
        """Get the buffer of keyboard events."""
        events = self.events.copy()
        self.clear()
        return events


def _key_to_str(key) -> str:
    """Convert a key event to its string representation."""
    if isinstance(key, KeyCode) and key.char is not None:
        return key.char
    elif isinstance(key, Key):
        return key.name
    else:
        return str(key)
