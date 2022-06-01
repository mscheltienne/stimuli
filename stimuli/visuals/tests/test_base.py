import pytest
import screeninfo

from stimuli.visuals import BaseFeedbackVisual, BaseVisual


def test_check_window_size():
    """Check the window size static checker."""
    winsize = BaseVisual._check_window_size((100, 20))
    assert winsize == (100, 20)
    if len(screeninfo.get_monitors()) == 0:
        with pytest.raises(ValueError):
            BaseVisual._check_window_size(None)
    else:
        winsize = BaseVisual._check_window_size(None)
        assert isinstance(winsize, tuple)
        assert len(winsize) == 2
        assert all(isinstance(elt, int) for elt in winsize)
        assert all(0 < elt for elt in winsize)

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
