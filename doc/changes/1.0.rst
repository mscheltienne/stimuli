.. NOTE: we use cross-references to highlight new functions and classes.
   Please follow the examples below, so the changelog page will have a link to
   the function/class documentation.

.. NOTE: there are 3 separate sections for changes, based on type:
   - "Enhancements" for new features
   - "Bugs" for bug fixes
   - "API changes" for backward-incompatible changes

.. include:: ./authors.inc

.. _latest:

Version 1.0
-----------

- Remove the visual stimuli module (by `Mathieu Scheltienne`_)
- Refactor the audio stimuli module to use a precise callback mechanism (by `Mathieu Scheltienne`_)
- Add trigger via parallel port with :class:`~stimuli.trigger.ParallelPortTrigger` (by `Mathieu Scheltienne`_)
- Add trigger via LSL with :class:`~stimuli.trigger.LSLTrigger` (by `Mathieu Scheltienne`_)
- Add time module to measure time and sleep with :class:`~stimuli.time.Clock` and :func:`~stimuli.time.sleep` (by `Mathieu Scheltienne`_)

Authors
~~~~~~~

* `Mathieu Scheltienne`_
