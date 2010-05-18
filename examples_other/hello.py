#!/usr/bin/env python

__doc__ = """
# get pyina to say 'hello'
# To run:

alias mpython='mpirun -np [#nodes] `which python`'
mpython hello.py
"""

from pyre.applications.Script import Script

class HelloApp(Script):
    """
Get pyina to say hello
    """
    class Inventory(Script.Inventory):
        import pyre.inventory

    def __init__(self):
        Script.__init__(self, 'HelloApp')
        return

    def _configure(self):
        Script._configure(self)

    def main(self, *args, **kwargs):
        from pyina import mpi
        print "hello from mpi.world.rank --> %s " % mpi.world.rank
        return


if __name__ == "__main__":

    app = HelloApp()
    app.run()


# End of file
