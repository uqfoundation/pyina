#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
# simple test of mpi communication
# To run:

mpiexec -np 4 `which python` test_comm.py
"""

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

class SimpleApp(object):

    def __call__(self):
        from pyina import mpi

        world = mpi.world
        logging.info("I am rank %d of %d" % (world.rank, world.size))
        if world.rank == 0:
            for peer in range(1, world.size):
                message = world.recv(tag=17)
                print("node %d of %d: received {%s}" % (world.rank, world.size, message))
        else:
            s = "My message is this: I am node %d" % world.rank
            logging.debug("%s" % s)
            #XXX: set up a port with mpi4py?
            world.send("%s" % s, dest=0, tag=17)
        return


# main

if __name__ == "__main__":

    app = SimpleApp()
    app()

# End of file
