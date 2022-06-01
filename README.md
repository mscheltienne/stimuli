[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![codecov](https://codecov.io/gh/mscheltienne/simple-stimuli/branch/main/graph/badge.svg?token=92BKRPSD0V)](https://codecov.io/gh/mscheltienne/simple-stimuli)
[![tests](https://github.com/mscheltienne/simple-stimuli/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/mscheltienne/simple-stimuli/actions/workflows/pytest.yml)
[![build](https://github.com/mscheltienne/simple-stimuli/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/mscheltienne/simple-stimuli/actions/workflows/build.yml)

# Simple-stimuli

This repository contains simple auditory and visual stimuli that do not require
[PsychoPy](https://www.psychopy.org/). The auditory stimuli use the python
[sounddevice](https://python-sounddevice.readthedocs.io/en/0.4.4/) library and
the visual stimuli use the python [opencv](https://docs.opencv.org/4.x/)
library.

# Installation

This repository is available on `pip` for `python ≥ 3.8`:
`pip install stimuli`.

# Usage

## Audio stimulus

```
from stimuli.audio import Tone

sound = Tone(volume=80, frequency=1000)
sound.play()
```

## Visual stimulus

Visual stimulus can be regrouped into 2 categories:

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
