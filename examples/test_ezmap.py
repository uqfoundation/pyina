#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

from pyina.launchers import MpiScatter, MpiPool

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print("Evaluate 10 items on 3 nodes using a worker pool:")
pool = MpiPool(3)
res1 = pool.map(host, range(10)) 
print(pool)
print('\n'.join(res1))
print('')

print("Evaluate 10 items on 3 nodes using scatter-gather:")
scat = MpiScatter(3)
res2 = scat.map(host, range(10)) 
print(scat)
print('\n'.join(res2))
print('')

print("Evaluate 5 items on 2 nodes using a worker pool:")
pool.nodes = 2
res3 = pool.map(host, range(5))
print(pool)
print('\n'.join(res3))
print('')

print("Evaluate 5 items on 2 nodes using scatter-gather:")
scat.nodes = 2
res4 = scat.map(host, range(5))
print(scat)
print('\n'.join(res4))
print('')

#NOTE: bug? does worker pool perform correctly when nnodes > range ???
print("Evaluate 5 items on 10 nodes using worker pool:")
pool.nodes = 10
res5 = pool.map(host, range(5)) 
print(pool)
print('\n'.join(res5))
print('')

print("Evaluate 5 items on 10 nodes using scatter-gather:")
scat.nodes = 10
res6 = scat.map(host, range(5)) 
print(scat)
print('\n'.join(res6))

# end of file
