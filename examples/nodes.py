#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2015 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

__doc__ = """
# get all nodes to report
# To run:

alias mpython='mpirun -np [#nodes] `which python`'
mpython nodes.py
"""


from pyina import mpi
world = mpi.world
print "Node (%d) of %d " % (world.rank, world.size)

# End of file
