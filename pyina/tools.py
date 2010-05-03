#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                       Patrick Hung & Mike McKerns, Caltech
#                        (C) 1998-2010  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
Various mpipython tools

Main function exported are::
    - ensure_mpi: make sure that the script is called through mpipython
    - get_workload: get the workload the processor is responsible for

"""

def ensure_mpi(doc = "Requires mpipython."):
    """
 ensure that mpipython is being called
    """
    import mpi, sys
    from mystic import helputil
    if mpi.world().size == 0:
        helputil.paginate(doc)
        sys.exit()
    return

def get_workload(myid, nproc, popsize):
    """
 returns the workload that this processor is responsible for
    """
    from math import ceil
    n1 = nproc
    n2 = popsize
    iend = 0
    for i in range(nproc):
        ibegin = iend
        ai = int( ceil( 1.0*n2/n1 ))
        n2 = n2 - ai
        n1 = n1 - 1
        iend = iend + ai
        if i==myid:
           break
    return (ibegin, iend)


if __name__=='__main__':
    import doctest
    doctest.testmod(verbose=True)

# End of file
