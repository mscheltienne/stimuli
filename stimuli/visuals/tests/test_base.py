import numpy as np
import pytest

from stimuli.visuals import BaseFeedbackVisual, BaseVisual


def test_check_window_size():
    """Check the window size static checker."""
    winsize = BaseVisual._check_window_size((100, 20))
    assert winsize == (100, 20)

    with pytest.raises(TypeError, match="must be an instance of"):
        BaseVisual._check_window_size([100, 20])
    with pytest.raises(AssertionError):
        BaseVisual._check_window_size((100, 20, 101))
    with pytest.raises(AssertionError):
        BaseVisual._check_window_size((100, -20))


def test_check_color():
    """Check the color static checker."""
    color = BaseVisual._check_color("teal")
    assert isinstance(color, tuple)
    assert len(color) == 3
    assert all(isinstance(c, int) for c in color)
    assert all(0 <= c <= 255 for c in color)

    color = BaseVisual._check_color((100, 20, 101))
    assert color == (100, 20, 101)

    with pytest.raises(TypeError, match="must be an instance of"):
        BaseVisual._check_color([100, 20, 101])
    with pytest.raises(AssertionError):
        BaseVisual._check_color((100, 101))
    with pytest.raises(AssertionError):
        BaseVisual._check_color((101, -101, 101))


def test_check_axis():
    """Check the axis static checker."""
    for axis in (0, "vertical", "v"):
        ax = BaseFeedbackVisual._check_axis(axis)
        assert ax == 0
    for axis in (1, "horizontal", "h"):
        ax = BaseFeedbackVisual._check_axis(axis)
        assert ax == 1

    with pytest.raises(TypeError, match="must be an instance of"):
        BaseFeedbackVisual._check_axis([0])
    with pytest.raises(TypeError, match="must be an instance of"):
        BaseFeedbackVisual._check_axis(True)
    with pytest.raises(AssertionError):
        BaseFeedbackVisual._check_axis("101")


def _test_base(Visual):
    """Test base functionalities with a Visual class."""
    visual = Visual(window_size=(100, 50))
    visual.show()
    visual.close()
    assert np.all(visual.img == 0)
    visual.draw_background(color=(101, 101, 101))
    assert np.all(visual.img == 101)
    assert visual.window_name == "Visual"
    assert visual.window_size == (100, 50)
    assert visual._window_width == 100
    assert visual._window_height == 50
    assert visual.window_center == (50, 25)
    visual.background = (50, 50, 50)
    assert np.all(visual.img == 50)
