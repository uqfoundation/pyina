#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                       Patrick Hung & Mike McKerns, Caltech
#                        (C) 1997-2010  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
MPI Constants
"""


#import pyina._pyina
# this file is imported by top level __init__, hell can break
# loose if we use absollute imports
import _pyina
import const as mpi
import sys

mpi.mpiconsts = _pyina.mpiconsts()

for (k, v) in mpi.mpiconsts.iteritems():
    mpi.__dict__[k] = v

sys.modules[__name__].__dict__.__delitem__('k')
sys.modules[__name__].__dict__.__delitem__('v')

# End of file
