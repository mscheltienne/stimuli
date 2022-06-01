from itertools import product

import cv2
import numpy as np
import pytest

from .. import Text
from .test_base import _test_base


@pytest.mark.parametrize(
    "fontFace, fontScale, color, thickness, lineType, position",
    product(
        (cv2.FONT_HERSHEY_COMPLEX, cv2.FONT_HERSHEY_SIMPLEX),
        (2, 3),
        ("white", "teal", (101, 101, 101)),
        (2, 4),
        (cv2.LINE_AA, cv2.LINE_4, cv2.LINE_8),
        ("center", (100, 400)),
    ),
)
def test_text(fontFace, fontScale, color, thickness, lineType, position):
    """Test a text visual."""
    visual = Text(window_name="test", window_size=(500, 500))
    assert visual.window_name == "test"
    assert visual.window_size == (500, 500)
    assert visual._window_center == (250, 250)
    assert np.count_nonzero(visual.img) == 0
    visual.putText(
        "101", fontFace, fontScale, color, thickness, lineType, position
    )


def test_base():
    """Test base functionalities with a text visual."""
    _test_base(Text)


def test_invalid_arguments():
    """Test invalid arguments."""
    visual = Text(window_name="test", window_size=(500, 500))

    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putText(101)
    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putText("101", fontFace="arial")
    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putText("101", fontScale="large")
    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putText("101", color=101)
    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putText("101", thickness="large")
    with pytest.raises(TypeError, match="must be an instance of"):
        visual.putText("101", lineType="large")

    with pytest.raises(AssertionError):
        visual.putText("101", position=(10, 10, 10))
    with pytest.raises(AssertionError):
        visual.putText("101", position=(-10, 10))
    with pytest.raises(AssertionError):
        visual.putText("101", position=(1, 1))
    with pytest.raises(AssertionError):
        visual.putText("101", position=(499, 400))
