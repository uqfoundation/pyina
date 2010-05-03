#!/usr/bin/env python
#
# 

"""
# simple test of mpi communication to ports
# To run:

mpirun -np 4 `which mpipython.exe` test_ports.py
"""

import pyina, mystic
from mpi.Application import Application
import logging

#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(levelname)s %(message)s',
#                    datefmt='%a, %d %b %Y %H:%M:%S')

class SimpleApp(Application):

    def main(self):
        import mpi

        world = mpi.world()
        logging.info("I am rank %d of %d" % (world.rank, world.size))
        if world.rank == 0:
            for peer in range(1, world.size):
                port = world.port(pyina.mpi.MPI_ANY_SOURCE, tag=17)
                message = port.receive()
                print "[%d/%d]: received {%s}" % (world.rank, world.size, message)
        else:
            s = "My message is this: I am node %d " % world.rank
            logging.debug("%s" % s)
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
