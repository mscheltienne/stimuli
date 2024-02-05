from abc import ABC, abstractmethod

from _typeshed import Incomplete
from numpy.typing import NDArray

from ..utils._checks import check_type as check_type
from ..utils._checks import ensure_int as ensure_int
from ..utils._docs import fill_doc as fill_doc
from ..utils.logs import logger as logger

class BaseVisual(ABC):
    """Base visual class.

    Parameters
    ----------
    window_name : str
        Name of the window in which the visual is displayed.
    window_size : tuple | None
        Either ``None`` to automatically select a window size based on the
        available monitors, or a 2-length of positive integer sequence as
        ``(width, height)`` in pixels.
    """

    _window_name: Incomplete
    _window_size: Incomplete
    _window_width: Incomplete
    _window_height: Incomplete
    _window_center: Incomplete
    _img: Incomplete
    _background: Incomplete

    @abstractmethod
    def __init__(
        self, window_name: str = "Visual", window_size: tuple[int, int] | None = None
    ): ...
    def show(self, wait: int = 1) -> None:
        """Show the visual with ``cv2.imshow()`` and ``cv2.waitKey()``.

        Parameters
        ----------
        wait : int
            Wait timer passed to ``cv2.waitKey()`` [ms].
        """

    def close(self) -> None:
        """Close the visual."""

    def draw_background(self, color: str | tuple[int, int, int]) -> None:
        """Draw a uniform single color background.

        Replace all the pixels with this color, thus this method erases any
        prior work.

        Parameters
        ----------
        color : str | tuple
            Color used to draw the background.

        Notes
        -----
        A color is provided as matplotlib string or as ``(B, G, R)`` tuple of
        int8 set between 0 and 255.
        """

    def __del__(self) -> None:
        """Close when deleting the object."""

    @staticmethod
    def _check_window_size(window_size: tuple[int, int] | None) -> tuple[int, int]:
        """Check if the window size is valid.

        If None, set it as the minimum (width, height) supported by any
        connected monitor.
        """

    @staticmethod
    def _check_color(color: str | tuple[int, int, int]) -> tuple[int, int, int]:
        """Check if a color is valid and converts it to BGR."""

    @property
    def window_name(self) -> str:
        """Window's name."""

    @property
    def window_size(self) -> tuple[int, int]:
        """Window's size (width x height)."""

    @property
    def window_center(self) -> tuple[int, int]:
        """Window's center position."""

    @property
    def img(self) -> NDArray[int]:
        """Image array."""

    @property
    def background(self) -> tuple[int, int, int]:
        """Background color in BGR color space."""

    @background.setter
    def background(self, background) -> None:
        """Background color in BGR color space."""

class BaseFeedbackVisual(BaseVisual):
    """Base visual feedback class.

    Parameters
    ----------
    %(visual_window_name)s
    %(visual_window_size)s
    """

    _backup_img: Incomplete

    @abstractmethod
    def __init__(
        self, window_name: str = "Visual", window_size: tuple[int, int] | None = None
    ): ...
    _img: Incomplete

    def _reset(self) -> None:
        """Reset the visual with the backup, thus removing the feedback."""

    @staticmethod
    def _check_axis(axis: str | int) -> int:
        """Check that the axis is valid and converts it to integer (0, 1).

        The axis is a binary integer:
        - 0: Vertical
        - 1: Horizontal
        """
