#!/usr/bin/env python
#
# 

"""
# Testing pyina.mpi.world.recv
# To run:

python test1.py
""" 

from mpi.Application import Application
import logging
import pyina

MPI_ANY_SOURCE = pyina.mpi.ANY_SOURCE

class SimpleApp(Application):

    class Inventory(Application.Inventory):
        import pyre.inventory
        nseg = pyre.inventory.int("nseg", default=200)
        nseg.meta['tip'] = 'divides the interval [0,1] into how many segments ?'

    def main(self):
        from pyina import mpi

        nsegs = self.inventory.nseg
        world = mpi.world
        logging.info("I am rank %d of %d" % (world.rank, world.size))
        if world.rank == 0:
            for peer in range(1, world.size):
                status = mpi.Status()
                message = world.recv(source=MPI_ANY_SOURCE,tag=17)
                print "[%d/%d]: received {%s}" % (world.rank, world.size, message)
        else:
            s = "My message is this: I am node %d " % world.rank
            logging.debug("%s" % s)
            world.send(s, 0, 17)

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
    journal.info("pyina.mpi.world.recv").activate()
    journal.debug("pyina.mpi.world.recv").activate()

    app = SimpleApp()
    app.run()

# End of file
