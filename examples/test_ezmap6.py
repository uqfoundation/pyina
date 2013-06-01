#!/usr/bin/env python

from pyina.mpi import Torque, SerialMapper

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Submit a non-parallel job to torque in the 'normal' queue..."
print "Using 5 items over 10 nodes and the default mapping strategy"
torque = Torque(queue='normal', timelimit='00:10')
pool = SerialMapper(10, scheduler=torque)
res = pool.map(host, range(5))
print pool
print '\n'.join(res)

# end of file
