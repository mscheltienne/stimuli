from __future__ import annotations

import pytest
from numpy.testing import assert_allclose
from pynput.keyboard import Controller

from stimuli.keyboard import Keyboard, KeyEvent
from stimuli.time import sleep


@pytest.fixture(scope="module")
def controller() -> Controller:
    """Controller for keyboard, to simulate key press and release."""  # noqa: D401
    return Controller()


@pytest.mark.xfail(reason="Unreliable on CIs.")
def test_keyboard_basic(controller: Controller) -> None:
    """Test basic keyboard functionalities."""
    kb = Keyboard().start(suppress=True)
    assert isinstance(kb, Keyboard)
    controller.press("a")
    sleep(0.1)
    controller.release("a")
    keys = kb.get_keys()
    kb.stop()
    assert isinstance(keys, list)
    assert len(keys) == 1
    assert isinstance(keys[0], KeyEvent)
    assert keys[0].key == "a"
    assert keys[0].press_time is not None
    assert keys[0].release_time is not None
    assert_allclose(keys[0].release_time - keys[0].press_time, 0.1, atol=0.01)
    with pytest.warns(RuntimeWarning, match="keyboard is not running"):
        assert kb.get_keys() is None


@pytest.mark.xfail(reason="Unreliable on CIs.")
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
