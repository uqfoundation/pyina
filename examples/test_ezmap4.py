#!/usr/bin/env python

from pyina.ez_map import ez_map

#XXX: should not have to define "func" within mapped function
#from mystic.models import rosen as func

def host(coeffs):
    from mystic.models import rosen as func
    return "x: %s --> %s" % (coeffs, func(coeffs))

from pyina.launchers import mpirun_launcher as mylauncher
params = [(i,i,i) for i in range(10)]
res = ez_map(host, params, nnodes=4, launcher=mylauncher)
print '\n'.join(res)

# end of file
