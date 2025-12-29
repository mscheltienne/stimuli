.. include:: ./links.inc

Stimuli
=======

.. toctree::
   :hidden:

   api/index
   generated/tutorials/index
   changes/index

Stimuli is a Python package for delivery of auditory stimuli and events via parallel
port or LSL which does not require `PsychoPy`_\ :footcite:p:`peirce_psychopy2_2019,
peirce_generating_2008,peirce_psychopypsychophysics_2007`. Instead, it uses
`sounddevice`_ for auditory stimuli which uses `PortAudio`_ under-the-hood.

Install
-------

Stimuli is available on `PyPI <project pypi_>`_ and on `conda-forge <project conda_>`_.

.. tab-set::

    .. tab-item:: PyPI

        .. code-block:: bash

            pip install stimuli

        Or use the faster `uv`_:

        .. code-block:: bash

            uv pip install stimuli

    .. tab-item:: Conda

        .. code-block:: bash

            conda install -c conda-forge stimuli

    .. tab-item:: Source

        .. code-block:: bash

            pip install git+https://github.com/mscheltienne/stimuli

License
-------

``stimuli`` is licensed under the `MIT license`_.
A full copy of the license can be found `on GitHub <project license_>`_.

References
----------

.. footbibliography::
