from abc import ABC, abstractmethod
from copy import deepcopy

import cv2
import numpy as np
import screeninfo
from matplotlib import colors
from numpy.typing import NDArray

from ..utils._checks import check_type, ensure_int
from ..utils._docs import fill_doc
from ..utils.logs import logger


@fill_doc
class BaseVisual(ABC):
    """Base visual class.

    Parameters
    ----------
    %(visual_window_name)s
    %(visual_window_size)s
    """

    @abstractmethod
    def __init__(
        self,
        window_name: str = "Visual",
        window_size: tuple[int, int] | None = None,
    ):
        check_type(window_name, (str,), "window_name")

        self._window_name = window_name

        # size attributes
        self._window_size = BaseVisual._check_window_size(window_size)
        self._window_width = self._window_size[0]
        self._window_height = self._window_size[1]
        self._window_center = (
            self._window_width // 2,
            self._window_height // 2,
        )

        # default to black background
        self._img = np.full(
            (self._window_height, self._window_width, 3),
            fill_value=(0, 0, 0),
            dtype=np.uint8,
        )
        self._background = (0, 0, 0)

    def show(self, wait: int = 1) -> None:
        """Show the visual with ``cv2.imshow()`` and ``cv2.waitKey()``.

        Parameters
        ----------
        wait : int
            Wait timer passed to ``cv2.waitKey()`` [ms].
        """
        wait = ensure_int(wait, "wait")
        cv2.imshow(self._window_name, self._img)
        cv2.waitKey(wait)

    def close(self) -> None:
        """Close the visual."""
        try:
            cv2.destroyWindow(self._window_name)
        except Exception:
            pass

    @fill_doc
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
        %(visual_color)s
        """
        color = BaseVisual._check_color(color)
        self._img = np.full(
            (self._window_height, self._window_width, 3),
            fill_value=color,
            dtype=np.uint8,
        )
        self._background = color

    def __del__(self):
        """Close when deleting the object."""
        self.close()

    # --------------------------------------------------------------------
    @staticmethod
    def _check_window_size(window_size: tuple[int, int] | None) -> tuple[int, int]:
        """Check if the window size is valid.

        If None, set it as the minimum (width, height) supported by any
        connected monitor.
        """
        check_type(window_size, (None, tuple), "window_size")

        if window_size is None:
            try:
                width = min(monitor.width for monitor in screeninfo.get_monitors())
                height = min(monitor.height for monitor in screeninfo.get_monitors())
            except Exception as error:
                logger.error("No monitor found.")
                raise error
            window_size = (width, height)

        for size in window_size:
            size = ensure_int(size)
        assert len(window_size) == 2
        assert all(0 < size for size in window_size)
        return window_size

    @staticmethod
    def _check_color(color: str | tuple[int, int, int]) -> tuple[int, int, int]:
        """Check if a color is valid and converts it to BGR."""
        check_type(color, (str, tuple), "color")
        if isinstance(color, str):
            r, g, b, _ = colors.to_rgba(color)
            color = tuple([int(c * 255) for c in (b, g, r)])
        assert len(color) == 3
        assert all(0 <= c <= 255 for c in color)
        return color

    # --------------------------------------------------------------------
    @property
    def window_name(self) -> str:
        """Window's name."""
        return self._window_name

    @property
    def window_size(self) -> tuple[int, int]:
        """Window's size (width x height)."""
        return self._window_size

    @property
    def window_center(self) -> tuple[int, int]:
        """Window's center position."""
        return self._window_center

    @property
    def img(self) -> NDArray[int]:
        """Image array."""
        return self._img

    @property
    def background(self) -> tuple[int, int, int]:
        """Background color in BGR color space."""
        return self._background

    @background.setter
    def background(self, background):
        self.draw_background(background)


class BaseFeedbackVisual(BaseVisual):
    """Base visual feedback class.

    Parameters
    ----------
    %(visual_window_name)s
    %(visual_window_size)s
    """

    @abstractmethod
    def __init__(
        self,
        window_name: str = "Visual",
        window_size: tuple[int, int] | None = None,
    ):
        super().__init__(window_name, window_size)
        self._backup_img = None

    def _reset(self):
        """Reset the visual with the backup, thus removing the feedback."""
        if self._backup_img is not None:
            self._img = deepcopy(self._backup_img)

    # --------------------------------------------------------------------
    @staticmethod
    def _check_axis(axis: str | int) -> int:
        """Check that the axis is valid and converts it to integer (0, 1).

        The axis is a binary integer:
        - 0: Vertical
        - 1: Horizontal
        """
        check_type(axis, ("int-like", str), "axis")
        if isinstance(axis, str):
            axis = axis.lower().strip()
            assert axis in ["horizontal", "h", "vertical", "v"]
            axis = 0 if axis.startswith("v") else 1
        else:
            axis = ensure_int(axis)
        assert axis in (0, 1)
        return axis
