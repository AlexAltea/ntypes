#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

import operator

def get_value(value, bits, signed):
    if isinstance(value, int_t):
        value = value.v
    mask = 2**bits - 1
    if signed and value & (1 << (bits - 1)):
        return value | ~mask
    else:
        return value & mask

# Promotions
def get_bits(value):
    return value.b if isinstance(value, int_t) else 64
def get_signed(value):
    return value.s if isinstance(value, int_t) else True

def promote_bits(lhs, rhs):
    return max(get_bits(lhs), get_bits(rhs))
def promote_signed(lhs, rhs):
    return get_signed(lhs) & get_signed(rhs)

# Native Integer
class int_t(object):
    def __init__(self, value=0, bits=32, signed=True):
        self.b = bits
        self.s = signed
        self.m = 2**bits - 1
        self.v = get_value(value, bits, signed)

    def __str__(self):
        return str(int(self))
    def __int__(self):
        return int(self.v)

    # Operation
    def op_binary_lhs(self, rhs, op):
        bits = promote_bits(self, rhs)
        signed = promote_signed(self, rhs)
        result = op(
            get_value(self, bits, signed),
            get_value(rhs, bits, signed))
        return int_t(result, bits, signed)

    def op_binary_rhs(self, lhs, op):
        bits = promote_bits(self, lhs)
        signed = promote_signed(self, lhs)
        result = op(
            get_value(lhs, bits, signed),
            get_value(self, bits, signed))
        return int_t(result, bits, signed)

    def op_rel(self, rhs, op):
        bits = promote_bits(self, rhs)
        signed = promote_signed(self, rhs)
        lhs_int = get_value(self, bits, signed)
        rhs_int = get_value(rhs, bits, signed)
        return op(lhs_int, rhs_int)

    def __add__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__add__)
    def __sub__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__sub__)
    def __mul__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__mul__)
    def __floordiv__  (self, rhs):  return self.op_binary_lhs(rhs, operator.__floordiv__)
    def __truediv__   (self, rhs):  return self.op_binary_lhs(rhs, operator.__floordiv__)
    def __mod__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__mod__)
    def __and__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__and__)
    def __or__        (self, rhs):  return self.op_binary_lhs(rhs, operator.__or__)
    def __xor__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__xor__)
    def __lshift__    (self, rhs):  return self.op_binary_lhs(rhs, operator.__lshift__)
    def __rshift__    (self, rhs):  return self.op_binary_lhs(rhs, operator.__rshift__)

    def __radd__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__add__)
    def __rsub__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__sub__)
    def __rmul__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__mul__)
    def __rfloordiv__ (self, lhs):  return self.op_binary_rhs(lhs, operator.__floordiv__)
    def __rtruediv__  (self, rhs):  return self.op_binary_lhs(rhs, operator.__floordiv__)
    def __rmod__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__mod__)
    def __rand__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__and__)
    def __ror__       (self, lhs):  return self.op_binary_rhs(lhs, operator.__or__)
    def __rxor__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__xor__)
    def __rlshift__   (self, lhs):  return self.op_binary_rhs(lhs, operator.__lshift__)
    def __rrshift__   (self, lhs):  return self.op_binary_rhs(lhs, operator.__rshift__)

    def __eq__        (self, rhs):  return self.op_rel(rhs, operator.__eq__)
    def __ne__        (self, rhs):  return self.op_rel(rhs, operator.__ne__)
    def __lt__        (self, rhs):  return self.op_rel(rhs, operator.__lt__)
    def __le__        (self, rhs):  return self.op_rel(rhs, operator.__le__)
    def __ge__        (self, rhs):  return self.op_rel(rhs, operator.__ge__)
    def __gt__        (self, rhs):  return self.op_rel(rhs, operator.__gt__)


# Shorthands
class int8_t(int_t):
    def __init__(self, value=0):
        super(int8_t, self).__init__(value, bits=8, signed=True)
class int16_t(int_t):
    def __init__(self, value=0):
        super(int16_t, self).__init__(value, bits=16, signed=True)
class int32_t(int_t):
    def __init__(self, value=0):
        super(int32_t, self).__init__(value, bits=32, signed=True)
class int64_t(int_t):
    def __init__(self, value=0):
        super(int64_t, self).__init__(value, bits=64, signed=True)

class uint8_t(int_t):
    def __init__(self, value):
        super(uint8_t, self).__init__(value, bits=8, signed=False)
class uint16_t(int_t):
    def __init__(self, value):
        super(uint16_t, self).__init__(value, bits=16, signed=False)
class uint32_t(int_t):
    def __init__(self, value):
        super(uint32_t, self).__init__(value, bits=32, signed=False)
class uint64_t(int_t):
    def __init__(self, value):
        super(uint64_t, self).__init__(value, bits=64, signed=False)
