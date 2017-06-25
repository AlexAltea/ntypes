#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

from nativetypes import *

def test_nfloat_values():
    assert float(float16(-1.0)) == -1.0
    assert float(float16(-0.0)) == -0.0
    assert float(float16(+0.0)) == +0.0
    assert float(float16(+1.0)) == +1.0
    assert float(float32(-1.0)) == -1.0
    assert float(float32(-0.0)) == -0.0
    assert float(float32(+0.0)) == +0.0
    assert float(float32(+1.0)) == +1.0
    # Precision
    import math
    assert float(float32(math.e)) != math.e
    assert float(float32(math.pi)) != math.pi

def test_nfloat_aliases():
    f8_type = nfloat_type('f', exponent=4, mantissa=3)
    f8_value = f8_type(0.0)
    assert f8_value.e == 4 and f8_value.m == 3

def test_nfloat_bytes():
    # bytes to nfloat
    assert float32.from_bytes(b'\x3f\x80\x00\x00', byteorder='big') == 1.0
    assert float32.from_bytes(b'\x00\x00\x80\x3f', byteorder='little') == 1.0
    # nfloat to bytes
    assert float32(1.0).to_bytes(byteorder='big') == b'\x3f\x80\x00\x00'
    assert float32(1.0).to_bytes(byteorder='little') == b'\x00\x00\x80\x3f'
    assert len(nfloat(exponent=4, mantissa= 3).to_bytes(byteorder='big')) == 1
    assert len(nfloat(exponent=4, mantissa= 4).to_bytes(byteorder='big')) == 2
    assert len(nfloat(exponent=5, mantissa=10).to_bytes(byteorder='big')) == 2
    assert len(nfloat(exponent=5, mantissa=11).to_bytes(byteorder='big')) == 3
    # Reinterpret cast
    assert reinterpret_cast(float32, int32(0x3F800000)) == 1.0

def test_nfloat_ops_type():
    inf = float('inf')
    nan = float('nan')
    # String
    assert str(float32(-0.5)) == str(-0.5)
    assert str(float32(-0.0)) == str(-0.0)
    assert str(float32(+0.0)) == str(+0.0)
    assert str(float32(+1.0)) == str(+1.0)
    assert str(float32(+inf)) == str(+inf)
    assert str(float32(+nan)) == str(+nan)
    # Representation
    assert repr(float32(0.0)) == 'float32(0.0)'
    assert repr(float64(1.0)) == 'float64(1.0)'
    assert repr(float64(nan)) == 'float64(nan)'
    assert repr(float64(inf)) == 'float64(inf)'
    # Format
    assert '{0}'.format(float32(-0.5)) == str(-0.5)
    assert '{0}'.format(float32(-0.5)) == str(+0.0)
    assert '{0}'.format(float32(-0.5)) == str(-1.0)
    assert '{0}'.format(float32(-0.5)) == str(+1.0)
    assert '{0}'.format(float32(-0.5)) == str(+inf)
    assert '{0}'.format(float32(-0.5)) == str(+nan)
    # Integer
    assert int(float32(-0.5)) == int(-0.5)
    assert int(float32(-0.0)) == int(-0.0)
    assert int(float32(+0.0)) == int(+0.0)
    assert int(float32(+1.0)) == int(+1.0)
    # Boolean
    assert bool(float32(-0.5)) == bool(-0.5)
    assert bool(float32(-0.0)) == bool(-0.0)
    assert bool(float32(+0.0)) == bool(+0.0)
    assert bool(float32(+1.0)) == bool(+1.0)
    assert bool(float32(+inf)) == bool(+inf)
    assert bool(float32(+nan)) == bool(+nan)
    # Float
    assert float(float32(-0.5)) == float(-0.5)
    assert float(float32(-0.0)) == float(-0.0)
    assert float(float32(+0.0)) == float(+0.0)
    assert float(float32(+1.0)) == float(+1.0)
    assert float(float32(+inf)) == float(+inf)
    assert float(float32(+nan)) != float(+nan)

