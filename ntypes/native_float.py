#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

import operator

# Helpers
def get_value(value, bits, signed):
    raise Exception('Unimplemented')

def ensure_native(lhs, rhs):
    assert isinstance(lhs, nfloat) or isinstance(rhs, nfloat)
    if not isinstance(lhs, nfloat):
        lhs = nfloat(lhs, rhs.e, rhs.f)
    if not isinstance(rhs, nfloat):
        rhs = nfloat(rhs, lhs.e, lhs.f)
    return lhs, rhs

# Promotions
# TODO

# Operators
def op_unary(value, op):
    raise Exception('Unimplemented')

def op_binary(lhs, rhs, op):
    lhs, rhs = ensure_native(lhs, rhs)
    raise Exception('Unimplemented')

def op_relational(lhs, rhs, op):
    lhs, rhs = ensure_native(lhs, rhs)
    raise Exception('Unimplemented')

# Native Integer
class nfloat(object):
    def __init__(self, value=0.0, exponent=8, fraction=23):
        self.e = exponent
        self.f = fraction
        self.set(value)

    def set(self, value):
        raise Exception('Unimplemented')

    def __str__(self):
        return str(int(self))
    def __int__(self):
        return int(float(self))
    def __float__(self):
        return float(self.v)

    def op_binary_inplace(self, value, op):
        result_int = op(self.v, value)
        self.set(result_int)
        return self

    # Unary operations
    def __abs__(self, value): return op_unary(self, operator.__abs__)
    def __pos__(self, value): return op_unary(self, operator.__pos__)
    def __neg__(self, value): return op_unary(self, operator.__neg__)
    def __inv__(self, value): return op_unary(self, operator.__inv__)

    # Binary operations
    def __add__       (self, rhs):  return op_binary(self, rhs, operator.__add__)
    def __sub__       (self, rhs):  return op_binary(self, rhs, operator.__sub__)
    def __mul__       (self, rhs):  return op_binary(self, rhs, operator.__mul__)
    def __floordiv__  (self, rhs):  return op_binary(self, rhs, operator.__floordiv__)
    def __truediv__   (self, rhs):  return op_binary(self, rhs, operator.__floordiv__)
    def __mod__       (self, rhs):  return op_binary(self, rhs, operator.__mod__)
    def __and__       (self, rhs):  return op_binary(self, rhs, operator.__and__)
    def __or__        (self, rhs):  return op_binary(self, rhs, operator.__or__)
    def __xor__       (self, rhs):  return op_binary(self, rhs, operator.__xor__)
    def __lshift__    (self, rhs):  return op_binary(self, rhs, operator.__lshift__)
    def __rshift__    (self, rhs):  return op_binary(self, rhs, operator.__rshift__)

    # Reflected binary operation
    def __radd__      (self, lhs):  return op_binary(lhs, self, operator.__add__)
    def __rsub__      (self, lhs):  return op_binary(lhs, self, operator.__sub__)
    def __rmul__      (self, lhs):  return op_binary(lhs, self, operator.__mul__)
    def __rfloordiv__ (self, lhs):  return op_binary(lhs, self, operator.__floordiv__)
    def __rtruediv__  (self, lhs):  return op_binary(lhs, self, operator.__floordiv__)
    def __rmod__      (self, lhs):  return op_binary(lhs, self, operator.__mod__)
    def __rand__      (self, lhs):  return op_binary(lhs, self, operator.__and__)
    def __ror__       (self, lhs):  return op_binary(lhs, self, operator.__or__)
    def __rxor__      (self, lhs):  return op_binary(lhs, self, operator.__xor__)
    def __rlshift__   (self, lhs):  return op_binary(lhs, self, operator.__lshift__)
    def __rrshift__   (self, lhs):  return op_binary(lhs, self, operator.__rshift__)

    # In-place operations
    def __iadd__      (self, v):  return self.op_binary_inplace(v, operator.__add__)
    def __isub__      (self, v):  return self.op_binary_inplace(v, operator.__sub__)
    def __imul__      (self, v):  return self.op_binary_inplace(v, operator.__mul__)
    def __ifloordiv__ (self, v):  return self.op_binary_inplace(v, operator.__floordiv__)
    def __itruediv__  (self, v):  return self.op_binary_inplace(v, operator.__floordiv__)
    def __imod__      (self, v):  return self.op_binary_inplace(v, operator.__mod__)
    def __iand__      (self, v):  return self.op_binary_inplace(v, operator.__and__)
    def __ior__       (self, v):  return self.op_binary_inplace(v, operator.__or__)
    def __ixor__      (self, v):  return self.op_binary_inplace(v, operator.__xor__)
    def __ilshift__   (self, v):  return self.op_binary_inplace(v, operator.__lshift__)
    def __irshift__   (self, v):  return self.op_binary_inplace(v, operator.__rshift__)

    def __eq__        (self, rhs):  return op_relational(self, rhs, operator.__eq__)
    def __ne__        (self, rhs):  return op_relational(self, rhs, operator.__ne__)
    def __lt__        (self, rhs):  return op_relational(self, rhs, operator.__lt__)
    def __le__        (self, rhs):  return op_relational(self, rhs, operator.__le__)
    def __ge__        (self, rhs):  return op_relational(self, rhs, operator.__ge__)
    def __gt__        (self, rhs):  return op_relational(self, rhs, operator.__gt__)


# Shorthands
class float16(nfloat):
    def __init__(self, value=0.0):
        super(float32, self).__init__(value, exponent=5, fraction=10)
class float32(nfloat):
    def __init__(self, value=0.0):
        super(float32, self).__init__(value, exponent=8, fraction=23)
class float64(nfloat):
    def __init__(self, value=0.0):
        super(float64, self).__init__(value, exponent=11, fraction=52)
