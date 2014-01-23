#!/usr/bin/env python
 
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 Caltech
# License: 3-clause BSD

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

# launchers
import launchers
import schedulers

# mappers
import mpi

# strategies
import mpi_scatter, mpi_pool

# tools
from tools import *

# backward compatibility
parallel_map = mpi_pool
parallel_map.parallel_map = mpi_pool.parallel_map
parallel_map2 = mpi_scatter
parallel_map2.parallel_map = mpi_scatter.parallel_map
#import ez_map
#import mappers


def license():
    """print license"""
    print __license__
    return

def citation():
    """print citation"""
    print __doc__[-499:-140]
    return

# end of file
