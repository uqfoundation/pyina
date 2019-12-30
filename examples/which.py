#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

__doc__ = """
# check which python mpirun is executing
# To run (in parallel):

mpiexec -np 1 python which.py
"""

import sys
print((sys.version))
print((sys.executable))

try:
    import mpi4py
    print(("mpi4py %s is installed" % getattr(mpi4py, '__version__', '')))
except ImportError:
    print("mpi4py not installed")
    exit()
except:
    print("mpi4py install broken")
    exit()

try:
    import pathos
    print(("pathos %s is installed" % getattr(pathos, '__version__', '')))
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
    print(("pyina %s is installed" % getattr(pyina, '__version__', '')))
except ImportError:
    print("pyina not installed")
except:
    print("pyina install broken")


# End of file
