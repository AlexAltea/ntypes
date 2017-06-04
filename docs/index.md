Native Types documentation
==========================

Disclaimer: This is a rather informal description.

## Introduction

Following terms are used.
* *Native type*: Type provided by the *ntypes* library, e.g. `int_t` or specializations like `int8_t` or `uint32_t`.
* *Python type*: Type provided by Python, e.g. `int`.


## Integer values

### Operators

Following operators are implemented:

* __Unary operators__: Expressions: `<op> value` resulting in `c`. Such operators require `value` to be *native integers*. `abs`, `+`, `-`, `~`.
* __Binary operators__: Expressions: `lhs <op> rhs` resulting in `c`. Such operators require either `lhs` or `rhs` to be *native integers*. `+`, `-`, `*`, `/`, `//`, `%`, `&`, `|`, `^`, `>>`, `<<`.
* __Inplace operators__: Expressions: `self <op> other`. `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `&=`, `|=`, `^=`, `>>=`, `<<=`.
* __Relational operators__: `==`, `!=`, `<`, `<=`, `=>`, `>`.

This corresponds to the following Python operators:
`__abs__`, `__pos__`, `__neg__`, `__inv__`, `__ceil__`, `__floor__`, `__round__`, `__trunc__`, `__abs__`, `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__mod__`, `__and__`, `__or__`, `__xor__`, `__lshift__`, `__rshift__`, `__radd__`, `__rsub__`, `__rmul__`, `__rfloordiv__`, `__rtruediv__`, `__rmod__`, `__rand__`, `__ror__`, `__rxor__`, `__rlshift__`, `__rrshift__`, `__iadd__`, `__isub__`, `__imul__`, `__ifloordiv__`, `__itruediv__`, `__imod__`, `__iand__`, `__ior__`, `__ixor__`, `__ilshift__`, `__irshift__`, `__eq__`, `__ne__`, `__lt__`, `__le__`, `__ge__`, `__gt__`.

Following operators have not been implemented as no-operation: `__ceil__`, `__floor__`, `__round__`, `__trunc__`.

All operators except conversion and boolean operators will return a `nint`. To ensure this, and to provide a C-like syntax the `__truediv__` operator will invoke the `__floordiv__` operator.

### Conversion rules

* __Binary operators__:
  1. Both `lhs` and `rhs` are converted into *native types*.
      * If `lhs` is a *Python type* convert it to `rhs`'s *native type*.
      * If `rhs` is a *Python type* convert it to `lhs`'s *native type*.
  2. Result size in bits will be the maximum of the size of `lhs` and `rhs`.
  3. If either `lhs` or `rhs` are unsigned types, then both `lhs` and `rhs` will be treated as unsigned types
  
* __Relational operators__: Same conversions as for *binary operators*.

* __Inplace operators__:
  1. If `other` is a *Python type*, convert it to `self`'s *native type*.


## Floating-point values

TODO
