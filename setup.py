#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import setuptools

NTYPES_VERSION = '1.0.1'
NTYPES_REPOSITORY_URL = 'https://github.com/AlexAltea/ntypes'
NTYPES_DOWNLOAD_URL = 'https://github.com/AlexAltea/ntypes/tarball/' + NTYPES_VERSION

# Description
NTYPES_DESCRIPTION = """Native Types
============

.. image:: https://api.travis-ci.org/AlexAltea/ntypes.svg?branch=master
    :target: https://travis-ci.org/AlexAltea/ntypes/
    
.. image:: https://coveralls.io/repos/github/AlexAltea/ntypes/badge.svg?branch=master
    :target: https://coveralls.io/github/AlexAltea/ntypes?branch=master
    
.. image:: https://img.shields.io/pypi/v/ntypes.svg
    :target: https://pypi.python.org/pypi/ntypes

Emulate native integer and floating-point types in Python 2.x and 3.x.

More information at: https://github.com/AlexAltea/ntypes

Install the package via:

.. code:: bash

    pip install nativetypes

Comparison
----------

There are several alternatives to *ntypes*, specifically: ``ctypes``,
``numpy``, ``fixedint``, ``cinc``. However, *ntypes* also offers some
features not present across all these packages.

+--------------------+------------+---------------+--------------+-----------------+-------------+
|                    | *ntypes*   | `*ctypes*`_   | `*numpy*`_   | `*fixedint*`_   | `*cinc*`_   |
+====================+============+===============+==============+=================+=============+
| Floating-point     | **Yes**    | Yes           | Yes          | -               | -           |
+--------------------+------------+---------------+--------------+-----------------+-------------+
| Implicit casts     | **Yes**    | -             | -            | Yes             | -           |
+--------------------+------------+---------------+--------------+-----------------+-------------+
| Custom aliases     | **Yes**    | -             | -            | -               | -           |
+--------------------+------------+---------------+--------------+-----------------+-------------+
| Slicing            | **Yes**    | -             | -            | Yes             | -           |
+--------------------+------------+---------------+--------------+-----------------+-------------+
| High-performance   | -          | Yes           | -            | -               | Yes         |
+--------------------+------------+---------------+--------------+-----------------+-------------+

Other reasons might include that ``numpy`` is way too large dependency
to be imported just for the sake of fixed-size integers. Note that
high-performance is not a goal for this library.

FAQ
---

    **What’s the point of this library?**

This library is syntactic sugar for developers and reverse-engineers
that want to port code from C/C++/ASM into Python and need all this
low-level quirks: Overflows, underflows, casts, etc.

Although Python prevents many headaches with its arbitrarily large
integers, writing code equivalent to functions written in C/C++/ASM
means masking every operation, and doing dozens of conversions manually
between distinct types. This library does that work for you.

    **Where can read about the API?**

The documentation is quite incomplete at this moment. Check the examples
below or check the tests.

    **Why is this package nativetypes**?

I’m not good with naming. Ideally, I would have registered *ntypes*
instead, but that one was apparently taken.

Examples
--------

-  Fast inverse square root (see `[1]`_)

.. code:: python

    def rsqrt(number: float32):
        i = reinterpret_cast(int32, number)
        i = 0x5F3759DF - (i >> 1)
        y = reinterpret_cast(float32, i)
        y *= (1.5 - (0.5 * number * y * y))
        return y

-  Ranbyus DGA (see `[2]`_):

   .. code:: python

       def ranbyus_dga(timestamp):
       s = uint32(self.seed)
       t1 = uint32(t.day)
       t2 = uint32(t.month)
       t3 = uint32(t.year)

       name = ""
       for i in xrange(12):
           t1 = (t1 >> 15) ^ (16 * (t1 & 0x1FFF ^ 4 * (t1 ^ s)))
           t2 = ((t2 ^ (4 * t2)) >>  8) ^ ((t2 & 0xFFFFFFFE) * 14)
           t3 = ((t3 ^ (7 * t3)) >> 11) | ((t3 & 0xFFFFFFF0) << 17)
           s = (s >> 6) ^ (((t1 + 8 * s) << 8) & 0x3FFFF00)
           name += string.ascii_lowercase[int(t1 ^ t2 ^ t3) % 25]

       # TLD omitted
       return name

.. _[1]: https://en.wikipedia.org/wiki/Fast_inverse_square_root#Overview_of_the_code
.. _[2]: https://www.govcert.admin.ch/blog/25/when-mirai-meets-ranbyus

.. _*ctypes*: https://docs.python.org/3/library/ctypes.html
.. _*numpy*: https://pypi.python.org/pypi/numpy
.. _*fixedint*: https://pypi.python.org/pypi/fixedint
.. _*cinc*: https://pypi.python.org/pypi/cinc
"""

setuptools.setup(
    name='nativetypes',
    version=NTYPES_VERSION,
    description='Native integer and floating-point type emulation',
    long_description=NTYPES_DESCRIPTION,
    license='MIT',
    author='Alexandro Sanchez Bach',
    author_email='alexandro@phi.nz',
    url=NTYPES_REPOSITORY_URL,
    download_url=NTYPES_DOWNLOAD_URL,
    packages=['nativetypes'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
    ],
)
