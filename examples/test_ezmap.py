#!/usr/bin/env python

from pyina.ez_map import ez_map
from pyina.mappers import *

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

res = ez_map(host, range(10), nnodes=3, mapper=carddealer_mapper) 
#res = ez_map(host, range(10), nnodes=3, mapper=equalportion_mapper) 
#res = ez_map(host, range(5), nnodes=2, mapper=carddealer_mapper)
#res = ez_map(host, range(5), nnodes=2, mapper=equalportion_mapper)
#res = ez_map(host, range(5), nnodes=10, mapper=carddealer_mapper) 
#res = ez_map(host, range(5), nnodes=10, mapper=equalportion_mapper) 
#NOTE: bug?  map algorithm performs correctly when nnodes > range ???

print '\n'.join(res)
    

# end of file
