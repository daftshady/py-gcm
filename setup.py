#!usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'pygcm'
]

requires = []

setup(
    name='pygcm',
    version='0.1',
    packages=packages,
    package_data={'': ['LICENSE']},
    include_package_data=True,
    author='daftshady',
    author_email='daftonshady@gmail.com',
    license=open('LICENSE').read(),
    description='Python wrapper for google cloud messaging',
    install_requires=requires
)
