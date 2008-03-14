#!/usr/bin/env python

from distutils.core import setup, Extension

setup(
    name='templatemaker',
    version='0.0.1',
    description='Given a list of text files in a similar format, templatemaker creates a template that can extract data from files in that same format.',
    author='Adrian Holovaty',
    author_email='adrian@holovaty.com',
    packages=['templatemaker'],
    ext_modules=[Extension('templatemaker._template', ['templatemaker.c'])],
)
