#!/usr/bin/env python
from setuptools import setup

NAME = 'squire'
DESCRIPTION = 'Watch a directory and run a command on changes'

VERSION = open('VERSION').read().strip()
LONG_DESC = open('README.rst').read()
LICENSE = open('LICENSE').read()

PACKAGES = ['squire']
SCRIPTS = ['bin/squire']

setup(
    name=NAME,
    version=VERSION,
    author='Charles Thomas',
    author_email='ch@rlesthom.as',
    url='https://github.com/charlesthomas/%s' % NAME,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    packages=PACKAGES,
    scripts=SCRIPTS,
)
