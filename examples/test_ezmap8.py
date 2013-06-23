#!/usr/bin/env python

from pyina.launchers import TorqueMpiPool as Launcher

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Submit an mpi job to torque in the 'weekendQ' queue..."
print "Using 15 items over 10 nodes and the worker pool strategy"
pool = Launcher('10:ppn=4', queue='weekendQ', timelimit='20:00:00', workdir='.')
res = pool.map(host, range(15))
print pool
print '\n'.join(res)

print "hello from master"

# end of file
