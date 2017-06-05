#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

from ntypes import *

#######################################
# Test: Native Integer values         #
#######################################

def test_nint_values():
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

def test_nint_casts_implicit():
    # Signedness
    assert (nint( signed=True  ) + nint( signed=True  )).s == True
    assert (nint( signed=True  ) + nint( signed=False )).s == False
    assert (nint( signed=False ) + nint( signed=True  )).s == False
    assert (nint( signed=False ) + nint( signed=False )).s == False
    # Size
    assert (nint( bits=8  ) + nint( bits = 8  )).b == 8
    assert (nint( bits=8  ) + nint( bits = 16 )).b == 16
    assert (nint( bits=16 ) + nint( bits = 8  )).b == 16
    assert (nint( bits=16 ) + nint( bits = 16 )).b == 16

def test_nint_casts_explicit():
    pass

def test_nint_ops_type():
    # String
    assert str(uint8(0x00)) == str(int8(0x00)) == str(0)
    assert str(uint8(0x01)) == str(int8(0x01)) == str(1)
    assert str(uint8(0x7F)) == str(int8(0x7F)) == str(127)
    assert str(uint8(0xFF)) == str(255)
    assert str( int8(0xFF)) == str(-1)
    # Integer
    assert int(uint8(0x00)) == int(int8(0x00)) == 0
    assert int(uint8(0x01)) == int(int8(0x01)) == 1
    assert int(uint8(0x7F)) == int(int8(0x7F)) == 127
    assert int(uint8(0xFF)) == 255
    assert int( int8(0xFF)) == -1
    # Boolean
    assert bool(uint8(0x00)) == bool(int8(0x00)) == False
    assert bool(uint8(0x01)) == bool(int8(0x01)) == True
    assert bool(uint8(0x7F)) == bool(int8(0x7F)) == True
    assert bool(uint8(0x80)) == bool(int8(0x80)) == True
    assert bool(uint8(0xFF)) == bool(int8(0xFF)) == True
    # Float
    assert float(uint8(0x00)) == float(int8(0x00)) == 0.0
    assert float(uint8(0x01)) == float(int8(0x01)) == 1.0
    assert float(uint8(0x7F)) == float(int8(0x7F)) == 127.0
    assert float(uint8(0xFF)) == 255.0
    assert float( int8(0xFF)) == -1.0
    # Index
    array = list(range(256 + 1))
    assert array[uint8(0x00)] == array[int8(0x00)] == 0x00
    assert array[uint8(0x01)] == array[int8(0x01)] == 0x01
    assert array[uint8(0x7F)] == array[int8(0x7F)] == 0x7F
    assert array[uint8(0xFF)] == 0xFF
    assert array[ int8(0xFF)] == 0x100

def test_nint_ops_unary():
    # Casts
    assert (~nint( signed=True  )).s == True
    assert (~nint( signed=False )).s == False
    assert (~nint( bits=8  )).b == 8
    assert (~nint( bits=16 )).b == 16
    # Absolute value
    assert abs(uint8(0x00)) == abs(int8(0x00)) == 0x00
    assert abs(uint8(0x01)) == abs(int8(0x01)) == 0x01
    assert abs(uint8(0x7F)) == abs(int8(0x7F)) == 0x7F
    assert abs(uint8(0x80)) == abs(int8(0x80)) == 0x80
    assert abs(uint8(0xFF)) == 0xFF
    assert abs( int8(0xFF)) == 0x01
    # Plus
    assert +uint8(0x00) == +int8(0x00) == 0x00
    assert +uint8(0x01) == +int8(0x01) == 0x01
    assert +uint8(0x7F) == +int8(0x7F) == 0x7F
    assert +uint8(0x80) == +int8(0x80) == 0x80
    assert +uint8(0xFF) == +int8(0xFF) == 0xFF
    # Minus
    assert -uint8(0x00) == -int8(0x00) == 0x00
    assert -uint8(0x01) == -int8(0x01) == 0xFF
    assert -uint8(0x7F) == -int8(0x7F) == 0x81
    assert -uint8(0x80) == -int8(0x80) == 0x80
    assert -uint8(0xFF) == -int8(0xFF) == 0x01
    # Not
    assert ~uint8(0x00) == ~int8(0x00) == 0xFF
    assert ~uint8(0x01) == ~int8(0x01) == 0xFE
    assert ~uint8(0x7F) == ~int8(0x7F) == 0x80
    assert ~uint8(0x80) == ~int8(0x80) == 0x7F
    assert ~uint8(0xFF) == ~int8(0xFF) == 0x00

