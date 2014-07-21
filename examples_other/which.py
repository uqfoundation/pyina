#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

__doc__ = """
# check which python mpirun is executing
# To run (in parallel):

mpirun -np 1 python which.py
"""

import sys
print(sys.version)
print(sys.executable)

try:
    import mpi4py
    print("mpi4py is installed")
except ImportError:
    print("mpi4py not installed")
    exit()
except:
    print("mpi4py install broken")
    exit()

try:
    import pathos
    print("pathos is installed")
except ImportError:
    print("pathos not installed")
    exit()
except:
    print("pathos install broken")
    exit()

try:
    import numpy
    import dill
    import pox
    print("all dependencies are installed")
except ImportError:
    print("all dependencies not installed")
    exit()
except:
    print("dependency install broken")
    exit()

try:
    import pyina
    print("pyina is installed")
except ImportError:
    print("pyina not installed")
except:
    print("pyina install broken")


# End of file
