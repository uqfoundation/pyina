#!/usr/bin/env python

from pyina.ez_map import ez_map
from pyina.mappers import *

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Evaluate 10 items on 1 node (w/ 1 ppn) using equalportion_mapper:"
res1 = ez_map(host, range(10), nnodes='1:ppn=1', mapper=equalportion_mapper) 
print '\n'.join(res1)
print ''

print "Evaluate 10 items on 1 node (w/ 2 ppn) using equalportion_mapper:"
res2 = ez_map(host, range(10), nnodes='1:ppn=2', mapper=equalportion_mapper) 
print '\n'.join(res2)
print ''

# end of file
