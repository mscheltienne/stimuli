from _typeshed import Incomplete

from ..utils._checks import check_type as check_type
from ..utils._checks import ensure_int as ensure_int
from ..utils._docs import fill_doc as fill_doc
from .base import BaseFeedbackVisual as BaseFeedbackVisual

class FillingBar(BaseFeedbackVisual):
    """Class to display a centered bar that can fill/unfill along a given axis.

    The filling process starts from the center of the bar and fills both sides
    simultaneously.

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
    _axis: Incomplete
    _margin: Incomplete
    _color: Incomplete
    _fill_color: Incomplete
    _fill_perc: Incomplete

    def putBar(
        self,
        length: int,
        width: int,
        margin: int,
        color: str | tuple[int, int, int],
        fill_color: str | tuple[int, int, int],
        fill_perc: float = 0,
        axis: int | str = 0,
    ) -> None:
        """Draw the bar on top of the current visual.

        Parameters
        ----------
        length : int
            Number of pixels used to draw the length of the bar.
        width : int
            Number of pixels used to draw the width of the bar.
        margin : int
            Margin in pixel between the filling bar and the containing bar.
            The containing bar ``(length x width)`` is set as
            ``(length+margin, width+margin)``.
        color : str | tuple
            Color used to draw the bar background.
        fill_color : str | tuple
            Color used to fill the bar.
        fill_perc : float
            Percentage between 0 and 1 of bar filling.

            * ``0``: not filled
            * ``1``: fully filled

            As the bar fills on both side simultaneously, the percentage filled
            is ``length//2 * fill_perc``.
        axis : int | str
            Axis along which the bar is moving:

            * ``0`` | ``'vertical'``   | ``'v'``  - vertical bar
            * ``1`` | ``'horizontal'`` | ``'h'``  - horizontal bar

        Notes
        -----
        A color is provided as matplotlib string or as ``(B, G, R)`` tuple of
        int8 set between 0 and 255.
        """

    def _putBar(self) -> None:
        """Draw the bar rectangle and fill rectangle.

        - Axis = 1 - Horizontal bar
        P1 ---------------
        |                |
        --------------- P2

        - Axis = 0 - Vertical bar
        P1 ---
        |    |
        |    |
        |    |
        |    |
        |    |
        --- P2
        """

    @staticmethod
    def _check_length_margin(
        length: int, margin: int, axis: int, window_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Check that the length and margin are valid."""

    @staticmethod
    def _check_width_margin(
        width: int, margin: int, length: int, axis: int, window_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Check that the width is valid."""

    @staticmethod
    def _check_fill_perc(fill_perc: float) -> float:
        """Check that the fill length is a percentage between 0 and 1."""

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
    def margin(self) -> int:
        """Margin in pixel between the bar and its filled content."""

    @margin.setter
    def margin(self, margin) -> None:
        """Margin in pixel between the bar and its filled content."""

    @property
    def color(self) -> tuple[int, int, int]:
        """Color used for the bar background in BGR color space."""

    @color.setter
    def color(self, color) -> None:
        """Color used for the bar background in BGR color space."""

    @property
    def fill_color(self) -> tuple[int, int, int]:
        """Color used to fill the bar in BGR color space."""

    @fill_color.setter
    def fill_color(self, fill_color) -> None:
        """Color used to fill the bar in BGR color space."""

    @property
    def fill_perc(self) -> float:
        """Length filled in percent between 0 and 1."""

    @fill_perc.setter
    def fill_perc(self, fill_perc) -> None:
        """Length filled in percent between 0 and 1."""

    @property
    def axis(self) -> int:
        """Axis on which the bar is moving.

        This property is a binary integer:
            - 0: Vertical bar filling along the vertical axis.
            - 1: Horizontal bar filling along the horizontal axis.
        """

    @axis.setter
    def axis(self, axis) -> None:
        """Axis on which the bar is moving.

        This property is a binary integer:
            - 0: Vertical bar filling along the vertical axis.
            - 1: Horizontal bar filling along the horizontal axis.
        """
