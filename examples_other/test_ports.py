#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
# simple test of mpi communication to ports
# To run:

mpiexec -np 4 `which python` test_ports.py
"""

import mystic
from mpi.Application import Application
import logging

class SimpleApp(Application):

    def main(self):
        from pyina import mpi

        world = mpi.world
        logging.info("I am rank %d of %d" % (world.rank, world.size))
        if world.rank == 0:
            for peer in range(1, world.size):
                #FIXME: How to set up a port in mpi4py?
                port = world.port(mpi.ANY_SOURCE, tag=17)
                message = port.receive()
                print "[%d/%d]: received {%s}" % (world.rank, world.size, message)
        else:
            s = "My message is this: I am node %d " % world.rank
            logging.debug("%s" % s)
            #FIXME: How to set up a port in mpi4py?
            port = world.port(peer=0, tag=17)
            port.send("%s" % s)

        return

    def _defaults(self):
        self.inventory.launcher.inventory.nodes = 4

    def __init__(self):
        Application.__init__(self, "simple")
        return


# main

if __name__ == "__main__":
    import journal
    journal.info("mpirun").activate()
    journal.debug("simple").activate()

    app = SimpleApp()
    app.run()

# End of file
