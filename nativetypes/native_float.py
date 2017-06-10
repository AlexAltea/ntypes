#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

import operator
import struct

from .native_int import *

# Helpers
def ensure_native(lhs, rhs):
    assert isinstance(lhs, nfloat) or isinstance(rhs, nfloat)
    if not isinstance(lhs, nfloat):
        lhs = nfloat(lhs, rhs.e, rhs.m)
    if not isinstance(rhs, nfloat):
        rhs = nfloat(rhs, lhs.e, lhs.m)
    return lhs, rhs

# Promotions
def promote_exponent(lhs, rhs):
    return max(lhs.e, rhs.e)
def promote_mantissa(lhs, rhs):
    return max(lhs.m, rhs.m)

# Operators
def op_unary(value, op):
    exponent = value.e
    mantissa = value.m
    result = op(float(value))
    return nfloat(result, exponent, mantissa)

def op_binary(lhs, rhs, op):
    lhs, rhs = ensure_native(lhs, rhs)
    exponent = promote_exponent(lhs, rhs)
    mantissa = promote_mantissa(lhs, rhs)
    result = op(float(lhs), float(rhs))
    return nfloat(result, exponent, mantissa)

def op_relational(lhs, rhs, op):
    lhs, rhs = ensure_native(lhs, rhs)
    exponent = promote_exponent(lhs, rhs)
    mantissa = promote_mantissa(lhs, rhs)
    return op(float(lhs), float(rhs))

