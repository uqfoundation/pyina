#!/usr/bin/env python
#
# 

"""
# Testing _pyina.receiveString
# To run:

mpipython.exe test2.py
""" 

from mpi.Application import Application
import logging
import pyina

MPI_ANY_SOURCE = pyina.mpi.MPI_ANY_SOURCE

#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(levelname)s %(message)s',
#                    datefmt='%a, %d %b %Y %H:%M:%S')

class SimpleApp(Application):

    class Inventory(Application.Inventory):
        import pyre.inventory
        nseg = pyre.inventory.int("nseg", default=200)
        nseg.meta['tip'] = 'divides the interval [0,1] into how many segments ?'

    def main(self):
        import mpi
        from pyina import _pyina

        nsegs = self.inventory.nseg
        world = mpi.world()
        logging.info("I am rank %d of %d" % (world.rank, world.size))
        if world.rank == 0:
            for peer in range(1, world.size):
                (message,status) = _pyina.receiveString(world.handle(), MPI_ANY_SOURCE, 17)
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
    journal.info("pyina.receiveString").activate()
    journal.debug("pyina.receiveString").activate()

    app = SimpleApp()
    app.run()

# End of file
