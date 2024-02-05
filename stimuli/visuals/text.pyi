from ..utils._checks import check_type as check_type
from ..utils._checks import ensure_int as ensure_int
from ..utils._docs import fill_doc as fill_doc
from .base import BaseVisual as BaseVisual

class Text(BaseVisual):
    """
    Class to display a text.

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
    def putText(
        self,
        text: str,
        fontFace: int = ...,
        fontScale: int = 2,
        color: str | tuple[int, int, int] = "white",
        thickness: int = 2,
        lineType: int = ...,
        position: str | tuple[int, int] = "centered",
    ) -> None:
        """Add text to the visual.

        Parameters
        ----------
        text : str
            Text to display.
        fontFace : int ``cv2.FONT``
            Font to use to write the text.
        fontScale : int
            Font scale factor multiplied by the font-specific base size.
        color : str | tuple
            Color used to write the text.
        thickness : int
            Text line thickness in pixel.
        lineType : int ``cv2.LINE``
            Type of line to use.
        position : str | tuple
            Position of the bottom left corner of the text. See notes for
            additional information.

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
    def _check_position(
        position: str | tuple[int, int],
        textWidth,
        textHeight,
        window_size: tuple[int, int],
        window_center: tuple[int, int],
    ) -> tuple[int, int]:
        """Check that the text position is coherent with the window size.

        The position of the text is given as the bottom left corner of the
        text-box.
        """
