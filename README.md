[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![codecov](https://codecov.io/gh/mscheltienne/stimuli/graph/badge.svg?token=92BKRPSD0V)](https://codecov.io/gh/mscheltienne/stimuli)
[![tests](https://github.com/mscheltienne/stimuli/actions/workflows/pytest.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/stimuli/actions/workflows/pytest.yaml)
[![doc](https://github.com/mscheltienne/stimuli/actions/workflows/doc.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/stimuli/actions/workflows/doc.yaml)
[![PyPI version](https://badge.fury.io/py/stimuli.svg)](https://badge.fury.io/py/stimuli)
[![Downloads](https://static.pepy.tech/personalized-badge/stimuli?period=total&units=international_system&left_color=grey&right_color=blue&left_text=pypi%20downloads)](https://pepy.tech/project/stimuli)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/stimuli.svg)](https://anaconda.org/conda-forge/stimuli)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/stimuli.svg)](https://anaconda.org/conda-forge/stimuli)
[![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/stimuli.svg)](https://anaconda.org/conda-forge/stimuli)

# Stimuli

This repository contains auditory stimuli that do not require
[PsychoPy](https://www.psychopy.org/). The auditory stimuli use the python
[sounddevice](https://python-sounddevice.readthedocs.io/en/latest/) library.

# Installation

This repository is available for `python ≥ 3.11` on `pip` with the command
`pip install stimuli` or on `conda-forge` with the command
`conda install -c conda-forge stimuli`.

# Usage

## Audio stimulus

```
from stimuli.audio import Tone
from stimuli.time import sleep
from stimuli.trigger import ParallelPortTrigger

trigger = ParallelPortTrigger("/dev/parport0")
sound = Tone(frequency=1000, volume=80, duration=1)
sound.play(when=0.2)
sleep(0.2)
trigger.signal(1)
```
