from typing import Optional, Tuple, Union

import cv2

from ..utils._checks import _check_type
from ..utils._docs import fill_doc
from .base import BaseVisual


@fill_doc
class Text(BaseVisual):
    """
    Class to display a text.

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
    def putText(
        self,
        text: str,
        fontFace: int = cv2.FONT_HERSHEY_DUPLEX,
        fontScale: int = 2,
        color: Union[str, Tuple[int, int, int]] = "white",
        thickness: int = 2,
        lineType: int = cv2.LINE_AA,
        position: Union[str, Tuple[int, int]] = "centered",
    ) -> None:
        """Add text to the visual.

        Parameters
        ----------
        text : str
            Text to display.
        fontFace : int (cv2.FONT)
            Font to use to write the text.
        fontScale : int
            Font scale factor multiplied by the font-specific base size.
        color : str | tuple
            Color used to write the text. %(visual_color)s
        thickness : int
            Text line thickness in pixel.
        lineType : int (cv2.LINE)
            Type of line to use.
        position : str | tuple
            Position of the bottom left corner of the text. See notes for
            additional information.

        Notes
        -----
        %(visual_position)s
        """
        _check_type(text, (str,), "text")
        if len(text.strip()) == 0:
            return None
        _check_type(fontFace, ("int",), "fontFace")
        _check_type(fontScale, ("int",), "fontScale")
        _check_type(thickness, ("int",), "thickness")
        _check_type(lineType, ("int",), "lineType")
        textWidth, textHeight = cv2.getTextSize(
            text, fontFace, fontScale, thickness
        )[0]
        position = Text._check_position(
            position,
            textWidth,
            textHeight,
            self._window_size,
            self._window_center,
        )
        color = BaseVisual._check_color(color)

        cv2.putText(
            self._img,
            text,
            position,
            fontFace,
            fontScale,
            color,
            thickness=thickness,
            lineType=lineType,
        )

    # --------------------------------------------------------------------
    @staticmethod
    def _check_position(
        position: Union[str, Tuple[int, int]],
        textWidth,
        textHeight,
        window_size: Tuple[int, int],
        window_center: Tuple[int, int],
    ) -> Tuple[int, int]:
        """Check that the text position is coherent with the window size.

        The position of the text is given as the bottom left corner of the
        text-box.
        """
        _check_type(position, (str, tuple), "position")
        if isinstance(position, str):
            position = position.lower().strip()
            assert position in ["centered", "center"]
            position = (
                window_center[0] - textWidth // 2,
                window_center[1] + textHeight // 2,
            )
        for pos in position:
            _check_type(pos, ("int",))
        assert len(position) == 2
        assert 0 <= position[0]
        assert position[0] + textWidth <= window_size[0]
        assert 0 <= position[1] - textHeight
        assert position[1] <= window_size[1]
        return position