def test_nint_ops_binary():
    # Casts
    assert uint8(0xFF) + 1 == uint8(0)
    # Arithmetic
    assert uint8(3)  + uint8(2) == uint8(5)
    assert uint8(3)  - uint8(2) == uint8(1)
    assert uint8(3)  * uint8(2) == uint8(6)
    assert uint8(3)  / uint8(2) == uint8(1)
    assert uint8(3) // uint8(2) == uint8(1)
    assert uint8(7)  % uint8(5) == uint8(2)
    assert uint8(3) ** uint8(4) == uint8(81)
    # Logical
    assert uint16(0xF0F0) & uint16(0xFF00) == uint16(0xF000)
    assert uint16(0xF0F0) | uint16(0xFF00) == uint16(0xFFF0)
    assert uint16(0xF0F0) ^ uint16(0xFF00) == uint16(0x0FF0)
    # Shifts
    assert uint16(0x1234) >> 4 == uint16(0x0123)
    assert uint16(0x1234) << 4 == uint16(0x2340)

def test_nint_ops_reflected():
    # Casts
    assert 1 + uint8(0xFF) == uint8(0)
    # Arithmetic
    assert 3  + uint8(2) == uint8(5)
    assert 3  - uint8(2) == uint8(1)
    assert 3  * uint8(2) == uint8(6)
    assert 3  / uint8(2) == uint8(1)
    assert 3 // uint8(2) == uint8(1)
    assert 7  % uint8(5) == uint8(2)
    assert 3 ** uint8(4) == uint8(81)
    # Logical
    assert 0xF0F0 & uint16(0xFF00) == uint16(0xF000)
    assert 0xF0F0 | uint16(0xFF00) == uint16(0xFFF0)
    assert 0xF0F0 ^ uint16(0xFF00) == uint16(0x0FF0)
    # Shifts
    assert 0x1234 >> 4 == uint16(0x0123)
    assert 0x1234 << 4 == uint16(0x2340)

def test_nint_ops_inplace():
    # Casts
    v = nint( signed=True  );  v += nint( signed=True  );  assert v.s == True
    v = nint( signed=True  );  v += nint( signed=False );  assert v.s == True
    v = nint( signed=False );  v += nint( signed=True  );  assert v.s == False
    v = nint( signed=False );  v += nint( signed=False );  assert v.s == False
    v = nint( bits=8  );       v += nint( bits=8  );       assert v.b == 8
    v = nint( bits=8  );       v += nint( bits=16 );       assert v.b == 8
    v = nint( bits=16 );       v += nint( bits=8  );       assert v.b == 16
    v = nint( bits=16 );       v += nint( bits=16 );       assert v.b == 16
    # Arithmetic
    v = uint8(3);  v  += uint8(2);  assert v == uint8(5)
    v = uint8(3);  v  -= uint8(2);  assert v == uint8(1)
    v = uint8(3);  v  *= uint8(2);  assert v == uint8(6)
    v = uint8(3);  v  /= uint8(2);  assert v == uint8(1)
    v = uint8(3);  v //= uint8(2);  assert v == uint8(1)
    v = uint8(7);  v  %= uint8(5);  assert v == uint8(2)
    v = uint8(3);  v **= uint8(4);  assert v == uint8(81)
    # Logical
    v = uint16(0xF0F0);  v &= uint16(0xFF00);  assert v == uint16(0xF000)
    v = uint16(0xF0F0);  v |= uint16(0xFF00);  assert v == uint16(0xFFF0)
    v = uint16(0xF0F0);  v ^= uint16(0xFF00);  assert v == uint16(0x0FF0)
    # Shifts
    v = uint16(0x1234);  v >>= 4;  assert v == uint16(0x0123)
    v = uint16(0x1234);  v <<= 4;  assert v == uint16(0x2340)

def test_nint_ops_relational():
    # Casts
    assert int8(0x1) == 1
    assert int8(0x100) == 0
    # Signedness
    assert  int8(0x80) <  int8(0x7F)
    assert uint8(0x80) >  int8(0x7F)
    assert  int8(0x80) > uint8(0x7F)
    assert uint8(0x80) > uint8(0x7F)

#######################################
# Test: Native Floating-point values  #
#######################################

def test_nint():
    test_nint_values()
    test_nint_casts_implicit()
    test_nint_casts_explicit()
    test_nint_ops_type()
    test_nint_ops_unary()
    test_nint_ops_binary()
    test_nint_ops_reflected()
    test_nint_ops_inplace()
    test_nint_ops_relational()

def test_nfloat():
    return

def test():
    test_nint()
    test_nfloat()

if __name__ == '__main__':
    test()
