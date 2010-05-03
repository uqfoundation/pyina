#!/usr/bin/env python

from pyina.ez_map import ez_map
from pyina.mappers import *

def play(Q):
    id, l = Q
    import numpy
    return "Sum: %d -- %d" % (id, numpy.sum(l))

def play2(id,l):
    import numpy
    return "Sum: %d -- %d" % (id, numpy.sum(l))

args = [ (i, range(3)*i) for i in range(5) ]
arg1 = [ i for i in range(5) ]
arg2 = [ range(3)*i for i in range(5) ]

res = ez_map(play, args, nnodes=12, mapper=carddealer_mapper)
#res = map(play, args)
res2 = ez_map(play2, arg1, arg2, nnodes=12, mapper=carddealer_mapper)
#res2 = map(play2, arg1, arg2)

print 'n-tuple arg...'
print '\n'.join(res)
print '\nn-args...'
print '\n'.join(res2)

# end of file
