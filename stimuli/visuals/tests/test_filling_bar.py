from itertools import product

import numpy as np
import pytest

from .. import FillingBar
from .test_base import _test_base


@pytest.mark.parametrize(
    "length, width, margin, color, fill_color, fill_perc, axis",
    product(
        (100, 200),
        (10, 20),
        (2, 4),
        ("white", (101, 101, 101)),
        ("teal", (201, 201, 201)),
        (0, 0.4, 0.8, 1),
        (0, 1, "v", "h"),
    ),
)
def test_filling_bar(
    length, width, margin, color, fill_color, fill_perc, axis
):
    """Test a filling bar visual."""
    visual = FillingBar(window_name="test", window_size=(500, 500))
    assert visual.window_name == "test"
    assert visual.window_size == (500, 500)
    assert visual._window_center == (250, 250)
    assert np.count_nonzero(visual.img) == 0
    visual.putBar(length, width, margin, color, fill_color, fill_perc, axis)


def test_filling_bar_setters():
    """Test property setters."""
    visual = FillingBar(window_name="test", window_size=(500, 500))
    visual.putBar(100, 20, 2, "white", (101, 101, 101), 0, 0)

    assert visual.fill_perc == 0
    visual.fill_perc = 0.5
    assert visual.fill_perc == 0.5

    assert visual.color == (255, 255, 255)
    visual.color = (210, 210, 210)
    assert visual.color == (210, 210, 210)

    assert visual.fill_color == (101, 101, 101)
    visual.fill_color = (201, 201, 201)
    assert visual.fill_color == (201, 201, 201)

    assert visual.length == 100
    visual.length = 200
    assert visual.length == 200

    assert visual.width == 20
    visual.width = 30
    assert visual.width == 30

    assert visual.margin == 2
    visual.margin = 5
    assert visual.margin == 5


def test_base():
    """Test base functionalities with a filling bar visual."""
    _test_base(FillingBar)


def test_invalid_arguments():
    """Test invalid arguments."""
    visual = FillingBar(window_name="test", window_size=(500, 500))

    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putBar("long", 20, 3, "white", "teal", 0.5, 0)
    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putBar(100, "long", 3, "white", "teal", 0.5, 0)
    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putBar(100, 20, "small", "white", "teal", 0.5, 0)

    with pytest.raises(AssertionError):
        visual.putBar(-100, 20, 3, "white", "teal", 0.5, 0)
    with pytest.raises(AssertionError):
        visual.putBar(100, -20, 3, "white", "teal", 0.5, 0)
    with pytest.raises(AssertionError):
        visual.putBar(100, 20, -3, "white", "teal", 0.5, 0)
    with pytest.raises(AssertionError):
        visual.putBar(100, 20, 3, "white", "teal", -0.5, 0)
    with pytest.raises(AssertionError):
        visual.putBar(100, 20, 3, "white", "teal", 50, 0)
    with pytest.raises(AssertionError):
        visual.putBar(100, 20, 40, "white", "teal", 0.5, 0)
    with pytest.raises(AssertionError):
        visual.putBar(100, 200, 40, "white", "teal", 0.5, 0)
