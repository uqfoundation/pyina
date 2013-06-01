#!/usr/bin/env python

from pyina.mpi import TorqueMpiScatter

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Submit an mpi job to torque in the 'normal' queue..."
print "Using 15 items over 10 nodes and the scatter-gather strategy"
pool = TorqueMpiScatter('10:ppn=4', queue='normal', timelimit='00:10')
res = pool.map(host, range(15))
print pool
print '\n'.join(res)

print "hello from master"

# end of file
