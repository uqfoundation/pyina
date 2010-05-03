#!/usr/bin/env mpipython.exe
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Patrick Hung, Caltech
#                        (C) 1998-2006  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
# Some basic tests.
# To run:

mpipython.exe test1.py
"""

from pyina import _pyina
import mpi

def test1():
    """
tests whether the module complains properly.

>>> _pyina.test(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
TypeError: Expecting a CObject as argument 0
    """
    pass


def test2():
    """
tests whether the module complains properly.

>>> _pyina.test('hello')
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
TypeError: Expecting a CObject as argument 0
    """
    pass

def test3():
    """
tests whether the module can accept a Commuicator CObject.

>>> x = mpi.world()
>>> c = _pyina.test(x.handle())
    """
    pass

def test4():
    """
tests MPI_ANY_TAG

>>> assert(_pyina.mpiconsts())
    """
    pass


if __name__=='__main__':
    import doctest
    doctest.testmod(verbose=True)

# End of file
