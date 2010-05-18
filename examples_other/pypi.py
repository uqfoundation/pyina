#!/usr/bin/env python

__doc__ = """
# The standard MPI example, computes the integral 
# 
# Integrate[4/(1+x^2),{x,0,1}]
# 
# numerically, and in parallel.
# To run:

alias mpython='mpirun -np [#nodes] `which python`'
mpython pypi.py

# A few warnings:
#  - Evaluating this integral is a horrible way to get the value of Pi
#  - Uniform sampling (or the trapezoidal rule, as implemented here) is
#    a horrible way to get the value of the integral
#
# For quickies, use scipy instead, which provides the bindings to quadpack.

import scipy.integrate
scipy.integrate.quad(lambda x: 4.0/(1+x*x), 0, 1)
"""

from numpy import arange

# default # of rectangles
n = 20000

integration_points = (arange(1,n+1)-0.5)/n

def f(x):
    return 4.0/(1.0+x*x)

#from pyina.parallel_map import parallel_map
from pyina.parallel_map2 import parallel_map


if __name__ == '__main__':

    from pyina import mpi
    out = parallel_map(f, integration_points)
    
    if mpi.world.rank == 0:
        print "approxmiate pi : ", sum(out)/n

# end of file
