from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pynput.keyboard import Key, KeyCode, Listener

from .time import BaseClock, Clock
from .utils._checks import check_type
from .utils._docs import fill_doc
from .utils.logs import logger, warn

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass
class KeyEvent:
    """Object representing a keyboard event.

    Attributes
    ----------
    key : str
        The string representation of the key.
    press_time : float | None
        The time at which the key was pressed in seconds.
    release_time : float | None
        The time at which the key was released in seconds.

    Notes
    -----
    The time reference is ``t0``, the instantation time of the
    :class:`~stimuli.keyboard.Keyboard` object or the last clock reset with
    :meth:`~stimuli.keyboard.Keyboard.reset_clock`.
    """

    key: str
    press_time: float | None
    release_time: float | None


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
        self._buffer: list[KeyEvent] = []
        self._listener: Listener | None = None
        self._lock = threading.Lock()
        # create the threading event for wait_keys
        self._wait_event = threading.Event()
        self._wait_result = None

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
            logger.info("Keyboard monitoring started.")
        else:
            warn("The keyboard is already running.")

    def stop(self) -> None:
        """Stop monitoring the keyboard."""
        if self._listener is not None:
            with self._lock:
                self._listener.stop()
                self._listener = None
                self._buffer.clear()
            logger.info("Keyboard monitoring stopped.")
        else:
            warn("The keyboard is not running.")

    def get_keys(self) -> list[KeyEvent]:
        """Get a list of keys that were pressed since the last call."""
        with self._lock:
            keys = self._buffer.copy()
            self._buffer.clear()
            return keys

    def wait_keys(self, *, timeout: float | None = None) -> str | None:
        """Wait until a key is pressed.

        Parameters
        ----------
        timeout : float | None
            The maximum time to wait for a key press in seconds. If None, the function
            will wait indefinitely.

        Returns
        -------
        key : str | None
            The key that was pressed or None if the timeout was reached.
        """
        check_type(timeout, ("numeric", None), "timeout")
        if timeout is not None and timeout <= 0:
            raise ValueError(
                "The argument 'timeout' should be a strictly positive number. Provided "
                f"value '{timeout}' is invalid."
            )
        with self._lock:
            self._wait_event.clear()
            self._wait_result = None
        is_set = self._wait_event.wait(timeout)
        with self._lock:
            if is_set:
                return self._wait_result
        warn("Timeout reached. No key was pressed.")

    def _on_press_callback(self, key) -> None:
        """Callback function called on key press."""  # noqa: D401
        try:
            key_str = _key_to_str(key)
            event = KeyEvent(key_str, self._clock.get_time(), None)
            if self._keys is None or key_str in self._keys:
                logger.debug("Key pressed: %s", key_str)
                with self._lock:
                    self._buffer.append(event)
                    self._wait_result = key_str
                    self._wait_event.set()
                if self._on_press is not None:  # call additional callback
                    self._on_press(key)
            else:
                logger.debug("Key press ignored: %s", event.key)
        except Exception as error:
            logger.error(
                "An error occurred while processing a key press event.\n\n%s", error
            )

    def _on_release_callback(self, key) -> None:
        """Callback function called on key release."""  # noqa: D401
        try:
            timestamp = self._clock.get_time()
            key_str = _key_to_str(key)
            if self._keys is None or key_str in self._keys:
                logger.debug("Key released: %s", key_str)
                with self._lock:
                    for event in reversed(self._buffer):
                        if event.key == key_str and event.release_time is None:
                            event.release_time = timestamp
                            break
                    else:
                        warn(
                            "No matching key press event found for key release: "
                            f"{key_str}."
                        )
                        self._buffer.append(KeyEvent(key_str, None, timestamp))
                if self._on_release is not None:  # call additional callback
                    self._on_release(key)
            else:
                logger.debug("Key release ignored: %s", key_str)
        except Exception as error:
            logger.error(
                "An error occurred while processing a key release event.\n\n%s", error
            )

    def reset_clock(self) -> None:
        """Reset the clock of the Keyboard."""
        self._clock.reset()

    def reset_buffer(self) -> None:
        """Reset the buffer of the Keyboard."""
        with self._lock:
            self._buffer.clear()

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
