#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import setuptools

NTYPES_VERSION = '1.0.5'
NTYPES_REPOSITORY_URL = 'https://github.com/AlexAltea/ntypes'
NTYPES_DOWNLOAD_URL = 'https://github.com/AlexAltea/ntypes/tarball/' + NTYPES_VERSION

# Description
NTYPES_DESCRIPTION = """Native Types
============

.. image:: https://api.travis-ci.org/AlexAltea/ntypes.svg?branch=master
    :target: https://travis-ci.org/AlexAltea/ntypes/
    
.. image:: https://coveralls.io/repos/github/AlexAltea/ntypes/badge.svg?branch=master
    :target: https://coveralls.io/github/AlexAltea/ntypes?branch=master
    
.. image:: https://img.shields.io/pypi/v/nativetypes.svg
    :target: https://pypi.python.org/pypi/nativetypes

Emulate native integer and floating-point types in Python 2.x and 3.x.

More information at: https://github.com/AlexAltea/ntypes
"""

setuptools.setup(
    name='nativetypes',
    version=NTYPES_VERSION,
    description='Native integer and floating-point type emulation',
    long_description=NTYPES_DESCRIPTION,
    license='MIT',
    author='Alexandro Sanchez Bach',
    author_email='alexandro@phi.nz',
    url=NTYPES_REPOSITORY_URL,
    download_url=NTYPES_DOWNLOAD_URL,
    packages=['nativetypes'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
    ],
)
