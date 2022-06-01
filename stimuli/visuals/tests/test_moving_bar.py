from itertools import product

import numpy as np
import pytest

from .. import MovingBar
from .test_base import _test_base


@pytest.mark.parametrize(
    "length, width, color, position, axis",
    product(
        (100, 200),
        (10, 20),
        ("white", (101, 101, 101)),
        (-1, -0.5, 0, 0.5, 1),
        (0, 1, "v", "h"),
    ),
)
def test_moving_bar(length, width, color, position, axis):
    """Test a moving bar visual."""
    visual = MovingBar(window_name="test", window_size=(500, 500))
    assert visual.window_name == "test"
    assert visual.window_size == (500, 500)
    assert visual._window_center == (250, 250)
    assert np.count_nonzero(visual.img) == 0
    visual.putBar(length, width, color, position, axis)
    visual.show()
    visual.close()


def test_moving_bar_setters():
    """Test property setters."""
    visual = MovingBar(window_name="test", window_size=(500, 500))
    visual.putBar(100, 20, "white", 0, 0)

    assert visual.position == 0
    visual.position = 0.5
    assert visual.position == 0.5

    assert visual.color == (255, 255, 255)
    visual.color = (210, 210, 210)
    assert visual.color == (210, 210, 210)

    assert visual.length == 100
    visual.length = 200
    assert visual.length == 200

    assert visual.width == 20
    visual.width = 30
    assert visual.width == 30

    assert visual.axis == 0
    visual.axis = 1
    assert visual.axis == 1


def test_base():
    """Test base functionalities with a moving bar visual."""
    _test_base(MovingBar)


def test_invalid_arguments():
    """Test invalid arguments."""
    visual = MovingBar(window_name="test", window_size=(500, 500))

    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putBar("long", 20, "white", 0, 0)
    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putBar(100, "long", "white", 0, 0)
    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putBar(100, 20, "white", "center", 0)

    with pytest.raises(AssertionError):
        visual.putBar(-100, 20, "white", 0, 0)
    with pytest.raises(AssertionError):
        visual.putBar(100, -20, "white", 0, 0)
    with pytest.raises(AssertionError):
        visual.putBar(100, 20, "white", 10, 0)
