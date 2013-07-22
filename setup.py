#!usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = ['pygcm']

requires = []

setup(
    name='pygcm',
    version='0.1',
    packages=packages,
    author='daftshady',
    author_email='daftonshady@gmail.com',
    licence=open('LICENSE').read(),
    description='Python wrapper for google cloud messaging',
    install_requires=requires
    )


