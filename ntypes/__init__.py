#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

import operator

class int_t(object):
    def __init__(self, value=0, bits=32, signed=True):
        self.b = bits
        self.s = signed
        self.m = 2**bits - 1
        if signed and value & (1 << (bits-1)):
            self.v = value | ~self.m
        else:
            self.v = value & self.m

    def __str__(self):
        return str(int(self))
    def __int__(self):
        return int(self.v)

    def op_binary_lhs(self, rhs, op):
        bits = self.b
        signed = self.s
        if isinstance(rhs, int_t):
            bits = max(bits, rhs.b)
            signed = self.s & rhs.s
        result = op(self.v, rhs)
        return int_t(result, bits, signed)

    def op_binary_lhs(self, lhs, op):
        bits = self.b
        signed = self.s
        if isinstance(lhs, int_t):
            bits = max(bits, lhs.b)
            signed = self.s & lhs.s
        result = op(lhs, self.v)
        return int_t(result, bits, signed)

    def op_rel(self, rhs, op):
        return op(self.v, int(rhs))

    def __add__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__add__)
    def __sub__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__sub__)
    def __mul__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__mul__)
    def __floordiv__  (self, rhs):  return self.op_binary_lhs(rhs, operator.__floordiv__)
    def __mod__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__mod__)
    def __and__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__and__)
    def __or__        (self, rhs):  return self.op_binary_lhs(rhs, operator.__or__)
    def __xor__       (self, rhs):  return self.op_binary_lhs(rhs, operator.__xor__)
    def __lshift__    (self, rhs):  return self.op_binary_lhs(rhs, operator.__lshift__)
    def __rshift__    (self, rhs):  return self.op_binary_lhs(rhs, operator.__rshift__)

    def __radd__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__radd__)
    def __rsub__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__rsub__)
    def __rmul__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__rmul__)
    def __rfloordiv__ (self, lhs):  return self.op_binary_rhs(lhs, operator.__rfloordiv__)
    def __rmod__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__rmod__)
    def __rand__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__rand__)
    def __ror__       (self, lhs):  return self.op_binary_rhs(lhs, operator.__ror__)
    def __rxor__      (self, lhs):  return self.op_binary_rhs(lhs, operator.__rxor__)
    def __rlshift__   (self, lhs):  return self.op_binary_rhs(lhs, operator.__rlshift__)
    def __rrshift__   (self, lhs):  return self.op_binary_rhs(lhs, operator.__rrshift__)

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
