#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

from pyina.launchers import Mpi

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print("Explicitly using the MPI launcher, we will execute...")
pool = Mpi(4)
print("10 items on 4 nodes using a worker pool:")
res1 = pool.map(host, range(10))
print(pool)
print('\n'.join(res1))
print('')

print("10 items on 4 nodes using scatter-gather:")
pool.scatter = True
res2 = pool.map(host, range(10))
print(pool)
print('\n'.join(res2))

# end of file
