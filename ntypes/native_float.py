#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

import math
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

    def set(self, value):
        assert isinstance(value, float)
        value = struct.pack('d', value)
        value = struct.unpack('Q', value)[0]
        self.vs.set(value >> (63))
        self.ve.set(value >> (63 - self.e))
        self.vm.set(value >> (52 - self.m))
        self.vm |= (value >> (51 - min(51, self.m))) & 1

    def __str__(self):
        return str(float(self))
    def __int__(self):
        return int(float(self))
    def __bool__(self):
        return bool(self.v)
    def __nonzero__(self):
        return bool(self.v)
    def __float__(self):
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
        sign = (-1) ** self.vs.v
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


# Shorthands
class float16(nfloat):
    def __init__(self, value=0.0):
        super(float32, self).__init__(value, exponent=5, mantissa=10)
class float32(nfloat):
    def __init__(self, value=0.0):
        super(float32, self).__init__(value, exponent=8, mantissa=23)
class float64(nfloat):
    def __init__(self, value=0.0):
        super(float64, self).__init__(value, exponent=11, mantissa=52)
