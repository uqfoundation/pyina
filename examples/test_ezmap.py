#!/usr/bin/env python

from pyina.ez_map import ez_map
from pyina.mappers import *

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

"""
print "Evaluate 10 items on 3 nodes using carddealer_mapper:"
res1 = ez_map(host, range(10), nnodes=3, mapper=carddealer_mapper) 
print '\n'.join(res1)
print ''

print "Evaluate 10 items on 3 nodes using equalportion_mapper:"
res2 = ez_map(host, range(10), nnodes=3, mapper=equalportion_mapper) 
print '\n'.join(res2)
print ''
"""

print "Evaluate 5 items on 2 nodes using carddealer_mapper:"
res3 = ez_map(host, range(5), nnodes=2, mapper=carddealer_mapper)
print '\n'.join(res3)
print ''

print "Evaluate 5 items on 2 nodes using equalportion_mapper:"
res4 = ez_map(host, range(5), nnodes=2, mapper=equalportion_mapper)
print '\n'.join(res4)
print ''

#NOTE: bug? does carddealer perform correctly when nnodes > range ???
print "Evaluate 5 items on 10 nodes using carddealer_mapper:"
res5 = ez_map(host, range(5), nnodes=10, mapper=carddealer_mapper) 
print '\n'.join(res5)
print ''

print "Evaluate 5 items on 10 nodes using equalportion_mapper:"
res6 = ez_map(host, range(5), nnodes=10, mapper=equalportion_mapper) 
print '\n'.join(res6)

# end of file
