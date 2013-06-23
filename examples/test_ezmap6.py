#!/usr/bin/env python

from pyina.launchers import SerialMapper
from pyina.schedulers import Torque
from pyina.mpi import _save, _debug

#_debug(True)
#_save(True)
def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Submit a non-parallel job to torque in the 'productionQ' queue..."
print "Using 5 items over 1 nodes and the default mapping strategy"
torque = Torque(queue='productionQ', timelimit='20:00:00', workdir='.')
pool = SerialMapper(scheduler=torque)
res = pool.map(host, range(5))
print pool
print '\n'.join(res)

# end of file
