#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

__doc__ = """
# get all nodes to report
# To run:

alias mpython='mpiexec -np [#nodes] `which python`'
mpython nodes.py
"""


from pyina import mpi
world = mpi.world
print("Node (%d) of %d " % (world.rank, world.size))

# End of file
