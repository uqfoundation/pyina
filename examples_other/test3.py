#!/usr/bin/env python
#
# 

"""
# Testing _pyina.bcastString
# To run:

mpipython.exe test3.py
""" 


from mpi.Application import Application
import logging

#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(levelname)s %(message)s',
#                    datefmt='%a, %d %b %Y %H:%M:%S')

class SimpleApp(Application):

    def main(self):
        import mpi
        from pyina import _pyina

        world = mpi.world()
        logging.info("I am rank %d of %d" % (world.rank, world.size))
	root = 0
        if world.rank == root:
            str = "hello world"
            nn = _pyina.bcastString(world.handle(), root, str)
            print "Master has: %s " % nn
        else:
            nn = _pyina.bcastString(world.handle(), root, "")
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
    #journal.debug("pyinaqString").activate()

    app = SimpleApp()
    app.run()

# End of file
