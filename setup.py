#!/usr/bin/env python2

from distutils.core import setup

setup(
    name = 'Sparks',
    version = '0.4',
    description = 'A vectorial shooter',
    author = 'Haltux',
    url = 'https://github.com/haltux',
    packages = ['Sparks'],
    package_data = {'Sparks': ['data/fonts/*', 'cfg/*']},
    scripts = ['sparks_pandora.sh', 'sparks.py'],
)
