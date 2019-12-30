#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

from pyina.launchers import TorqueMpiPool as Launcher
from pyina.mpi import _save, _debug

#_debug(True)
#_save(True)
def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print("Submit an mpi job to torque in the 'productionQ' queue...")
print("Using 15 items over 5 nodes and the worker pool strategy")
pool = Launcher('5:ppn=2', queue='productionQ', timelimit='20:00:00', workdir='.')
res = pool.map(host, range(15))
print(pool)
print('\n'.join(res))

print("hello from master")

# end of file
