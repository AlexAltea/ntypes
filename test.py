#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

from ntypes import *

def test():
    # Addition
    assert uint32_t(1) + uint32_t(1) == uint32_t(2)

if __name__ == '__main__':
    test()
