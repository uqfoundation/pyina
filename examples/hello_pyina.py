#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

__doc__ = """
# get pyina to say 'hello'
# To run:

alias mpython='mpiexec -np [#nodes] `which python`'
mpython hello.py
"""

class HelloApp(object):
    """
Get pyina to say hello
    """
    def __call__(self, *args, **kwargs):
        from pyina import mpi
        print("hello from mpi.world.rank --> %s " % mpi.world.rank)
        return


if __name__ == "__main__":

    app = HelloApp()
    app()


# End of file
