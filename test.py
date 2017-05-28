#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

from ntypes import *

def test_values():
    # Max-min values
    assert int(int8_t(+0x7F)) == +0x7F
    assert int(int8_t(-0x80)) == -0x80
    assert int(int16_t(+0x7FFF)) == +0x7FFF
    assert int(int16_t(-0x8000)) == -0x8000
    assert int(int32_t(+0x7FFFFFFF)) == +0x7FFFFFFF
    assert int(int32_t(-0x80000000)) == -0x80000000
    assert int(int64_t(+0x7FFFFFFFFFFFFFFF)) == +0x7FFFFFFFFFFFFFFF
    assert int(int64_t(-0x8000000000000000)) == -0x8000000000000000
    assert int(uint8_t(+0x00)) == +0x00
    assert int(uint8_t(+0xFF)) == +0xFF
    assert int(uint16_t(+0x0000)) == +0x0000
    assert int(uint16_t(+0xFFFF)) == +0xFFFF
    assert int(uint32_t(+0x00000000)) == +0x00000000
    assert int(uint32_t(+0xFFFFFFFF)) == +0xFFFFFFFF
    assert int(uint64_t(+0x0000000000000000)) == +0x0000000000000000
    assert int(uint64_t(+0xFFFFFFFFFFFFFFFF)) == +0xFFFFFFFFFFFFFFFF

    # Overflow-underflow values
    assert int(int8_t(+0x80)) == -0x80
    assert int(int8_t(-0x81)) == +0x7F
    assert int(int16_t(+0x8000)) == -0x8000
    assert int(int16_t(-0x8001)) == +0x7FFF
    assert int(int32_t(+0x80000000)) == -0x80000000
    assert int(int32_t(-0x80000001)) == +0x7FFFFFFF
    assert int(int64_t(+0x8000000000000000)) == -0x8000000000000000
    assert int(int64_t(-0x8000000000000001)) == +0x7FFFFFFFFFFFFFFF
    assert int(uint8_t(-1)) == 0xFF
    assert int(uint8_t(0x100)) == 0
    assert int(uint16_t(-1)) == 0xFFFF
    assert int(uint16_t(0x10000)) == 0
    assert int(uint32_t(-1)) == 0xFFFFFFFF
    assert int(uint32_t(0x100000000)) == 0
    assert int(uint64_t(-1)) == 0xFFFFFFFFFFFFFFFF
    assert int(uint64_t(0x10000000000000000)) == 0


def test_implicit_casts():
    # Signedness
    assert (int_t( signed=True  ) + int_t( signed=True  )).s == True
    assert (int_t( signed=True  ) + int_t( signed=False )).s == False
    assert (int_t( signed=False ) + int_t( signed=True  )).s == False
    assert (int_t( signed=False ) + int_t( signed=False )).s == False

    # Size
    assert (int_t( bits=8  ) + int_t( bits = 8  )).b == 8
    assert (int_t( bits=8  ) + int_t( bits = 16 )).b == 16
    assert (int_t( bits=16 ) + int_t( bits = 8  )).b == 16
    assert (int_t( bits=16 ) + int_t( bits = 16 )).b == 16


def test_explicit_casts():
    pass


def test():
    test_values()
    test_implicit_casts()
    test_explicit_casts()
    # Overflows
    assert uint8_t(0xFF) + uint8_t(0x01) == uint8_t(0x00)


if __name__ == '__main__':
    test()
