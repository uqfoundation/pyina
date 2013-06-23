#!/usr/bin/env python

from pyina.launchers import SerialMapper
from pyina.schedulers import Torque

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Submit a non-parallel job to torque in the 'weekendQ' queue..."
print "Using 5 items over 10 nodes and the default mapping strategy"
torque = Torque(queue='weekendQ', timelimit='20:00:00', workdir='.')
pool = SerialMapper(10, scheduler=torque)
res = pool.map(host, range(5))
print pool
print '\n'.join(res)

# end of file
