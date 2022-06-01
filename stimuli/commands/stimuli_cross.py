import argparse

from .. import set_log_level
from ..visuals import Cross
from . import helpdict


def run():
    """Entry-point to display a fixation cross via CLI."""
    parser = argparse.ArgumentParser(
        prog="Stimuli", description="Display a fixation cross"
    )
    parser.add_argument(
        "--name",
        help="name of the visual window",
        type=str,
        metavar=str,
        default="FixationCross",
    )
    parser.add_argument(
        "--winsize",
        help="size of the visual window",
        type=int,
        metavar=int,
        nargs=2,
        default=None,
    )
    parser.add_argument(
        "--bgcolor",
        help="background BGR color as 3 integers in the range [0, 255]",
        type=int,
        metavar=int,
        nargs=3,
        default=(0, 0, 0),
    )
    parser.add_argument(
        "--length",
        help="length of the fixation cross [px]",
        type=int,
        metavar=int,
        default=200,
    )
    parser.add_argument(
        "--thickness",
        help="thickness of the fixation cross [px]",
        type=int,
        metavar=int,
        default=30,
    )
    parser.add_argument(
        "--color",
        help="BGR color of the cross as 3 integers in the range [0, 255]",
        type=int,
        metavar=int,
        nargs=3,
        default=(210, 210, 210),
    )
    parser.add_argument(
        "--position",
        help="(x, y) position of the fixation cross [px]",
        type=str,
        metavar=int,
        nargs=2,
        default="center",
    )
    parser.add_argument(
        "--loglevel",
        type=str,
        metavar="str",
        help=helpdict["loglevel"],
        default="warning",
    )
    args = parser.parse_args()
    set_log_level(args.loglevel.upper().strip())

    winsize = None if args.winsize is None else tuple(args.winsize)
    position = (
        args.position
        if args.position in ("center", "centered")
        else tuple([int(elt) for elt in args.position])
    )

    visual = Cross(args.name, winsize)
    visual.draw_background(tuple(args.bgcolor))
    visual.putCross(args.length, args.thickness, tuple(args.color), position)
    visual.show(0)