def test_nfloat_ops_unary():
    inf = float('inf')
    nan = float('nan')
    # Casts
    assert abs(nfloat( exponent=4 )).e == 4
    assert abs(nfloat( exponent=8 )).e == 8
    assert abs(nfloat( mantissa=4 )).m == 4
    assert abs(nfloat( mantissa=8 )).m == 8
    # Absolute value
    assert abs(float32(+0.0)) == abs(float32(-0.0)) == +0.0
    assert abs(float32(+0.5)) == abs(float32(-0.5)) == +0.5
    assert abs(float32(+inf)) == abs(float32(-inf)) == +inf
    # Plus
    assert +(float32(+0.0)) == +0.0
    assert +(float32(-0.0)) == -0.0
    assert +(float32(+0.5)) == +0.5
    assert +(float32(-0.5)) == -0.5
    assert +(float32(+inf)) == +inf
    assert +(float32(-inf)) == -inf
    # Minus
    assert -(float32(+0.0)) == -0.0
    assert -(float32(-0.0)) == +0.0
    assert -(float32(+0.5)) == -0.5
    assert -(float32(-0.5)) == +0.5
    assert -(float32(+inf)) == -inf
    assert -(float32(-inf)) == +inf

def test_nfloat_ops_binary():
    # Signedness (nfloat + nfloat)
    assert (nfloat( exponent=4 ) + nfloat( exponent=4 )).e == 4
    assert (nfloat( exponent=4 ) + nfloat( exponent=8 )).e == 8
    assert (nfloat( exponent=8 ) + nfloat( exponent=4 )).e == 8
    assert (nfloat( exponent=8 ) + nfloat( exponent=8 )).e == 8
    # Size (nfloat + nfloat)
    assert (nfloat( mantissa=4 ) + nfloat( mantissa=4 )).m == 4
    assert (nfloat( mantissa=4 ) + nfloat( mantissa=8 )).m == 8
    assert (nfloat( mantissa=8 ) + nfloat( mantissa=4 )).m == 8
    assert (nfloat( mantissa=8 ) + nfloat( mantissa=8 )).m == 8
    # Signedness (nfloat + float)
    assert (nfloat( exponent=4 ) + 0.0).e == 4
    assert (nfloat( exponent=8 ) + 0.0).e == 8
    # Size (nfloat + float)
    assert (nfloat( mantissa=4 ) + 0.0).m == 4
    assert (nfloat( mantissa=8 ) + 0.0).m == 8
    # Arithmetic
    assert float32(3.0) +  float32(2.0) == float32(5.0)
    assert float32(3.0) -  float32(2.0) == float32(1.0)
    assert float32(3.0) *  float32(2.0) == float32(6.0)
    assert float32(3.0) /  float32(2.0) == float32(1.5)
    assert float32(3.0) // float32(2.0) == float32(1.0)
    assert float32(7.0) %  float32(5.0) == float32(2.0)
    assert float32(3.0) ** float32(4.0) == float32(81.0)

def test_nfloat_ops_reflected():
    # Exponent size (float <op> nfloat)
    assert (0.0 + nfloat( exponent=4 )).e == 4
    assert (0.0 + nfloat( exponent=8 )).e == 8
    assert (0.0 + nfloat( exponent=4 )).e == 4
    assert (0.0 + nfloat( exponent=8 )).e == 8
    # Mantissa size (float <op> nfloat)
    assert (0.0 + nfloat( mantissa=4 )).m == 4
    assert (0.0 + nfloat( mantissa=8 )).m == 8
    assert (0.0 + nfloat( mantissa=4 )).m == 4
    assert (0.0 + nfloat( mantissa=8 )).m == 8
    # Arithmetic
    assert 3.0  + float32(2.0) == float32(5.0)
    assert 3.0  - float32(2.0) == float32(1.0)
    assert 3.0  * float32(2.0) == float32(6.0)
    assert 3.0  / float32(2.0) == float32(1.5)
    assert 3.0 // float32(2.0) == float32(1.0)
    assert 7.0  % float32(5.0) == float32(2.0)
    assert 3.0 ** float32(4.0) == float32(81.0)

