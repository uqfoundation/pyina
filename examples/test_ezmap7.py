#!/usr/bin/env python

from pyina.launchers import Mpi
from pyina.schedulers import Torque

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Submit an mpi job to torque in the 'weekendQ' queue..."
print "Using 10 items over 5 nodes and the scatter-gather strategy"
torque = Torque('5:ppn=2', queue='weekendQ', timelimit='20:00:00', workdir='.')
pool = Mpi(scheduler=torque, scatter=True)
res = pool.map(host, range(10))
print pool
print '\n'.join(res)

# end of file
