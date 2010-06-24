#!/usr/bin/env python

from pyina.ez_map import *

#XXX:: ez_map fails with NameError: global name 'func' is not defined
#XXX:: ez_map2 fails with RuntimeError: maximum recursion depth exceeded
#from mystic.models.poly import chebyshev8cost as func

def host(coeffs):
    from mystic.models.poly import chebyshev8cost as func
    return "Chebyshev%s = %s" % (coeffs, func(coeffs))

from pyina.launchers import mpirun_launcher as mylauncher
params = [(i,0,-2*i,0,4*i,0,-2*i,0,i) for i in range(10)]

print "Evaluate the 8th order Chebyshev polynomial..."
print "Using 'ez_map' for 10 combinations over 4 nodes"
res1 = ez_map(host, params, nnodes=4, launcher=mylauncher)
print '\n'.join(res1)
print ''

print "Using 'ez_map2' for 10 combinations over 4 nodes"
res2 = ez_map2(host, params, nnodes=4, launcher=mylauncher)
print '\n'.join(res2)

# end of file
