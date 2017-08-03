#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
# Testing pyina.mpi.world.bcast
# To run:

python mpipyre2.py
""" 


from mpi.Application import Application
import logging

class SimpleApp(Application):

    def main(self):
        from pyina import mpi

        world = mpi.world
        logging.info("I am rank %d of %d" % (world.rank, world.size))
	root = 0
        if world.rank == root:
            str = "hello world"
            nn = world.bcast(str, root)
            print "Master has: %s " % nn
        else:
            nn = world.bcast("", root)
            print "Slave (%d) has: %s " % (world.rank, nn)
        return

    def _defaults(self):
        self.inventory.launcher.inventory.nodes = 4

    def __init__(self):
        Application.__init__(self, "simple")
        return


# main

if __name__ == "__main__":
    import journal
    #journal.info("mpirun").activate()
    #journal.debug("pyina.mpi.world.bcast").activate()

    app = SimpleApp()
    app.run()

# End of file
