#!/usr/bin/env python

__doc__ = """
# An example of running ez_map to process a batch file
# BE VERY CAREFUL with this script, as it executes system calls. 
# To run:

alias mpython='mpirun -np [#nodes] `which mpipython.exe`'
mpython parallel_batch_raw.py [batchfile.txt]
"""

def runshell(input):
    """
    This function just calls popen on the input string, and the stdout is printed.
    """
    import mpi
    from os import popen
    print "%d of %d: executing: %s" % (mpi.world().rank, mpi.world().size, input)
    popen(input).readlines()
    return 0


if __name__ == "__main__":

    try:
        from pyina.parallel_map2 import parallel_map as parallel_map2

        import mpi
        world = mpi.world()
    
        inputlist = []
        if world.rank == 0:
            import sys
            batchfile = sys.argv[1]
            inputlist = open(batchfile).readlines()
        out = parallel_map2(runshell, inputlist)
    except:
        print __doc__


# End of file
