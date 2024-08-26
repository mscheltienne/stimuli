from itertools import product

import numpy as np
import pytest

from .. import Cross
from .test_base import _test_base


@pytest.mark.parametrize(
    ("length", "thickness", "color", "position"),
    product(
        (100, 20),
        (5, 10),
        ("white", "teal", (101, 101, 101)),
        ("center", (100, 400)),
    ),
)
def test_cross(length, thickness, color, position):
    """Test a cross visual."""
    visual = Cross(window_name="test", window_size=(500, 500))
    assert visual.window_name == "test"
    assert visual.window_size == (500, 500)
    assert visual._window_center == (250, 250)
    assert np.count_nonzero(visual.img) == 0
    visual.putCross(length, thickness, color, position)


def test_base():
    """Test base functionalities with a cross visual."""
    _test_base(Cross)


def test_invalid_arguments():
    """Test invalid arguments."""
    visual = Cross(window_name="test", window_size=(500, 500))

    with pytest.raises(TypeError, match="must be an integer"):
        visual.putCross(length="long", thickness=10, color="white")
    with pytest.raises(TypeError, match="must be an integer"):
        visual.putCross(length=100, thickness="large", color="white")

    with pytest.raises(AssertionError):
        visual.putCross(length=-100, thickness=10, color="white")
    with pytest.raises(AssertionError):
        visual.putCross(length=100, thickness=-10, color="white")
    with pytest.raises(AssertionError):
        visual.putCross(length=10000, thickness=20, color="white")
    with pytest.raises(AssertionError):
        visual.putCross(length=100, thickness=200, color="white")
    with pytest.raises(AssertionError):
        visual.putCross(length=100, thickness=10, color="white", position=(10, 10, 10))
    with pytest.raises(AssertionError):
        visual.putCross(length=100, thickness=10, color="white", position=(-10, 10))
    with pytest.raises(AssertionError):
        visual.putCross(length=100, thickness=10, color="white", position=(1, 1))
    with pytest.raises(AssertionError):
        visual.putCross(length=100, thickness=10, color="white", position=(499, 250))
