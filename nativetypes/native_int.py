#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

import operator
import sys

# Helpers
def get_value(value, bits, signed):
    if isinstance(value, nint):
        value = value.v
    mask = 2**bits - 1
    if signed and value & (1 << (bits - 1)):
        return value | ~mask
    else:
        return value & mask

def ensure_native(lhs, rhs):
    assert isinstance(lhs, nint) or isinstance(rhs, nint)
    if not isinstance(lhs, nint):
        lhs = nint(lhs, rhs.b, rhs.s)
    if not isinstance(rhs, nint):
        rhs = nint(rhs, lhs.b, lhs.s)
    return lhs, rhs

# Promotions
def promote_bits(lhs, rhs):
    return max(lhs.b, rhs.b)
def promote_signed(lhs, rhs):
    return lhs.s & rhs.s

# Operators
def op_unary(value, op):
    bits = value.b
    signed = value.s
    result = op(get_value(value, bits, signed))
    return nint(result, bits, signed)

def op_binary(lhs, rhs, op):
    lhs, rhs = ensure_native(lhs, rhs)
    bits = promote_bits(lhs, rhs)
    signed = promote_signed(lhs, rhs)
    result = op(
        get_value(lhs, bits, signed),
        get_value(rhs, bits, signed))
    return nint(result, bits, signed)

def op_relational(lhs, rhs, op):
    lhs, rhs = ensure_native(lhs, rhs)
    bits = promote_bits(lhs, rhs)
    signed = promote_signed(lhs, rhs)
    return op(
        get_value(lhs, bits, signed),
        get_value(rhs, bits, signed))

