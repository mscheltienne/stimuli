import pytest
from pynput.keyboard import Key, KeyCode

from stimuli.keyboard._utils import KeyBuffer, KeyEvent, _key_to_str


def test_key_to_str():
    """Test the conversion of key events to strings."""
    assert _key_to_str(Key.space) == "space"
    assert _key_to_str(Key.enter) == "enter"
    assert _key_to_str(101) == "101"
    assert _key_to_str(KeyCode.from_char("o")) == "o"


def test_KeyEvent():
    """Test the key event object."""
    event = KeyEvent("a", 0.1, 0.2)
    assert event.key == "a"
    assert event.press_time == 0.1
    assert event.release_time == 0.2


@pytest.fixture
def event() -> KeyEvent:
    """Return a key event."""
    return KeyEvent("a", 0.1, 0.2)


def test_KeyBuffer(event: KeyEvent):
    """Test the key buffer object."""
    buffer = KeyBuffer()
    assert buffer.events == []
    buffer.events.append(event)
    buffer.pressed_keys.add(event.key)
    assert buffer.events == [event]
    assert buffer.pressed_keys == {event.key}

    buffer.clear()
    assert buffer.events == []
    assert buffer.pressed_keys == set()


def test_KeyBuffer_get(event: KeyEvent):
    """Test the get method from a key buffer."""
    buffer = KeyBuffer()
    buffer.events.append(event)
    buffer.pressed_keys.add(event.key)
    assert buffer.pressed_keys == {"a"}
    assert buffer.events == [event]
    assert buffer.get() == [event]
    assert buffer.events == []
    assert buffer.pressed_keys == set()


def test_KeyBuffer_clear(event: KeyEvent):
    """Test the clear method from a key buffer."""
    buffer = KeyBuffer()
    buffer.events.append(event)
    buffer.pressed_keys.add(event.key)
    assert buffer.pressed_keys == {event.key}
    assert buffer.events == [event]
    buffer.clear()
    assert buffer.events == []
    assert buffer.pressed_keys == set()
