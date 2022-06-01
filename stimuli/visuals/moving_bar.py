from copy import deepcopy
from typing import Optional, Tuple, Union

import cv2

from ..utils._checks import _check_type
from ..utils._docs import fill_doc
from .base import BaseFeedbackVisual


@fill_doc
class MovingBar(BaseFeedbackVisual):
    """Class to display a centered moving bar along an axis.

    Parameters
    ----------
    %(visual_window_name)s
    %(visual_window_size)s
    """

    def __init__(
        self,
        window_name: str = "Visual",
        window_size: Optional[Tuple[int, int]] = None,
    ):
        super().__init__(window_name, window_size)

    @fill_doc
    def putBar(
        self,
        length: int,
        width: int,
        color: Union[str, Tuple[int, int, int]],
        position: float = 0,
        axis: Union[int, str] = 0,
    ):
        """Draw the bar on top of the current visual.

        Parameters
        ----------
        %(visual_length)s
        %(visual_width)s
        color : str | tuple
            Color used to draw the bar. %(visual_color)s
        position : float
            Relative position of the bar along the given axis.
            Along the vertical axis:
                - -1: corresponds to the top of the window.
                - 1: corresponds to the bottom of the window.
            Along the horizontal axis:
                - -1: corresponds to the left of the window.
                - 1: corresponds to the right of the window.
            0 corresponds to the center of the window.
        axis : int | str
            Axis along which the bar is moving:
                - 0 | 'vertical' | 'v'
                    horizontal bar along vertical axis.
                - 1 | 'horizontal' | 'h'
                    vertical bar along horizontal axis.
        """
        if self._backup_img is None:
            self._backup_img = deepcopy(self._img)
        else:
            self._reset()

        self._position = MovingBar._check_position(position)
        self._axis = BaseFeedbackVisual._check_axis(axis)

        self._length = MovingBar._check_length(
            length, self._axis, self._window_size
        )
        self._width = MovingBar._check_width(
            width, self._length, self._axis, self._window_size
        )
        self._color = BaseFeedbackVisual._check_color(color)

        self._putBar()

    def _putBar(self):
        """Draw the bar rectangle.

        - Axis = 0 - Horizontal bar along vertical axis.
        P1 ---------------
        |                |
        --------------- P2

        - Axis = 1 - Vertical bar along horizontal axis
        P1 ---
        |    |
        |    |
        |    |
        |    |
        |    |
        --- P2
        """
        position = MovingBar._convert_position_to_pixel(
            self._position, self._axis, self._window_size, self.window_center
        )

        if self._axis == 0:
            xP1 = self.window_center[0] - self._length // 2
            yP1 = position - self._width // 2
            xP2 = xP1 + self._length
            yP2 = yP1 + self._width
        elif self._axis == 1:
            xP1 = position - self._width // 2
            yP1 = self.window_center[1] - self._length // 2
            xP2 = xP1 + self._width
            yP2 = yP1 + self._length

        cv2.rectangle(self._img, (xP1, yP1), (xP2, yP2), self._color, -1)

    # --------------------------------------------------------------------
    @staticmethod
    def _check_length(
        length: int, axis: int, window_size: Tuple[int, int]
    ) -> int:
        """Check that the length is valid."""
        _check_type(length, ("int",), "length")
        assert 0 < length
        assert length <= window_size[axis]
        return length

    @staticmethod
    def _check_width(
        width: int, length: int, axis: int, window_size: Tuple[int, int]
    ) -> int:
        """Check that the width is valid."""
        _check_type(width, ("int",), "width")
        assert 0 < width
        assert width <= length
        assert width <= window_size[(axis + 1) % 2]
        return width

    @staticmethod
    def _check_position(position: float) -> float:
        """Check that the position given is between -1 and 1."""
        _check_type(position, ("numeric",), "position")
        assert -1 <= position <= 1
        return position

    @staticmethod
    def _convert_position_to_pixel(
        position: float,
        axis: int,
        window_size: Tuple[int, int],
        window_center: Tuple[int, int],
    ) -> int:
        """Convert the position [-1, 1] to an absolute position in pixel."""
        idx = (axis + 1) % 2
        if position == 0:
            return window_center[idx]
        elif -1 <= position < 0:
            return int(window_center[idx] * (1 - abs(position)))
        elif 0 < position <= 1:
            return int(
                window_center[idx]
                + (window_size[idx] - window_center[idx]) * position
            )

    # --------------------------------------------------------------------
    @property
    def length(self) -> int:
        """Length of the bar in pixel."""
        return self._length

    @length.setter
    def length(self, length):
        self._length = MovingBar._check_length(
            length, self._axis, self._window_size
        )
        self._reset()
        self._putBar()

    @property
    def width(self) -> int:
        """Width of the bar in pixel."""
        return self._width

    @width.setter
    def width(self, width):
        self._width = MovingBar._check_width(
            width, self._length, self._axis, self._window_size
        )
        self._reset()
        self._putBar()

    @property
    def color(self) -> Tuple[int, int, int]:
        """Color of the bar in BGR color space."""
        return self._color

    @color.setter
    def color(self, color):
        self._color = BaseFeedbackVisual._check_color(color)
        self._reset()
        self._putBar()

    @property
    def position(self) -> float:
        """Position between -1 and 1 of the bar on the given axis."""
        return self._position

    @position.setter
    def position(self, position):
        self._position = MovingBar._check_position(position)
        self._reset()
        self._putBar()

    @property
    def axis(self):
        """Axis on which the bar is moving.

        This property is a binary integer:
            - 0: Horizontal bar along vertical axis.
            - 1: Vertical bar along horizontal axis.
        """
        return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = BaseFeedbackVisual._check_axis(axis)
        self._reset()
        self._putBar()
