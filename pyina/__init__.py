#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                              Mike McKerns, Caltech
#                        (C) 1997-2012  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# get version numbers, license, and long description
try:
    from info import this_version as __version__
    from info import readme as __doc__, license as __license__
except ImportError:
    msg = """First run 'python setup.py build' to build pyina."""
    raise ImportError(msg)

__author__ = 'Mike McKerns'

__doc__ = """
""" + __doc__

__license__ = """
""" + __license__

# shortcuts
from mpi4py import MPI as mpi
mpi.world = mpi.COMM_WORLD
# (also: mpi.world.rank, mpi.world.size)

# launchers
import launchers
import schedulers

# mappers
#import pp_map
import ez_map
import mappers

# strategies
import parallel_map, parallel_map2

# tools
from tools import *

def license():
    """print license"""
    print __license__
    return

def citation():
    """print citation"""
    print __doc__[-499:-140]
    return

# end of file
