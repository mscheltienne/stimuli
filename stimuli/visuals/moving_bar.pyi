from _typeshed import Incomplete

from ..utils._checks import check_type as check_type
from ..utils._checks import ensure_int as ensure_int
from ..utils._docs import fill_doc as fill_doc
from .base import BaseFeedbackVisual as BaseFeedbackVisual

class MovingBar(BaseFeedbackVisual):
    """Class to display a centered moving bar along an axis.

    Parameters
    ----------
    window_name : str
        Name of the window in which the visual is displayed.
    window_size : tuple | None
        Either ``None`` to automatically select a window size based on the
        available monitors, or a 2-length of positive integer sequence as
        ``(width, height)`` in pixels.
    """

    def __init__(
        self, window_name: str = "Visual", window_size: tuple[int, int] | None = None
    ) -> None: ...
    _backup_img: Incomplete
    _position: Incomplete
    _axis: Incomplete
    _length: Incomplete
    _width: Incomplete
    _color: Incomplete

    def putBar(
        self,
        length: int,
        width: int,
        color: str | tuple[int, int, int],
        position: float = 0,
        axis: int | str = 0,
    ):
        """Draw the bar on top of the current visual.

        Parameters
        ----------
        length : int
            Number of pixels used to draw the length of the bar.
        width : int
            Number of pixels used to draw the width of the bar.
        color : str | tuple
            Color used to draw the bar.
        position : float
            Relative position of the bar along the given axis.
            Along the vertical axis:

            * ``-1``: corresponds to the top of the window.
            * ``1``: corresponds to the bottom of the window.

            Along the horizontal axis:

            * ``-1``: corresponds to the left of the window.
            * ``1``: corresponds to the right of the window.

            ``0`` corresponds to the center of the window.
        axis : int | str
            Axis along which the bar is moving:

            * ``0`` | ``'vertical'``   | ``'v'``  - horizontal bar along
              vertical axis.
            * ``1`` | ``'horizontal'`` | ``'h'``  - vertical bar along
              horizontal axis.

        Notes
        -----
        A color is provided as matplotlib string or as ``(B, G, R)`` tuple of
        int8 set between 0 and 255.
        """

    def _putBar(self) -> None:
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

    @staticmethod
    def _check_length(length: int, axis: int, window_size: tuple[int, int]) -> int:
        """Check that the length is valid."""

    @staticmethod
    def _check_width(
        width: int, length: int, axis: int, window_size: [int, int]
    ) -> int:
        """Check that the width is valid."""

    @staticmethod
    def _check_position(position: float) -> float:
        """Check that the position given is between -1 and 1."""

    @staticmethod
    def _convert_position_to_pixel(
        position: float,
        axis: int,
        window_size: tuple[int, int],
        window_center: tuple[int, int],
    ) -> int:
        """Convert the position [-1, 1] to an absolute position in pixel."""

    @property
    def length(self) -> int:
        """Length of the bar in pixel."""

    @length.setter
    def length(self, length) -> None:
        """Length of the bar in pixel."""

    @property
    def width(self) -> int:
        """Width of the bar in pixel."""

    @width.setter
    def width(self, width) -> None:
        """Width of the bar in pixel."""

    @property
    def color(self) -> tuple[int, int, int]:
        """Color of the bar in BGR color space."""

    @color.setter
    def color(self, color) -> None:
        """Color of the bar in BGR color space."""

    @property
    def position(self) -> float:
        """Position between -1 and 1 of the bar on the given axis."""

    @position.setter
    def position(self, position) -> None:
        """Position between -1 and 1 of the bar on the given axis."""

    @property
    def axis(self):
        """Axis on which the bar is moving.

        This property is a binary integer:
            - 0: Horizontal bar along vertical axis.
            - 1: Vertical bar along horizontal axis.
        """

    @axis.setter
    def axis(self, axis) -> None:
        """Axis on which the bar is moving.

        This property is a binary integer:
            - 0: Horizontal bar along vertical axis.
            - 1: Vertical bar along horizontal axis.
        """
