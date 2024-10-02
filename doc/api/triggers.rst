.. include:: ../links.inc

Triggers
--------

To mark events in time during an experiment, you can use triggers. For instance, you can
mark the onset of a sound. The triggers defined in ``stimuli`` uses one byte to encode
the trigger value, i.e. the trigger value must be between 1 and 255 (except for the
:class:`~stimuli.trigger.LSLTrigger` which uses a trigger value between 1 and 127).

.. currentmodule:: stimuli.trigger

.. autosummary::
    :toctree: ../generated/api

    MockTrigger
    LSLTrigger
    ParallelPortTrigger

Example usage::

    from stimuli.trigger import ParallelPortTrigger

    trigger = ParallelPortTrigger("/dev/parport0")
    trigger.signal(1)  # send trigger value 1

Arduino to Parallel Port converter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parallel ports are less and less common on computers, and are not supported by macOS.
Instead, the `Fondation Campus Biotech Geneva <fcbg_>`_ developed a USB to parallel port
converter using an arduino.

The details can be found on this repository:
https://github.com/fcbg-platforms/arduino-trigger

This converter can be used with the :class:`~stimuli.trigger.ParallelPortTrigger` class
by specifying the path to the serial port connected to the arduino or by using the
:class:`str` ``"arduino"`` for automatic detection.
