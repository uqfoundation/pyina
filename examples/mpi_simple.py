#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
# Testing pyina.mpi.world.recv
# To run:

mpiexec -np 4 `which python` mpi_simple.py

of

python mpi_simple.py
""" 

import logging
import pyina

class SimpleApp(object):

    def __call__(self):
        from pyina import mpi
        stat = mpi.MPI.Status

        world = mpi.world
        logging.info("I am rank %d of %d" % (world.rank, world.size))
        if world.rank == 0:
            for peer in range(1, world.size):
                status = stat()
                message = world.recv(tag=17)
                print("node %d of %d: received {%s}" % (world.rank, world.size, message))
        else:
            s = "My message is this: I am node %d" % world.rank
            logging.debug("%s" % s)
            world.send(s, 0, 17)

        return


if __name__ == "__main__":

    app = SimpleApp()
    app()

# End of file
