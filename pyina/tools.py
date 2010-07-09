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
Various mpi python tools

Main function exported are::
    - ensure_mpi: make sure the script is called by mpi-enabled python
    - get_workload: get the workload the processor is responsible for

"""

def ensure_mpi(size = 1, doc = None):
    """
 ensure that mpi-enabled python is being called with the appropriate size

 inputs:
   - size: minimum required size of the MPI world [default = 1]
   - doc: error string to throw if size restriction is violated
    """
    if doc == None:
        doc = "Error: Requires MPI-enabled python with size >= %s" % size
    from mpi4py import MPI as mpi
    world = mpi.COMM_WORLD
    mpisize = world.Get_size()
    mpirank = world.Get_rank()
    if mpisize < size:
        if mpirank == 0: print doc
        import sys
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
   #ensure_mpi(size=3)
    import doctest
    doctest.testmod(verbose=True)

# End of file
