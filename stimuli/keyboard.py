from __future__ import annotations

import threading
from copy import deepcopy
from typing import TYPE_CHECKING

from pynput.keyboard import Key, KeyCode, Listener

from .time import BaseClock, Clock
from .utils._checks import check_type
from .utils._docs import fill_doc
from .utils.logs import logger, warn

if TYPE_CHECKING:
    from collections.abc import Callable


@fill_doc
class Keyboard:
    """Object monitoring inputs on the keyboard.

    Parameters
    ----------
    keys: list of str | str | None
        The list of keys to monitor. If None, all keys will be monitored.
        Keys should be specified as strings, for instance
        ``['a', 'enter', 'space', 'shift_r']``.
    %(clock)s
    on_press : callable | None
        Additional callback function to call on a button press. The function should
        have the signature ``callback(key: KeyCode | Key | None)`` where key is ``None``
        if the key is unknown or :class:`~pynput.keyboard.KeyCode` or
        :class:`~pynput.keyboard.Key` otherwise.
    on_release : callable | None
        Additional callback function to call on a button release. The function should
        have the signature ``callback(key: KeyCode | Key | None)`` where key is ``None``
        if the key is unknown or :class:`~pynput.keyboard.KeyCode` or
        :class:`~pynput.keyboard.Key` otherwise.
    """

    def __init__(
        self,
        keys: str | list[str] | None = None,
        *,
        clock: BaseClock = Clock,
        on_press: Callable | None = None,
        on_release: Callable | None = None,
    ) -> None:
        check_type(keys, (list, str, None), "keys")
        if isinstance(keys, str):
            keys = [keys]
        elif keys is not None:
            for key in keys:
                check_type(key, (str,), "key")
        self._keys: list[str] | None = keys
        self._clock = clock()
        check_type(self._clock, (BaseClock,), "clock")
        check_type(on_press, (None, "callable"), "on_press")
        check_type(on_release, (None, "callable"), "on_release")
        self._on_press = on_press
        self._on_release = on_release
        # create an event buffer and a threading lock to modify the buffer
        self._buffer: list[dict[str, Key | KeyCode | None | float]] = []
        self._listener: Listener | None = None
        self._lock = threading.Lock()

    def __del__(self) -> None:
        """Make sure to stop the listener when the object is deleted."""
        if hasattr(self, "_listener") and self._listener is not None:
            self.stop()

    def __repr__(self) -> str:
        """Representation of the object."""
        if hasattr(self, "_listener"):
            status = "enabled" if self._listener else "disabled"
        else:
            status = "invalid"
        if self._keys is None:
            repr_ = f"< {self.__class__.__name__} ({status}) - monitor all keys >"
        else:
            repr_ = f"< {self.__class__.__name__} ({status}) - "
            if len(self._keys) <= 3:
                repr_ += f"monitor {', '.join(self._keys)} >"
            else:
                repr_ += f"monitor {len(self._keys)} keys >"
        return repr_

    def start(self, *, suppress: bool = False) -> None:
        """Start monitoring the keyboard.

        Parameters
        ----------
        suppress : bool
            If True, the events are not propagated to the system meaning that they will
            be only received by the :class:`~stimuli.keyboard.Keyboard` object and not
            by any other application or process.
        """
        if self._listener is None:
            self._listener = Listener(
                on_press=self._on_press_callback,
                on_release=self._on_release_callback,
                suppress=suppress,
            )
            self._listener.start()
        else:
            warn("The keyboard is already running.")

    def stop(self) -> None:
        """Stop monitoring the keyboard."""
        if self._listener is not None:
            with self._lock:
                self._listener.stop()
                self._listener = None
                self._buffer.clear()
        else:
            warn("The keyboard is not running.")

    def get_keys(self) -> list[dict[str, str | float | None]]:
        """Get a list of keys that were pressed since the last call."""
        with self._lock:
            keys = deepcopy(self._buffer)
            self._buffer.clear()
            return keys

    def wait_keys(self, *, timeout: float | None = None) -> bool:
        """Wait until a key is pressed.

        Parameters
        ----------
        timeout : float | None
            The maximum time to wait for a key press in seconds. If None, the function
            will wait indefinitely.

        Returns
        -------
        success : bool
            If True, a key was pressed before the timeout was reached. If False, no key
            was pressed before the timeout was reached.
        """
        t0 = self._clock.get_time_ns()
        n_keys = len(self._buffer)
        check_type(timeout, ("numeric", None), "timeout")
        if timeout is not None and timeout <= 0:
            raise ValueError(
                "The argument 'timeout' should be a strictly positive number. Provided "
                f"value '{timeout}' is invalid."
            )
        timeout = float("inf") if timeout is None else timeout * 1e9
        while self._clock.get_time_ns() - t0 < timeout:
            if n_keys < len(self._buffer):
                break
        else:
            warn("Timeout reached. No key was pressed.")
            return False
        return True

    def _on_press_callback(self, key) -> None:
        event = {
            "key": _key_to_str(key),
            "press_time": self._clock.get_time(),
            "release_time": None,
        }
        if self._keys is None or event["key"] in self._keys:
            logger.debug("Key pressed: %s", event["key"])
            with self._lock:
                self._buffer.append(event)
            if self._on_press is not None:  # call additional callback
                self._on_press(key)
        else:
            logger.debug("Key press ignored: %s", event["key"])

    def _on_release_callback(self, key) -> None:
        timestamp = self._clock.get_time()
        key_str = _key_to_str(key)
        if self._keys is None or key_str in self._keys:
            logger.debug("Key released: %s", key_str)
            with self._lock:
                for event in reversed(self._buffer):
                    if event["key"] == key_str and event["release_time"] is None:
                        event["release_time"] = timestamp
                        break
            if self._on_release is not None:  # call additional callback
                self._on_release(key)
        else:
            logger.debug("Key release ignored: %s", key_str)

    @property
    def t0(self) -> float:
        """The time of instantiation of the Keyboard in seconds.

        All timestamps of keyboard events are relative to this time.

        :type: :class:`float`
        """
        return self._clock.t0


def _key_to_str(key) -> str:
    """Convert a key event to its string representation."""
    if isinstance(key, KeyCode) and key.char is not None:
        return key.char
    elif isinstance(key, Key):
        return key.name
    else:
        return str(key)
