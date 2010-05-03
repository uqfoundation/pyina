#!/usr/bin/env python

__doc__ = """
# get all nodes to report
# To run:

alias mpython='mpirun -np [#nodes] `which mpipython.exe`'
mpython nodes.py
"""


import mpi
world = mpi.world()
print "Node (%d) of %d " % (world.rank, world.size)

# End of file
