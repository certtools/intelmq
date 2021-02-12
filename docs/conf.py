# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import codecs
import os
import subprocess
import sys
from sphinx.domains import Domain

sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('./'))

import autogen

# -- Project information -----------------------------------------------------

project = 'intelmq'
copyright = '2020, cert.at'
author = 'IntelMQ Community'
# for compatibility with Sphinx < 2.0 as the old versions default to 'contents'
master_doc = 'index'

# The full version, including alpha/beta/rc tags
release = '2.3.0'

rst_prolog = """
.. |intelmq-users-list-link| replace:: `IntelMQ Users Mailinglist <https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-users>`__
.. |intelmq-developers-list-link| replace:: `IntelMQ Developers Mailinglist <https://lists.cert.at/cgi-bin/mailman/listinfo/intelmq-dev>`__
.. |intelmq-manager-github-link| replace:: `IntelMQ Manager <https://github.com/certtools/intelmq-manager>`__
"""
# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.extlinks',
        'sphinx.ext.napoleon'
]

# Napoleon settings
# based on https://github.com/certtools/intelmq/issues/910
#napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
#napoleon_include_special_with_doc = True
#napoleon_use_admonition_for_examples = False
#napoleon_use_admonition_for_notes = False
#napoleon_use_admonition_for_references = False
#napoleon_use_ivar = False
#napoleon_use_param = True
#napoleon_use_rtype = True


extlinks = {'issue': ('https://github.com/certtools/intelmq/issues/%s', 'issue ')}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'source/intelmq.tests.*']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
        'logo': 'Logo_Intel_MQ.svg',
        'github_user': 'certtools',
        'github_repo': 'intelmq',
        'font_family': "'Open Sans', sans-serif",
        'description': 'IntelMQ is a solution for IT security teams for collecting and processing security feeds using a message queuing protocol.',
        'show_powered_by': False,
        }

def run_apidoc(_):
    subprocess.check_call("sphinx-apidoc --implicit-namespaces -o source ../intelmq", shell=True)


def run_autogen(_):
    with codecs.open('dev/harmonization-fields.rst', 'w', encoding='utf-8') as handle:
        handle.write(autogen.harm_docs())
    with codecs.open('user/feeds.rst', 'w', encoding='utf-8') as handle:
        handle.write(autogen.feeds_docs())


def setup(app):
    app.connect("builder-inited", run_apidoc)
    app.connect("builder-inited", run_autogen)
