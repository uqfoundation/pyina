#!/usr/bin/env python

__doc__ = """
# print rank - hostname info
# To run:

mpipython.exe machines.py [#nodes]
"""

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())
        

import sys
if len(sys.argv) > 1: nnodes = int(sys.argv[1])
else: nnodes = 1

try:
    from pyina.ez_map import ez_map
    hostnames = ez_map(host, range(nnodes), nnodes=nnodes)
    print '\n'.join(hostnames)
except:
    print __doc__


# end of file
