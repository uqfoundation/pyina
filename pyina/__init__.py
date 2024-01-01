#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2024 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

# author, version, license, and long description
try: # the package is installed
    from .__info__ import __version__, __author__, __doc__, __license__
except: # pragma: no cover
    import os
    import sys
    parent = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    sys.path.append(parent)
    # get distribution meta info 
    from version import (__version__, __author__,
                         get_license_text, get_readme_as_rst)
    __license__ = get_license_text(os.path.join(parent, 'LICENSE'))
    __license__ = "\n%s" % __license__
    __doc__ = get_readme_as_rst(os.path.join(parent, 'README.md'))
    del os, sys, parent, get_license_text, get_readme_as_rst


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
    print (__doc__[-491:-118])
    return

# end of file
