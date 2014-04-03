#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

__doc__ = """
# print a listing of compute nodes as (rank, hostname)
# To run:

python machines.py [#nodes]
"""

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())
        

import sys
if len(sys.argv) > 1: nnodes = int(sys.argv[1])
else: nnodes = 1

try:
    from pyina.launchers import MpiPool
    pool = MpiPool()
    pool.nodes = nnodes
    hostnames = pool.map(host, range(nnodes))
    print '\n'.join(hostnames)
except:
    print __doc__


# end of file
