#!/usr/bin/env python

from pyina.ez_map import *

#XXX:: ez_map fails with NameError: global name 'func' is not defined
#XXX:: ez_map2 fails with RuntimeError: maximum recursion depth exceeded
#from mystic.models.poly import chebyshev8cost as func

def host(coeffs):
    from mystic.models.poly import chebyshev8cost as func
    return "x: %s --> %s" % (coeffs, func(coeffs))

from pyina.launchers import mpirun_launcher as mylauncher
params = [(i,0,-2*i,0,4*i,0,-2*i,0,i) for i in range(10)]

#res = ez_map(host, params, nnodes=4, launcher=mylauncher)
res = ez_map2(host, params, nnodes=4, launcher=mylauncher)
print '\n'.join(res)

# end of file
