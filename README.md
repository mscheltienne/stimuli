[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![codecov](https://codecov.io/gh/mscheltienne/simple-stimuli/branch/main/graph/badge.svg?token=92BKRPSD0V)](https://codecov.io/gh/mscheltienne/simple-stimuli)
[![tests](https://github.com/mscheltienne/simple-stimuli/actions/workflows/pytest.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/simple-stimuli/actions/workflows/pytest.yaml)
[![doc](https://github.com/mscheltienne/simple-stimuli/actions/workflows/doc.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/simple-stimuli/actions/workflows/doc.yaml)
[![PyPI version](https://badge.fury.io/py/stimuli.svg)](https://badge.fury.io/py/stimuli)
[![Downloads](https://static.pepy.tech/personalized-badge/stimuli?period=total&units=international_system&left_color=grey&right_color=blue&left_text=pypi%20downloads)](https://pepy.tech/project/stimuli)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/stimuli.svg)](https://anaconda.org/conda-forge/stimuli)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/stimuli.svg)](https://anaconda.org/conda-forge/stimuli)
[![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/stimuli.svg)](https://anaconda.org/conda-forge/stimuli)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7470600.svg)](https://zenodo.org/records/7470600)

# Simple-stimuli

This repository contains simple auditory and visual stimuli that do not require
[PsychoPy](https://www.psychopy.org/). The auditory stimuli use the python
[sounddevice](https://python-sounddevice.readthedocs.io/en/0.4.4/) library and
the visual stimuli use the python [opencv](https://docs.opencv.org/4.x/)
library.

# Installation

This repository is available for `python ≥ 3.8` on `pip` with the command
`pip install stimuli` or on `conda-forge` with the command
`conda install -c conda-forge stimuli`.

# Usage

## Audio stimulus

```
from stimuli.audio import Tone

sound = Tone(volume=80, frequency=1000)
sound.play()
```

The volume can be set independently for each channel (stereo) by providing a tuple
`(L, R)`.

## Visual stimulus

Visual stimulus can be grouped into 2 categories:

- simple visuals that are drawn on top of each other
- feedback visuals that are drawn once and updated

### Simple visual

```
from stimuli.visuals import Text

visual = Text()
visual.background = "lightgrey"  # equivalent to visual.draw_background()
visual.putText("Top secret not-so-secret instructions!")
visual.show()
```

### Feedback visual

```
import numpy as np

from stimuli.visuals import FillingBar

visual = FillingBar()
visual.background = "lightgrey"  # equivalent to visual.draw_background()
visual.putBar(length=200, width=20, margin=2, color="black", fill_color="teal")

for k in np.arange(0, 1, 0.1):
    visual.fill_perc = k  # update the visual
    visual.show(100)  # wait 100 ms

visual.close()
```
