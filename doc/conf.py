# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import stimuli

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "simple-stimuli"
copyright = "2022, Mathieu Scheltienne"
author = "Mathieu Scheltienne"
release = stimuli.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = "5.0"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_copybutton",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_issues",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Sphinx will warn about all references where the target cannot be found.
nitpicky = True

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]

# -- Autodoc -----------------------------------------------------------------
autodoc_typehints = "none"

# -- Intersphinx -------------------------------------------------------------
intersphinx_mapping = {
    "numpy": ("https://numpy.org/devdocs", None),
    "python": ("https://docs.python.org/3", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "scipy": ("https://scipy.github.io/devdocs", None),
    "sounddevice": ("https://python-sounddevice.readthedocs.io/", None),
}
intersphinx_timeout = 5

# -- Napoleon ----------------------------------------------------------------
napoleon_google_docstring = False
napoleon_numpy_docstring = True

# -- Sphinx-issues -----------------------------------------------------------
issues_github_path = "mscheltienne/simple-stimuli"
