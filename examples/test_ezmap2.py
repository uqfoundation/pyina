#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

from pyina.launchers import MpiScatter, MpiPool

def play(Q):
    id, l = Q
    import numpy
    return "3 x %d = %d" % (id, numpy.sum(l))

def play2(id,l):
    import numpy
    return "3 x %d = %d" % (id, numpy.sum(l))

args = [ (i, range(3)*i) for i in range(5) ]
arg1 = [ i for i in range(5) ]
arg2 = [ range(3)*i for i in range(5) ]

print("Using 12 nodes and a worker pool...")
print('Evaluate a function that expects a n-tuple argument "map(f,args)"')
pool = MpiPool(12)
res1 = pool.map(play, args)
#res1 = map(play, args)
print(pool)
print('\n'.join(res1))
print('')

print('Evaluate a function that expects n arguments "map(f,arg1,arg2)"')
res2 = pool.map(play2, arg1, arg2)
#res2 = map(play2, arg1, arg2)
print(pool)
print('\n'.join(res2))

# end of file