def test_nfloat_ops_inplace():
    # Exponent size (nfloat <op>= nfloat)
    v = nfloat( exponent=4 );  v += nfloat( exponent=4 );  assert v.e == 4
    v = nfloat( exponent=4 );  v += nfloat( exponent=8 );  assert v.e == 4
    v = nfloat( exponent=8 );  v += nfloat( exponent=4 );  assert v.e == 8
    v = nfloat( exponent=8 );  v += nfloat( exponent=8 );  assert v.e == 8
    # Mantissa size (nfloat <op>= nfloat)
    v = nfloat( mantissa=4 );  v += nfloat( mantissa=4 );  assert v.m == 4
    v = nfloat( mantissa=4 );  v += nfloat( mantissa=8 );  assert v.m == 4
    v = nfloat( mantissa=8 );  v += nfloat( mantissa=4 );  assert v.m == 8
    v = nfloat( mantissa=8 );  v += nfloat( mantissa=8 );  assert v.m == 8
    # Arithmetic
    v = float32(3.0);  v  += float32(2.0);  assert v == float32(5.0)
    v = float32(3.0);  v  -= float32(2.0);  assert v == float32(1.0)
    v = float32(3.0);  v  *= float32(2.0);  assert v == float32(6.0)
    v = float32(3.0);  v  /= float32(2.0);  assert v == float32(1.5)
    v = float32(3.0);  v //= float32(2.0);  assert v == float32(1.0)
    v = float32(7.0);  v  %= float32(5.0);  assert v == float32(2.0)
    v = float32(3.0);  v **= float32(4.0);  assert v == float32(81.0)

def test_nfloat_ops_relational():
    # Casts
    assert float32(-1.0) == -1.0
    assert float64(+1.0) == +1.0
    assert float32(+2.0) == float32(+2.0)
    assert float32(-2.0) == float64(-2.0)
    # Operations
    assert (float32(0.0) == float32(0.0)) == True
    assert (float32(1.0) == float32(0.0)) == False
    assert (float32(0.0) == float32(1.0)) == False
    assert (float32(0.0) != float32(0.0)) == False
    assert (float32(1.0) != float32(0.0)) == True
    assert (float32(0.0) != float32(1.0)) == True
    assert (float32(0.0) <  float32(0.0)) == False
    assert (float32(1.0) <  float32(0.0)) == False
    assert (float32(0.0) <  float32(1.0)) == True
    assert (float32(0.0) <= float32(0.0)) == True
    assert (float32(1.0) <= float32(0.0)) == False
    assert (float32(0.0) <= float32(1.0)) == True
    assert (float32(0.0) >  float32(0.0)) == False
    assert (float32(1.0) >  float32(0.0)) == True
    assert (float32(0.0) >  float32(1.0)) == False
    assert (float32(0.0) >= float32(0.0)) == True
    assert (float32(1.0) >= float32(0.0)) == True
    assert (float32(0.0) >= float32(1.0)) == False
    # NaN
    nan = float('nan')
    assert (float32(nan) == float32(1.0)) == False
    assert (float32(nan) != float32(1.0)) == True
    assert (float32(nan) <  float32(1.0)) == False
    assert (float32(nan) <= float32(1.0)) == False
    assert (float32(nan) >= float32(1.0)) == False
    assert (float32(nan) >  float32(1.0)) == False
    # Infinite
    inf = float('inf')
    assert (float32(inf) == float32(1.0)) == False
    assert (float32(inf) != float32(1.0)) == True
    assert (float32(inf) <  float32(1.0)) == False
    assert (float32(inf) <= float32(1.0)) == False
    assert (float32(inf) >= float32(1.0)) == True
    assert (float32(inf) >  float32(1.0)) == True
