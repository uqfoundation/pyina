#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2025 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

from pyina.mpi import _save, _debug
from pyina.launchers import Pool as Mpi
from pyina.schedulers import Torque, Sheduled
if Scheduled != Torque:
    print('Torque scheduler is not available')
    exit()

#_debug(True)
#_save(True)
def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print("Submit an mpi job to torque in the 'productionQ' queue...")
print("Using 15 items over 5 nodes and the scatter-gather strategy")
torque = Torque('5:ppn=2', queue='productionQ', timelimit='20:00:00', workdir='.')
pool = Mpi(scheduler=torque, scatter=True)
res = pool.map(host, range(15))
print(pool)
print('\n'.join(res))

print("hello from master")

# end of file
