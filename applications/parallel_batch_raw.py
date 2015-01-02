#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2015 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

__doc__ = """
# An example of running ez_map to process a batch file
# BE VERY CAREFUL with this script, as it executes system calls. 
# To run:

alias mpython='mpirun -np [#nodes] `which python`'
mpython parallel_batch_raw.py [batchfile.txt]
"""

def runshell(input):
    """
    This function just calls popen on the input string, and the stdout is printed.
    """
    from pyina import mpi
    from subprocess import Popen, PIPE
    print "%d of %d: executing: %s" % (mpi.world.rank, mpi.world.size, input)
    pipe = Popen(input, shell=True, stdout=PIPE).stdout
    pipe.readlines()
    return 0


if __name__ == "__main__":

    try:
        from pyina.mpi_scatter import parallel_map as parallel_map2

        from pyina import mpi
        world = mpi.world
    
        inputlist = []
        if world.rank == 0:
            import sys
            batchfile = sys.argv[1]
            inputlist = open(batchfile).readlines()
        out = parallel_map2(runshell, inputlist)
    except:
        print __doc__


# End of file
