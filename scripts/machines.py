#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

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
