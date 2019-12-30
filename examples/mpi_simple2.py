#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
# Testing pyina.mpi.world.bcast
# To run:

mpiexec -np 4 `which python` mpi_simple2.py

python mpi_simple2.py
""" 

import logging

class SimpleApp(object):

    def __call__(self):
        from pyina import mpi

        world = mpi.world
        logging.info("I am rank %d of %d" % (world.rank, world.size))
        root = 0
        if world.rank == root:
            str = "hello world"
            nn = world.bcast(str, root)
            print("Master has: %s " % nn)
        else:
            nn = world.bcast("", root)
            print("Worker (%d) has: %s " % (world.rank, nn))
        return


if __name__ == "__main__":

    app = SimpleApp()
    app()

# End of file
