#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2018 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

__doc__ = """
# get pyina to say 'hello'
# To run:

alias mpython='mpiexec -np [#nodes] `which python`'
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
