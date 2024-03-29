import os
import sys

sys.path.insert(0, os.path.abspath('../'))

project = 'shorty'
copyright = '2023, Velocidensity'
author = 'Velocidensity'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinxcontrib.autohttp.flask'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'furo'
html_static_path = ['_static']
