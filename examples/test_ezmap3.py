#!/usr/bin/env python

from pyina.ez_map import ez_map
from pyina.mappers import *

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

from pyina.launchers import mpirun_launcher as mylauncher
res = ez_map(host, range(10), nnodes=4, launcher=mylauncher, \
                                       mapper=carddealer_mapper)
                                       #mapper=equalportion_mapper)
print '\n'.join(res)

# end of file
