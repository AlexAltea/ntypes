#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

from tests import *

def test_nint():
    test_nint_values()
    test_nint_aliases()
    test_nint_bytes()
    test_nint_utils()
    test_nint_ops_type()
    test_nint_ops_unary()
    test_nint_ops_binary()
    test_nint_ops_reflected()
    test_nint_ops_inplace()
    test_nint_ops_relational()

def test_nfloat():
    test_nfloat_values()
    test_nfloat_aliases()
    test_nfloat_bytes()
    test_nfloat_ops_type()
    test_nfloat_ops_unary()
    test_nfloat_ops_binary()
    test_nfloat_ops_reflected()
    test_nfloat_ops_inplace()
    test_nfloat_ops_relational()

def test():
    test_nint()
    test_nfloat()

if __name__ == '__main__':
    test()
