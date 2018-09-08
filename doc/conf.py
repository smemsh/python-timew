# -*- coding: utf-8 -*-
# project = 'Timewarrior API'
# copyright = '2018, Tjaart van der Walt'
# author = 'Tjaart van der Walt'

# # The short X.Y version
# version = ''
# # The full version, including alpha/beta/rc tags
# release = '1.0.0'

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinxcontrib.apidoc',
]
templates_path = ['_templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'
language = None
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = "sphinx_rtd_theme"
htmlhelp_basename = 'TimewarriorAPIdoc'
todo_include_todos = True

apidoc_module_dir = '../timew'
apidoc_output_dir = 'src'
apidoc_excluded_paths = ['tests']
apidoc_separate_modules = True
