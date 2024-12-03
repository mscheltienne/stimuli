.. include:: ../links.inc

Keyboard
--------

To interact with the keyboard during an experiment, you can use a
:class:`~stimuli.keyboard.Keyboard` object which monitors in a separate thread for key
inputs.

.. curentmodule:: stimuli.keyboard

.. autosummary::
    :toctree: ../generated/api

    Keyboard
    KeyEvent

Example usage::

    from stimuli.keyboard import Keyboard
    from stimuli.time import sleep


    kb = Keyboard(keys=["esc", "space"]).start(suppress=True)
    while True:
        events = kb.get_keys()
        if any(event.key == "esc" for event in events):
            print("Escape key pressed")
            break
        spaces = [event.key == "space" for event in events]
        print(f"Space bar pressed {spaces.count(True)} times in the last 500 ms.")
        sleep(0.5)
