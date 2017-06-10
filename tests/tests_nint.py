#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

from ntypes import *

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

def test_nint_aliases():
    s7_type = nint_type('s5', bits=7, signed=True)
    u9_type = nint_type('u9', bits=9, signed=False)
    s7_value = s7_type(0)
    u9_value = u9_type(0)
    assert s7_value.b == 7 and s7_value.s == True
    assert u9_value.b == 9 and u9_value.s == False

def test_nint_bytes():
    # bytes to nint
    assert int16.from_bytes(b'\x00\x01', byteorder='big') == 1
    assert int16.from_bytes(b'\x00\x01', byteorder='little') == 256
    assert nint.from_bytes(b'\x12\x34', byteorder='big', bits=12, signed=False) == 0x234
    # nint to bytes
    assert int16(0x0001).to_bytes(byteorder='big') == b'\x00\x01'
    assert int16(0x0001).to_bytes(byteorder='little') == b'\x01\x00'
    assert nint(0x234, bits=12, signed=False).to_bytes(byteorder='big') == b'\x02\x34'
    assert len(nint(bits=1, signed=False).to_bytes(byteorder='big')) == 1
    assert len(nint(bits=8, signed=False).to_bytes(byteorder='big')) == 1
    assert len(nint(bits=9, signed=False).to_bytes(byteorder='big')) == 2
    # Reinterpret cast
    assert reinterpret_cast(int32, float32(1.0)) == 0x3F800000

def test_nint_slicing():
    # By index
    assert int8(0b1001)[0] == True
    assert int8(0b1001)[1] == False
    assert int8(0b1001)[2] == False
    assert int8(0b1001)[3] == True
    # By slice
    assert int8(0b1001)[0:2] == 1
    assert int8(0b1001)[1:3] == 4

def test_nint_utils():
    assert int8().min() == -0x80
    assert int8().max() == +0x7F
    assert uint8().min() == +0x00
    assert uint8().max() == +0xFF

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
    # Signedness (nint + nint)
    assert (nint( signed=True  ) + nint( signed=True  )).s == True
    assert (nint( signed=True  ) + nint( signed=False )).s == False
    assert (nint( signed=False ) + nint( signed=True  )).s == False
    assert (nint( signed=False ) + nint( signed=False )).s == False
    # Size (nint + nint)
    assert (nint( bits=8  ) + nint( bits = 8  )).b == 8
    assert (nint( bits=8  ) + nint( bits = 16 )).b == 16
    assert (nint( bits=16 ) + nint( bits = 8  )).b == 16
    assert (nint( bits=16 ) + nint( bits = 16 )).b == 16
    # Signedness (nint + int)
    assert (nint( signed=True  ) + 0).s == True
    assert (nint( signed=False ) + 0).s == False
    # Size (nint + int)
    assert (nint( bits=8  ) + 0).b == 8
    assert (nint( bits=16 ) + 0).b == 16
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
    # Signedness (int + nint)
    assert (0 + nint( signed=True  )).s == True
    assert (0 + nint( signed=False )).s == False
    assert (0 + nint( signed=True  )).s == True
    assert (0 + nint( signed=False )).s == False
    # Size (int + nint)
    assert (0 + nint( bits = 8  )).b == 8
    assert (0 + nint( bits = 16 )).b == 16
    assert (0 + nint( bits = 8  )).b == 8
    assert (0 + nint( bits = 16 )).b == 16
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
    assert 0x1234 >> uint16(4) == uint16(0x0123)
    assert 0x1234 << uint16(4) == uint16(0x2340)

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
    # Operations
    assert (uint8(0x00) == uint8(0x00)) == True
    assert (uint8(0x01) == uint8(0x00)) == False
    assert (uint8(0x00) == uint8(0x01)) == False
    assert (uint8(0x00) != uint8(0x00)) == False
    assert (uint8(0x01) != uint8(0x00)) == True
    assert (uint8(0x00) != uint8(0x01)) == True
    assert (uint8(0x00) <  uint8(0x00)) == False
    assert (uint8(0x01) <  uint8(0x00)) == False
    assert (uint8(0x00) <  uint8(0x01)) == True
    assert (uint8(0x00) <= uint8(0x00)) == True
    assert (uint8(0x01) <= uint8(0x00)) == False
    assert (uint8(0x00) <= uint8(0x01)) == True
    assert (uint8(0x00) >  uint8(0x00)) == False
    assert (uint8(0x01) >  uint8(0x00)) == True
    assert (uint8(0x00) >  uint8(0x01)) == False
    assert (uint8(0x00) >= uint8(0x00)) == True
    assert (uint8(0x01) >= uint8(0x00)) == True
    assert (uint8(0x00) >= uint8(0x01)) == False
