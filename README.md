Native Types
============

![](https://api.travis-ci.org/AlexAltea/ntypes.svg?branch=master)
![](https://coveralls.io/repos/AlexAltea/ntypes/badge.svg?branch=master)
![](https://img.shields.io/pypi/v/ntypes.svg)

Emulate native integer and floating-point types in Python 2.x and 3.x.

Install the package via:

```bash
pip install ntypes
````

## Comparison

There are several alternatives to *ntypes*, specifically: `ctypes`, `numpy`, `fixedint`, `cinc`. However, *ntypes* also offers some features not present across all these packages.

|                  | *ntypes*     | [*ctypes*](https://docs.python.org/3/library/ctypes.html) | [*numpy*](https://pypi.python.org/pypi/numpy) | [*fixedint*](https://pypi.python.org/pypi/fixedint) | [*cinc*](https://pypi.python.org/pypi/cinc) |
|------------------|:------------:|:--------:|:-------:|:----------:|:------:|
| Floating-point   | __Yes__      | Yes      | Yes     | -          | -      |
| Implicit casts   | __Yes__      | -        | -       | Yes        | -      |
| Custom aliases   | __Yes__      | -        | -       | -          | -      |
| High-performance | -            | -        | -       | -          | Yes    |

Other reasons might include that `numpy` is way too large dependency to be imported just for the sake of fixed-size integers.

## Examples

...

## FAQ

> __Why call this *ntypes*?__

No reason in particular. Easy to remember, similar to "*ctypes*". The word "*native*" might be misleading though. 
