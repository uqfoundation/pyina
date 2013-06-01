#!/usr/bin/env python

from pyina.launchers import Mpi

#XXX: should not have to define "func" within mapped function
#from mystic.models import rosen as func

def host(coeffs):
    from mystic.models import rosen as func
    return "rosen%s = %s" % (coeffs, func(coeffs))

print "Evaluate an imported function (the rosenbrock function)..."
print "For 10 items on 4 nodes, using the default mapping strategy"
params = [(i,i,i) for i in range(10)]
pool = Mpi(4)
res = pool.map(host, params)
print pool
print '\n'.join(res)

# end of file
