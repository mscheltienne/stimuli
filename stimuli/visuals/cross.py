from typing import Optional, Tuple, Union

import cv2

from ..utils._checks import _check_type
from ..utils._docs import fill_doc
from .base import BaseVisual


@fill_doc
class Cross(BaseVisual):
    """Class to display a cross, e.g. a fixation cross.

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
    def putCross(
        self,
        length: int,
        thickness: int,
        color: Union[str, Tuple[int, int, int]],
        position: Union[str, Tuple[int, int]] = "centered",
    ) -> None:
        """Draw a cross composed of 2 rectangles.

        The rectangles are defined by length and thickness.
        The rectangles are positioned to form a cross.

        - Horizontal rectangle
        P1 --------------
        |                |
         -------------- P2

        - Vertical rectangle
        P1 --
        |    |
        |    |
        |    |
        |    |
        |    |
         -- P2

        Parameters
        ----------
        length : int
            Number of pixels used to draw the length of the cross.
        thickness : int
            Number of pixels used to draw the thickness of the cross.
        color : str | tuple
            Color used to fill the cross. %(visual_color)s
        position : str | tuple
            Position of the center of the cross. See notes for additional
            information.

        Notes
        -----
        %(visual_position)s
        """
        length = Cross._check_length(length, self._window_size)
        thickness = Cross._check_thickness(thickness, length)
        color = BaseVisual._check_color(color)
        position = Cross._check_position(
            position, length, self._window_size, self._window_center
        )

        # Horizontal rectangle
        xP1 = position[0] - length // 2
        yP1 = position[1] - thickness // 2
        xP2 = xP1 + length
        yP2 = yP1 + thickness
        cv2.rectangle(self._img, (xP1, yP1), (xP2, yP2), color, -1)

        # Vertical rectangle
        xP1 = position[0] - thickness // 2
        yP1 = position[1] - length // 2
        xP2 = xP1 + thickness
        yP2 = yP1 + length
        cv2.rectangle(self._img, (xP1, yP1), (xP2, yP2), color, -1)

    # --------------------------------------------------------------------
    @staticmethod
    def _check_length(length: int, window_size: Tuple[int, int]) -> int:
        """Check that the length is valid."""
        _check_type(length, ("int",), "length")
        assert 0 < length
        assert all(length <= size for size in window_size)
        return length

    @staticmethod
    def _check_thickness(thickness: int, length: int) -> int:
        """Check that the thickness is valid."""
        _check_type(thickness, ("int",), "thickness")
        assert 0 < thickness
        assert thickness < length
        return thickness

    @staticmethod
    def _check_position(
        position: Union[str, Tuple[int, int]],
        length: int,
        window_size: Tuple[int, int],
        window_center: Tuple[int, int],
    ) -> Tuple[int, int]:
        """Check that the cross position is coherent with the window size.

        The position of the cross is given as the center of the cross.
        """
        _check_type(position, (str, tuple), "position")
        if isinstance(position, str):
            position = position.lower().strip()
            assert position in ["centered", "center"]
            position = window_center
        for pos in position:
            _check_type(pos, ("int",))
        assert len(position) == 2
        assert 0 <= position[0] - length // 2
        assert position[0] - length // 2 + length <= window_size[0]
        assert 0 <= position[1] - length // 2
        assert position[1] - length // 2 + length <= window_size[1]
        return position
