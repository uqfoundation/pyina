#!/usr/bin/env python

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
    from pyina.mpi import MpiPool
    pool = MpiPool()
    pool.nodes = nnodes
    hostnames = pool.map(host, range(nnodes))
    print '\n'.join(hostnames)
except:
    print __doc__


# end of file
