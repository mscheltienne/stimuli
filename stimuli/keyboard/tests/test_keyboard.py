from __future__ import annotations

import os

import pytest
from numpy.testing import assert_allclose
from pynput.keyboard import KeyCode

from stimuli.keyboard import Keyboard, KeyEvent
from stimuli.time import sleep


def _fake_key_press(keyboard: Keyboard, key: str) -> None:
    """Fake a key press."""
    keyboard._on_press_callback(KeyCode.from_char(key))


def _fake_key_release(keyboard: Keyboard, key: str) -> None:
    """Fake a key release."""
    keyboard._on_release_callback(KeyCode.from_char(key))


def _get_keys(keyboard: Keyboard) -> list[KeyEvent]:
    """Get the list of keys in the buffer."""
    with keyboard._lock:
        keys = keyboard._buffer.get()
    return keys


def test_keyboard_basic() -> None:
    """Test basic keyboard functionalities."""
    kb = Keyboard()
    assert isinstance(kb, Keyboard)
    _fake_key_press(kb, "a")
    sleep(0.1)
    _fake_key_release(kb, "a")
    keys = _get_keys(kb)
    assert isinstance(keys, list)
    assert len(keys) == 1
    assert isinstance(keys[0], KeyEvent)
    assert keys[0].key == "a"
    assert keys[0].press_time is not None
    assert keys[0].release_time is not None
    assert_allclose(keys[0].release_time - keys[0].press_time, 0.1, atol=0.01)


def test_keyboard_not_monitoring() -> None:
    """Test keyboard not monitoring."""
    kb = Keyboard()
    with pytest.warns(RuntimeWarning, match="keyboard is not running"):
        assert kb.get_keys() is None

    with pytest.warns(RuntimeWarning, match="keyboard is not running"):
        kb.stop()


def test_keyboard_key_restriction() -> None:
    """Test monitoring specific keys."""
    kb = Keyboard(keys="b")
    assert isinstance(kb, Keyboard)
    _fake_key_press(kb, "a")
    sleep(0.1)
    _fake_key_press(kb, "b")
    sleep(0.1)
    _fake_key_release(kb, "b")
    sleep(0.1)
    _fake_key_release(kb, "a")
    keys = _get_keys(kb)
    assert len(keys) == 1
    assert keys[0].key == "b"


def test_keyboard_reset() -> None:
    """Test keyboard reset."""
    kb = Keyboard()
    _fake_key_press(kb, "a")
    sleep(0.1)
    _fake_key_release(kb, "a")
    t0 = kb.t0
    assert 0 < t0
    kb.reset()
    keys = _get_keys(kb)
    assert len(keys) == 0
    assert t0 < kb.t0


@pytest.mark.xfail(
    os.getenv("GITHUB_ACTIONS", "") == "true", reason="Unreliable on CIs."
)
def test_keyboard_repr() -> None:
    """Test keyboard representation."""
    kb = Keyboard()
    assert repr(kb) == "<Keyboard (disabled) - monitor all keys>"
    kb.start()
    assert repr(kb) == "<Keyboard (enabled) - monitor all keys>"
    kb.stop()

    kb = Keyboard(keys=["a", "b", "c"])
    assert repr(kb) == "<Keyboard (disabled) - monitor a, b, c>"
    kb.start()
    assert repr(kb) == "<Keyboard (enabled) - monitor a, b, c>"
    kb.stop()

    kb = Keyboard(keys=["a", "b", "c", "d"])
    assert repr(kb) == "<Keyboard (disabled) - monitor 4 keys>"
    kb.start()
    assert repr(kb) == "<Keyboard (enabled) - monitor 4 keys>"
    kb.stop()
