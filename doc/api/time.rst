Time
----

The python ``time`` module is not accurate enough for precise timing in experiments. The
``stimuli`` package provides a more accurate clock, the :class:`~stimuli.time.Clock`
class, which uses :func:`time.perf_counter` or :func:`time.monotonic_ns` depending on
which has the highest resolution. The sleeping function :func:`stimuli.time.sleep`
replaces the standard :func:`time.sleep` function and make use of the clock from
``stimuli`` to achieve a better precision.

.. currentmodule:: stimuli.time

.. autosummary::
    :toctree: ../generated/api

    Clock
    sleep

Sleep performance (linux)::

    %timeit time.sleep(0.0005)
    556 μs ± 131 ns per loop (mean ± std. dev. of 7 runs, 1,000 loops each)

    %timeit stimuli.time.sleep(0.0005)
    501 μs ± 77.5 ns per loop (mean ± std. dev. of 7 runs, 1,000 loops each)

Regardless of the function used, ``stimuli`` is still limited by the accuracy of the
on-board computer clock. If you have access to a more accurate clock, you can subclass
the abstract class :class:`~stimuli.time.BaseClock` to implement your own clock.

.. autosummary::
    :toctree: ../generated/api

    BaseClock