# Native Integer
class nint(object):
    def __init__(self, value=0, bits=32, signed=True):
        assert bits >= 1, 'Support down to int1 only'
        self.b = bits
        self.s = signed
        self.m = (1 << bits) - 1
        self.set(value)

    # Bytes conversion
    @staticmethod
    def from_bytes(data, byteorder, bits, signed):
        if sys.version_info[0] < 3:
            if byteorder == 'little':
                data = data[::-1]
            value = int(data.encode('hex'), 16)
        else:
            value = int.from_bytes(data, byteorder)
        return nint(value, bits, signed)

    def to_bytes(self, byteorder):
        length = (self.b + 7) // 8
        if sys.version_info[0] < 3:
            data = '%x' % int(self)
            data = ('0' * (len(data) % 2) + data)
            data = data.zfill(length * 2).decode('hex')
            if byteorder == 'little':
                data = data[::-1]
            return data
        else:
            return int(self).to_bytes(length, byteorder)

    def set(self, value):
        if self.s and value & (1 << (self.b - 1)):
            self.v = value | ~self.m
        else:
            self.v = value & self.m

    def op_binary_inplace(self, value, op):
        result_int = op(self.v, value)
        self.set(result_int)
        return self

    # Utilities
    def min(self):
        return -(2 ** (self.b - 1)) * int(self.s)

    def max(self):
        return (2 ** (self.b - int(self.s))) - 1

    # Slicing
    def __getitem__(self, key):
        if isinstance(key, int):
            assert 0 <= key < self.b
            return bool((int(self) >> key) & 1)
        if isinstance(key, slice):
            assert 0 <= key.start < self.b
            assert 0 <= key.stop < self.b
            assert key.start < key.stop
            bits = key.stop - key.start
            mask = 2 ** bits - 1
            value = int(self) >> key.start
            return nint(value, bits, signed=False)

    # Conversion operations
    def __str__(self):
        return str(int(self))
    def __repr__(self):
        typename = type(self).__name__
        return '%s(%s)' % (typename, self)
    def __format__(self, format_spec):
        template = '{{:{}}}'.format(format_spec)
        return template.format(self.v)
    def __int__(self):
        return int(self.v)
    def __bool__(self):
        return bool(self.v)
    def __nonzero__(self):
        return bool(self.v)
    def __float__(self):
        return float(self.v)
    def __index__(self):
        return self.v.__index__()

    # Unary operations
    def __abs__(self):
        return op_unary(self, operator.__abs__)
    def __pos__(self):
        return op_unary(self, operator.__pos__)
    def __neg__(self):
        return op_unary(self, operator.__neg__)
    def __invert__(self):
        return op_unary(self, operator.__invert__)

    # Binary operations
    def __add__(self, rhs):
        return op_binary(self, rhs, operator.__add__)
    def __sub__(self, rhs):
        return op_binary(self, rhs, operator.__sub__)
    def __mul__(self, rhs):
        return op_binary(self, rhs, operator.__mul__)
    def __div__(self, rhs):
        return op_binary(self, rhs, operator.__floordiv__)
    def __floordiv__(self, rhs):
        return op_binary(self, rhs, operator.__floordiv__)
    def __truediv__(self, rhs):
        return op_binary(self, rhs, operator.__floordiv__)
    def __mod__(self, rhs):
        return op_binary(self, rhs, operator.__mod__)
    def __pow__(self, rhs):
        return op_binary(self, rhs, operator.__pow__)
    def __and__(self, rhs):
        return op_binary(self, rhs, operator.__and__)
    def __or__(self, rhs):
        return op_binary(self, rhs, operator.__or__)
    def __xor__(self, rhs):
        return op_binary(self, rhs, operator.__xor__)
    def __lshift__(self, rhs):
        return op_binary(self, rhs, operator.__lshift__)
    def __rshift__(self, rhs):
        return op_binary(self, rhs, operator.__rshift__)

    # Reflected binary operation
    def __radd__(self, lhs):
        return op_binary(lhs, self, operator.__add__)
    def __rsub__(self, lhs):
        return op_binary(lhs, self, operator.__sub__)
    def __rmul__(self, lhs):
        return op_binary(lhs, self, operator.__mul__)
    def __rdiv__(self, lhs):
        return op_binary(lhs, self, operator.__floordiv__)
    def __rfloordiv__(self, lhs):
        return op_binary(lhs, self, operator.__floordiv__)
    def __rtruediv__(self, lhs):
        return op_binary(lhs, self, operator.__floordiv__)
    def __rmod__(self, lhs):
        return op_binary(lhs, self, operator.__mod__)
    def __rpow__(self, lhs):
        return op_binary(lhs, self, operator.__pow__)
    def __rand__(self, lhs):
        return op_binary(lhs, self, operator.__and__)
    def __ror__(self, lhs):
        return op_binary(lhs, self, operator.__or__)
    def __rxor__(self, lhs):
        return op_binary(lhs, self, operator.__xor__)
    def __rlshift__(self, lhs):
        return op_binary(lhs, self, operator.__lshift__)
    def __rrshift__(self, lhs):
        return op_binary(lhs, self, operator.__rshift__)

    # In-place operations
    def __iadd__(self, v):
        return self.op_binary_inplace(v, operator.__add__)
    def __isub__(self, v):
        return self.op_binary_inplace(v, operator.__sub__)
    def __imul__(self, v):
        return self.op_binary_inplace(v, operator.__mul__)
    def __idiv__(self, v):
        return self.op_binary_inplace(v, operator.__floordiv__)
    def __ifloordiv__(self, v):
        return self.op_binary_inplace(v, operator.__floordiv__)
    def __itruediv__(self, v):
        return self.op_binary_inplace(v, operator.__floordiv__)
    def __imod__(self, v):
        return self.op_binary_inplace(v, operator.__mod__)
    def __ipow__(self, v):
        return self.op_binary_inplace(v, operator.__pow__)
    def __iand__(self, v):
        return self.op_binary_inplace(v, operator.__and__)
    def __ior__(self, v):
        return self.op_binary_inplace(v, operator.__or__)
    def __ixor__(self, v):
        return self.op_binary_inplace(v, operator.__xor__)
    def __ilshift__(self, v):
        return self.op_binary_inplace(v, operator.__lshift__)
    def __irshift__(self, v):
        return self.op_binary_inplace(v, operator.__rshift__)

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
def nint_type(name, bits, signed):
    def __init__(self, value=0):
        nint.__init__(self, value, bits, signed)
    @staticmethod
    def from_bytes(data, byteorder):
        return nint.from_bytes(data, byteorder, bits, signed)
    return type(name, (nint,), {
        "__init__": __init__,
        "from_bytes": from_bytes
    })

# Shorthands
int8   = nint_type('int8',   bits=8,  signed=True)
int16  = nint_type('int16',  bits=16, signed=True)
int32  = nint_type('int32',  bits=32, signed=True)
int64  = nint_type('int64',  bits=64, signed=True)
uint8  = nint_type('uint8',  bits=8,  signed=False)
uint16 = nint_type('uint16', bits=16, signed=False)
uint32 = nint_type('uint32', bits=32, signed=False)
uint64 = nint_type('uint64', bits=64, signed=False)
