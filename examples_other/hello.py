#!/usr/bin/env python

__doc__ = """
# get pyina._pyina to say hello
# To run:

alias mpython='mpirun -np [#nodes] `which mpipython.exe`'
mpython hello.py
"""

from pyre.applications.Script import Script

class HelloApp(Script):
    """
Get the C-bindings to say hello
    """
    class Inventory(Script.Inventory):
        import pyre.inventory

    def __init__(self):
        Script.__init__(self, 'HelloApp')
        return

    def _configure(self):
        Script._configure(self)

    def main(self, *args, **kwargs):
        import pyina
        print "Output of pyina._pyina.hello --> %s " % pyina._pyina.hello()
        return


if __name__ == "__main__":

    app = HelloApp()
    app.run()


# End of file
