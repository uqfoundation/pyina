#!/usr/bin/env python

from pyina.ez_map import ez_map2 as ez_map
from pyina.launchers import mpirun_launcher
from pyina.launchers import torque_launcher
from pyina.schedulers import torque_scheduler
from pyina.mappers import carddealer_mapper, equalportion_mapper

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Submit an mpi job to torque in the 'normal' queue..."
print "Using 15 items over 10 nodes and the 'equalportion' mapping strategy"
res = ez_map(host, range(15), nnodes="10:ppn=4", launcher=mpirun_launcher,\
             queue='normal', timelimit='00:10', scheduler=torque_scheduler,\
             mapper=equalportion_mapper)
print '\n'.join(res)

print "hello from master"

# end of file
