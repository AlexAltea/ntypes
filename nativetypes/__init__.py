#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

# Imports
from .native_int import *
from .native_float import *

# Prevent polluting namespace
del native_int
del native_float

def reinterpret_cast(dst, src):
    assert (isinstance(dst(), nint) or isinstance(dst(), nfloat)) and \
           (isinstance(src, nint) or isinstance(src, nfloat))
    byteorder = 'big'
    return dst.from_bytes(src.to_bytes(byteorder), byteorder)
