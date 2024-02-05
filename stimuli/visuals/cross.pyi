from ..utils._checks import check_type as check_type
from ..utils._checks import ensure_int as ensure_int
from ..utils._docs import fill_doc as fill_doc
from .base import BaseVisual as BaseVisual

class Cross(BaseVisual):
    """Class to display a cross, e.g. a fixation cross.

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
    def putCross(
        self,
        length: int,
        thickness: int,
        color: str | tuple[int, int, int],
        position: str | tuple[int, int] = "centered",
    ) -> None:
        """Draw a cross composed of 2 rectangles.

        The rectangles are defined by length and thickness.
        The rectangles are positioned to form a cross.

        Parameters
        ----------
        length : int
            Number of pixels used to draw the length of the cross.
        thickness : int
            Number of pixels used to draw the thickness of the cross.
        color : str | tuple
            Color used to fill the cross.
        position : str | tuple
            Position of the center of the cross. See notes for additional
            information.

        Notes
        -----
        A color is provided as matplotlib string or as ``(B, G, R)`` tuple of
        int8 set between 0 and 255.
        The position of the object can be either defined as the string 'center' or
        'centered' to position the object in the center of the window; or as a 2-length
        tuple of positive integer. The position is defined in pixels in opencv
        coordinates, with (0, 0) being the top left corner of the window.
        """

    @staticmethod
    def _check_length(length: int, window_size: tuple[int, int]) -> int:
        """Check that the length is valid."""

    @staticmethod
    def _check_thickness(thickness: int, length: int) -> int:
        """Check that the thickness is valid."""

    @staticmethod
    def _check_position(
        position: str | tuple[int, int],
        length: int,
        window_size: tuple[int, int],
        window_center: tuple[int, int],
    ) -> tuple[int, int]:
        """Check that the cross position is coherent with the window size.

        The position of the cross is given as the center of the cross.
        """
