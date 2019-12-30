#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

from pyina.launchers import Mpi

#XXX: should not have to define "func" within mapped function
#from mystic.models import rosen as func

def host(coeffs):
    from mystic.models import rosen as func
    return "rosen%s = %s" % (coeffs, func(coeffs))

print("Evaluate an imported function (the rosenbrock function)...")
print("For 10 items on 4 nodes, using the default mapping strategy")
params = [(i,i,i) for i in range(10)]
pool = Mpi(4)
res = pool.map(host, params)
print(pool)
print('\n'.join(res))

# end of file
