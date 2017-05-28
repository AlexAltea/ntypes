#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

from ntypes import *

def test_values():
    # Max-min values
    assert int(int8(+0x7F)) == +0x7F
    assert int(int8(-0x80)) == -0x80
    assert int(int16(+0x7FFF)) == +0x7FFF
    assert int(int16(-0x8000)) == -0x8000
    assert int(int32(+0x7FFFFFFF)) == +0x7FFFFFFF
    assert int(int32(-0x80000000)) == -0x80000000
    assert int(int64(+0x7FFFFFFFFFFFFFFF)) == +0x7FFFFFFFFFFFFFFF
    assert int(int64(-0x8000000000000000)) == -0x8000000000000000
    assert int(uint8(+0x00)) == +0x00
    assert int(uint8(+0xFF)) == +0xFF
    assert int(uint16(+0x0000)) == +0x0000
    assert int(uint16(+0xFFFF)) == +0xFFFF
    assert int(uint32(+0x00000000)) == +0x00000000
    assert int(uint32(+0xFFFFFFFF)) == +0xFFFFFFFF
    assert int(uint64(+0x0000000000000000)) == +0x0000000000000000
    assert int(uint64(+0xFFFFFFFFFFFFFFFF)) == +0xFFFFFFFFFFFFFFFF

    # Overflow-underflow values
    assert int(int8(+0x80)) == -0x80
    assert int(int8(-0x81)) == +0x7F
    assert int(int16(+0x8000)) == -0x8000
    assert int(int16(-0x8001)) == +0x7FFF
    assert int(int32(+0x80000000)) == -0x80000000
    assert int(int32(-0x80000001)) == +0x7FFFFFFF
    assert int(int64(+0x8000000000000000)) == -0x8000000000000000
    assert int(int64(-0x8000000000000001)) == +0x7FFFFFFFFFFFFFFF
    assert int(uint8(-1)) == 0xFF
    assert int(uint8(0x100)) == 0
    assert int(uint16(-1)) == 0xFFFF
    assert int(uint16(0x10000)) == 0
    assert int(uint32(-1)) == 0xFFFFFFFF
    assert int(uint32(0x100000000)) == 0
    assert int(uint64(-1)) == 0xFFFFFFFFFFFFFFFF
    assert int(uint64(0x10000000000000000)) == 0


def test_casts_implicit():
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


def test_casts_explicit():
    pass


def test_ops_binary():
    # Casts
    assert uint8(0xFF) + 1 == uint8(0)
    assert 1 + uint8(0xFF) == uint8(0)

    # Binary ops
    assert uint8(3)  + uint8(2) == uint8(5)
    assert uint8(3)  - uint8(2) == uint8(1)
    assert uint8(3)  * uint8(2) == uint8(6)
    assert uint8(3)  / uint8(2) == uint8(1)
    assert uint8(3) // uint8(2) == uint8(1)
    assert uint8(7)  % uint8(5) == uint8(2)

def test_ops_inplace():
    v = uint32(0xFFFFFFFF)
    v += uint64(1)
    assert v == uint32(0)

def test_ops_relational():
    # Casts
    assert int8(0x1) == 1
    assert int8(0x100) == 0

    # Signedness
    assert  int8(0x80) <  int8(0x7F)
    assert uint8(0x80) >  int8(0x7F)
    assert  int8(0x80) > uint8(0x7F)
    assert uint8(0x80) > uint8(0x7F)


def test():
    test_values()
    test_casts_implicit()
    test_casts_explicit()
    test_ops_binary()
    test_ops_inplace()
    test_ops_relational()


if __name__ == '__main__':
    test()
