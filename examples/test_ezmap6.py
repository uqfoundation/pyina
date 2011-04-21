#!/usr/bin/env python

from pyina.ez_map import ez_map2 as ez_map
from pyina.launchers import torque_launcher

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Submit a non-parallel job to torque in the 'normal' queue..."
print "Using 5 items over 10 nodes and the default mapping strategy"
res = ez_map(host, range(5), nnodes=10, launcher=torque_launcher,\
             queue='normal', timelimit='00:10')
print '\n'.join(res)

# end of file
