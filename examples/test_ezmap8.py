#!/usr/bin/env python

from pyina.launchers import TorqueMpiPool as Launcher
from pyina.mpi import _save, _debug

#_debug(True)
#_save(True)
def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Submit an mpi job to torque in the 'productionQ' queue..."
print "Using 15 items over 5 nodes and the worker pool strategy"
pool = Launcher('5:ppn=2', queue='productionQ', timelimit='20:00:00', workdir='.')
res = pool.map(host, range(15))
print pool
print '\n'.join(res)

print "hello from master"

# end of file
