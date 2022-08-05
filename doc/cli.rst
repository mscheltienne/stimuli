Command-Line-Interface
======================

Simple-stimuli supports the following CLI entry-points:

- :ref:`stimuli_cross`

In a terminal, use the ``--help`` flag to get additional information on the
arguments.

.. code-block:: bash

    command --help

stimuli_cross
-------------

Arguments
~~~~~~~~~

The ``stimuli_cross`` command display a fixation
:class:`~stimuli.visuals.Cross`. It supports the arguments:

- ``--name`` - name of the visual window (str)
- ``--winsize`` - size of the visual window (int int)
- ``--bgcolor`` - background color in the range 0 to 255 (int int int)
- ``--length`` - length of the fixation cross in pixels (int)
- ``--thickness`` - thickness of the fixation cross in pixels (int)
- ``--color`` - color of the fixation cross in the range 0 to 255 (int int int)
- ``--position`` - (x, y) position of the fixation cross in pixels (int int)

Example
~~~~~~~

.. code-block:: bash

    stimuli_cross --name Cross --winsize 1000 500 --bgcolor 255 255 255 --color 10 10 10

Note that all the arguments are optional. The command by itself will draw a
lightgrey fixation :class:`~stimuli.visuals.Cross` on a black background.
