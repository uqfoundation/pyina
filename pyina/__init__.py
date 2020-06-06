#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

# get version numbers, license, and long description
try:
    from pyina.info import this_version as __version__
    from pyina.info import readme as __doc__, license as __license__
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
import pyina.launchers as launchers
import pyina.schedulers as schedulers

# mappers
import pyina.mpi as mpi

# strategies
import pyina.mpi_scatter as mpi_scatter
import pyina.mpi_pool as mpi_pool

# tools
from .tools import *

# backward compatibility
parallel_map = mpi_pool
parallel_map.parallel_map = mpi_pool.parallel_map
parallel_map2 = mpi_scatter
parallel_map2.parallel_map = mpi_scatter.parallel_map
#import ez_map
#import mappers


def license():
    """print license"""
    print(__license__)
    return

def citation():
    """print citation"""
    print (__doc__[-485:-115])
    return

# end of file
