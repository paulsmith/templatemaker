#!/usr/bin/env python

from distutils.core import setup, Extension
from templatemaker import __version__

setup(
    name='templatemaker',
    version=__version__,
    description='Given a list of text files in a similar format, templatemaker creates a template that can extract data from files in that same format.',
    author='Adrian Holovaty',
    author_email='adrian@holovaty.com',
    packages=['templatemaker'],
    ext_modules=[Extension('templatemaker._template', ['templatemaker.c'])],
)
