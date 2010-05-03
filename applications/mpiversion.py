#!/usr/bin/env python

__doc__ = """
# finds the version of mpipython.exe
# To run:

mpipython.exe mpiversion.py
"""

from pyre.applications.Script import Script

class MPIVersionApp(Script):
    """
 Prints sys.version
    """
    class Inventory(Script.Inventory):
        import pyre.inventory

    def __init__(self):
        Script.__init__(self, 'MPIVersionApp')
        return

    def _configure(self):
        Script._configure(self)

    def main(self, *args, **kwargs):
        import sys
        print "Version of mpipython.exe: %s " % sys.version
       #import mpi
       #world = mpi.world()
       #f = open('mpiversion.%d.out' % world.rank ,'w')
       #f.write("Version of mpipython.exe: %s " % sys.version)
       #f.close()
        return


if __name__ == "__main__":

    try:
        import pyina
        app = MPIVersionApp()
        app.run()
    
    except:
        print __doc__


# End of file
