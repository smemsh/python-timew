#

import os
import sys

from sphinxcontrib.writers.rst import RstTranslator, RstWriter
from sphinxcontrib.builders.rst import RstBuilder

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinxcontrib.apidoc',
    'sphinxcontrib.restbuilder',
]
templates_path = ['_templates']
source_suffix = ['.rst']
master_doc = 'index'
language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = True

apidoc_module_dir = '../timew'
apidoc_output_dir = '.'
apidoc_excluded_paths = ['tests']
apidoc_separate_modules = True

class PyTimewRstBuilder(RstBuilder):
    name = 'rst'
    def prepare_writing(self, docnames):
        self.writer = PyTimewRstWriter(self)

class PyTimewRstWriter(RstWriter):
    def translate(self):
        visitor = PyTimewRstTranslator(self.document, self.builder)
        self.document.walkabout(visitor)
        self.output = visitor.body

class PyTimewRstTranslator(RstTranslator):

    def visit_desc_sig_space(self, node):
        pass
    def depart_desc_sig_space(self, node):
        pass

    def visit_literal_strong(self, node):
        self.visit_strong(node)
    def depart_literal_strong(self, node):
        self.depart_strong(node)

    # see upstream commit 82a6d5e99
    def visit_compact_paragraph(self, node):
        self.visit_paragraph(node)
    def depart_compact_paragraph(self, node):
        self.depart_paragraph(node)

    def visit_literal_emphasis(self, node):
        t = node.astext()
        if t.startswith(' ') or t.endswith(' '): pass
        else: self.add_text('*')
    def depart_literal_emphasis(self, node):
        self.visit_literal_emphasis(node)


def setup(app):
    app.add_builder(PyTimewRstBuilder, override=True)
    app.set_translator('rst', PyTimewRstTranslator, override=True)
