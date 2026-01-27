import os
import sys
import sphinx_rtd_theme

# -- Project information -----------------------------------------------------
project = 'ThirdFactor AI API Gateway'
copyright = '2025, ThirdFactor AI'
author = 'ThirdFactor AI'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