# Native Float
class nfloat(object):
    def __init__(self, value=0.0, exponent=8, mantissa=23):
        assert exponent <= 11, 'Support up to float64 only'
        assert mantissa <= 52, 'Support up to float64 only'
        self.e = exponent
        self.m = mantissa
        # Value
        self.vs = nint(bits=1)
        self.ve = nint(bits=exponent, signed=False)
        self.vm = nint(bits=mantissa, signed=False)
        self.set(value)

    # Bytes conversion
    @staticmethod
    def from_bytes(data, byteorder, exponent, mantissa):
        bits = 1 + exponent + mantissa
        value = int(nint.from_bytes(data, byteorder, bits=bits, signed=False))
        result = nfloat(0.0, exponent, mantissa)
        result.vs.set(value >> (mantissa + exponent))
        result.ve.set(value >> (mantissa))
        result.vm.set(value)
        return result

    def to_bytes(self, byteorder):
        value = 0
        value |= int(self.vm)
        value |= int(self.ve) << (self.m)
        value |= int(self.vs) << (self.m + self.e)
        bits = 1 + self.e + self.m
        return nint(value, bits=bits, signed=False).to_bytes(byteorder)

    def set(self, value):
        assert isinstance(value, float)
        value = struct.pack('d', value)
        value = struct.unpack('Q', value)[0]
        self.vs.set(value >> (63))
        # Exponent
        ve = (value >> 52) & 0x7FF
        if not ve:
            self.ve.set(0)
        else:
            src_bits = 11
            dst_bits = self.e
            exp_min = - 2 ** (dst_bits - 1) + 2
            exp_max = + 2 ** (dst_bits - 1) + 0
            ve -= (2 ** (src_bits - 1)) - 1
            ve = min(max(ve, exp_min), exp_max)
            ve += (2 ** (dst_bits - 1)) - 1
            self.ve.set(ve)
        # Mantissa
        self.vm.set(value >> (52 - self.m))
        self.vm |= (value >> (51 - min(51, self.m))) & 1

    def __str__(self):
        return str(float(self))
    def __repr__(self):
        typename = type(self).__name__
        return '%s(%s)' % (typename, self)
    def __int__(self):
        return int(float(self))
    def __bool__(self):
        return bool(float(self))
    def __nonzero__(self):
        return bool(float(self))
    def __float__(self):
        sign = (-1) ** self.vs.v
        # Non-numbers
        if self.ve == self.ve.max():
            if self.vm == 0:
                return float('inf') * sign
            return float('nan')
        denormalized = (self.ve == 0)
        # Exponent
        exponent = -(2 ** (self.e - 1)) + 2
        if not denormalized:
            exponent += self.ve.v - 1
        # Mantissa
        mantissa = 0.0 if denormalized else 1.0
        for i in range(1, self.m + 1):
            mantissa += ((self.vm.v >> (self.m - i)) & 1) * (2 ** (-i))
        # Value
        value = mantissa * (2 ** exponent)
        return sign * value

    def op_binary_inplace(self, value, op):
        result_float = op(float(self), float(value))
        self.set(result_float)
        return self

    # Unary operations
    def __abs__(self):
        return op_unary(self, operator.__abs__)
    def __pos__(self):
        return op_unary(self, operator.__pos__)
    def __neg__(self):
        return op_unary(self, operator.__neg__)

    # Binary operations
    def __add__(self, rhs):
        return op_binary(self, rhs, operator.__add__)
    def __sub__(self, rhs):
        return op_binary(self, rhs, operator.__sub__)
    def __mul__(self, rhs):
        return op_binary(self, rhs, operator.__mul__)
    def __div__(self, rhs):
        return op_binary(self, rhs, operator.__div__)
    def __floordiv__(self, rhs):
        return op_binary(self, rhs, operator.__floordiv__)
    def __truediv__(self, rhs):
        return op_binary(self, rhs, operator.__truediv__)
    def __mod__(self, rhs):
        return op_binary(self, rhs, operator.__mod__)
    def __pow__(self, rhs):
        return op_binary(self, rhs, operator.__pow__)

    # Reflected binary operation
    def __radd__(self, lhs):
        return op_binary(lhs, self, operator.__add__)
    def __rsub__(self, lhs):
        return op_binary(lhs, self, operator.__sub__)
    def __rmul__(self, lhs):
        return op_binary(lhs, self, operator.__mul__)
    def __rdiv__(self, lhs):
        return op_binary(lhs, self, operator.__div__)
    def __rfloordiv__(self, lhs):
        return op_binary(lhs, self, operator.__floordiv__)
    def __rtruediv__(self, lhs):
        return op_binary(lhs, self, operator.__truediv__)
    def __rmod__(self, lhs):
        return op_binary(lhs, self, operator.__mod__)
    def __rpow__(self, lhs):
        return op_binary(lhs, self, operator.__pow__)

    # In-place operations
    def __iadd__(self, v):
        return self.op_binary_inplace(v, operator.__add__)
    def __isub__(self, v):
        return self.op_binary_inplace(v, operator.__sub__)
    def __imul__(self, v):
        return self.op_binary_inplace(v, operator.__mul__)
    def __idiv__(self, v):
        return self.op_binary_inplace(v, operator.__div__)
    def __ifloordiv__(self, v):
        return self.op_binary_inplace(v, operator.__floordiv__)
    def __itruediv__(self, v):
        return self.op_binary_inplace(v, operator.__truediv__)
    def __imod__(self, v):
        return self.op_binary_inplace(v, operator.__mod__)
    def __ipow__(self, v):
        return self.op_binary_inplace(v, operator.__pow__)

    # Boolean operations
    def __eq__(self, rhs):
        return op_relational(self, rhs, operator.__eq__)
    def __ne__(self, rhs):
        return op_relational(self, rhs, operator.__ne__)
    def __lt__(self, rhs):
        return op_relational(self, rhs, operator.__lt__)
    def __le__(self, rhs):
        return op_relational(self, rhs, operator.__le__)
    def __ge__(self, rhs):
        return op_relational(self, rhs, operator.__ge__)
    def __gt__(self, rhs):
        return op_relational(self, rhs, operator.__gt__)


# Aliases
def nfloat_type(name, exponent, mantissa):
    def __init__(self, value=0.0):
        nfloat.__init__(self, value, exponent, mantissa)
    @staticmethod
    def from_bytes(data, byteorder):
        return nfloat.from_bytes(data, byteorder, exponent, mantissa)
    return type(name, (nfloat,), {
        "__init__": __init__,
        "from_bytes": from_bytes
    })

# Shorthands
float16 = nfloat_type('float16', exponent=5,  mantissa=10)
float32 = nfloat_type('float32', exponent=8,  mantissa=23)
float64 = nfloat_type('float64', exponent=11, mantissa=52)
