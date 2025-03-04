"""Read / write access to the parallel port for Linux or Windows.

This code snippet is inspired from the parallel module of PsychoPy.
"""

import sys

# To make life easier, only try drivers which have a hope in heck of working. Because
# hasattr() in connection to windll ends up in an OSError trying to load 32bit drivers
# in a 64bit environment, different drivers defined in the dictionary 'drivers' are
# tested.

if sys.platform.startswith("linux"):
    from ._linux import PParallelLinux

    ParallelPort = PParallelLinux
elif sys.platform == "win32":
    drivers = dict(
        inpout32=("_inpout", "PParallelInpOut"),
        inpoutx64=("_inpout", "PParallelInpOut"),
        dlportio=("_dlportio", "PParallelDLPortIO"),
    )
    from ctypes import windll
    from importlib import import_module

    for key, val in drivers.items():
        driver_name, class_name = val
        try:
            hasattr(windll, key)
            ParallelPort = getattr(
                import_module("." + driver_name, __name__), class_name
            )
            break
        except (OSError, KeyError, NameError):
            ParallelPort = None
            continue
else:
    ParallelPort = None
