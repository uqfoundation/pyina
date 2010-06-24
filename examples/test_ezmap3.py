#!/usr/bin/env python

from pyina.ez_map import ez_map
from pyina.mappers import *

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Explicitly using the MPI launcher, we will execute..."
from pyina.launchers import mpirun_launcher as mylauncher
print "10 items on 4 nodes using carddealer_mapper:"
res1 = ez_map(host, range(10), nnodes=4, launcher=mylauncher, \
                                        mapper=carddealer_mapper)
print '\n'.join(res1)
print ''

print "10 items on 4 nodes using equalportion_mapper:"
res2 = ez_map(host, range(10), nnodes=4, launcher=mylauncher, \
                                        mapper=equalportion_mapper)
print '\n'.join(res2)

# end of file
