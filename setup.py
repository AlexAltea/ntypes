#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import setuptools

NTYPES_VERSION = '1.0.0'
NTYPES_REPOSITORY_URL = 'https://github.com/AlexAltea/ntypes'
NTYPES_DOWNLOAD_URL = 'https://github.com/AlexAltea/ntypes/tarball/' + NTYPES_VERSION

def read(path):
    with codecs.open(path, 'r', 'utf8') as f:
        return f.read()

setuptools.setup(
    name='ntypes',
    version='1.0',
    description='Native types for Python',
    long_description=read('README.rst'),
    license='MIT',
    author='Alexandro Sanchez Bach',
    author_email='alexandro@phi.nz',
    url=NTYPES_REPOSITORY_URL,
    download_url=NTYPES_DOWNLOAD_URL,
    packages=['ntypes'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
    ],
)
