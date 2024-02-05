from copy import deepcopy

import cv2

from ..utils._checks import check_type, ensure_int
from ..utils._docs import fill_doc
from .base import BaseFeedbackVisual


@fill_doc
class FillingBar(BaseFeedbackVisual):
    """Class to display a centered bar that can fill/unfill along a given axis.

    The filling process starts from the center of the bar and fills both sides
    simultaneously.

    Parameters
    ----------
    %(visual_window_name)s
    %(visual_window_size)s
    """

    def __init__(
        self,
        window_name: str = "Visual",
        window_size: tuple[int, int] | None = None,
    ):
        super().__init__(window_name, window_size)

    @fill_doc
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
        %(visual_length)s
        %(visual_width)s
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
        %(visual_color)s
        """
        if self._backup_img is None:
            self._backup_img = deepcopy(self._img)
        else:
            self._reset()

        self._axis = BaseFeedbackVisual._check_axis(axis)
        self._length, margin = FillingBar._check_length_margin(
            length, margin, self._axis, self._window_size
        )
        self._width, margin = FillingBar._check_width_margin(
            width, margin, self._length, self._axis, self._window_size
        )
        self._margin = margin
        self._color = BaseFeedbackVisual._check_color(color)
        self._fill_color = BaseFeedbackVisual._check_color(fill_color)
        self._fill_perc = FillingBar._check_fill_perc(fill_perc)

        self._putBar()

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
        # external rectangle to fill
        if self._axis == 0:
            xP1 = self.window_center[0] - self._width // 2 - self._margin
            yP1 = self.window_center[1] - self._length // 2 - self._margin
            xP2 = xP1 + self._width + 2 * self._margin
            yP2 = yP1 + self._length + 2 * self._margin
        elif self._axis == 1:
            xP1 = self.window_center[0] - self._length // 2 - self._margin
            yP1 = self.window_center[1] - self._width // 2 - self._margin
            xP2 = xP1 + self._length + 2 * self._margin
            yP2 = yP1 + self._width + 2 * self._margin

        cv2.rectangle(self._img, (xP1, yP1), (xP2, yP2), self._color, -1)

        # internal smaller rectangle filling the external rectangle
        fill_perc = int((self._length // 2) * self._fill_perc)
        if fill_perc != 0:
            if self._axis == 0:
                xP1 = self.window_center[0] - self._width // 2
                yP1 = self.window_center[1] - fill_perc
                xP2 = xP1 + self._width
                yP2 = yP1 + 2 * fill_perc
            elif self._axis == 1:
                xP1 = self.window_center[0] - fill_perc
                yP1 = self.window_center[1] - self._width // 2
                xP2 = xP1 + 2 * fill_perc
                yP2 = yP1 + self._width

            cv2.rectangle(self._img, (xP1, yP1), (xP2, yP2), self._fill_color, -1)

    # --------------------------------------------------------------------
    @staticmethod
    def _check_length_margin(
        length: int, margin: int, axis: int, window_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Check that the length and margin are valid."""
        length = ensure_int(length, "length")
        margin = ensure_int(margin, "margin")
        assert 0 < length
        assert 0 < margin
        assert margin < length
        assert length + margin <= window_size[(axis + 1) % 2]
        return length, margin

    @staticmethod
    def _check_width_margin(
        width: int,
        margin: int,
        length: int,
        axis: int,
        window_size: tuple[int, int],
    ) -> tuple[int, int]:
        """Check that the width is valid."""
        width = ensure_int(width, "width")
        margin = ensure_int(margin, "margin")
        assert 0 < width
        assert width < length
        assert margin < width
        assert width + margin <= window_size[axis]
        return width, margin

    @staticmethod
    def _check_fill_perc(fill_perc: float) -> float:
        """Check that the fill length is a percentage between 0 and 1."""
        check_type(fill_perc, ("numeric",), fill_perc)
        assert 0 <= fill_perc <= 1
        return fill_perc

    # --------------------------------------------------------------------
    @property
    def length(self) -> int:
        """Length of the bar in pixel."""
        return self._length

    @length.setter
    def length(self, length):
        self._length, _ = FillingBar._check_length_margin(
            length, self._margin, self._axis, self._window_size
        )
        self._reset()
        self._putBar()

    @property
    def width(self) -> int:
        """Width of the bar in pixel."""
        return self._width

    @width.setter
    def width(self, width):
        self._width, _ = FillingBar._check_width_margin(
            width, self._margin, self._length, self._axis, self._window_size
        )
        self._reset()
        self._putBar()

    @property
    def margin(self) -> int:
        """Margin in pixel between the bar and its filled content."""
        return self._margin

    @margin.setter
    def margin(self, margin):
        _, margin = FillingBar._check_length_margin(
            self._length, margin, self._axis, self._window_size
        )
        _, margin = FillingBar._check_width_margin(
            self._width, margin, self._length, self._axis, self._window_size
        )
        self._margin = margin
        self._reset()
        self._putBar()

    @property
    def color(self) -> tuple[int, int, int]:
        """Color used for the bar background in BGR color space."""
        return self._color

    @color.setter
    def color(self, color):
        self._color = BaseFeedbackVisual._check_color(color)
        self._reset()
        self._putBar()

    @property
    def fill_color(self) -> tuple[int, int, int]:
        """Color used to fill the bar in BGR color space."""
        return self._fill_color

    @fill_color.setter
    def fill_color(self, fill_color):
        self._fill_color = BaseFeedbackVisual._check_color(fill_color)
        self._reset()
        self._putBar()

    @property
    def fill_perc(self) -> float:
        """Length filled in percent between 0 and 1."""
        return self._fill_perc

    @fill_perc.setter
    def fill_perc(self, fill_perc):
        self._fill_perc = FillingBar._check_fill_perc(fill_perc)
        self._reset()
        self._putBar()

    @property
    def axis(self) -> int:
        """Axis on which the bar is moving.

        This property is a binary integer:
            - 0: Vertical bar filling along the vertical axis.
            - 1: Horizontal bar filling along the horizontal axis.
        """
        return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = BaseFeedbackVisual._check_axis(axis)
        self._reset()
        self._putBar()
