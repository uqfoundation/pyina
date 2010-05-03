#!/usr/bin/env python

"""
ezrun.py  

This is a helper for func_pickle.py.
Don't use directly.
"""

import pyina.launchers as launchers

if __name__ == '__main__':

    from pyina.parallel_map import parallel_map
    import dill as pickle #XXX: to address costfactories
    import mpi, pyina, sys
    world = mpi.world()

   # funcname, arglist, outfilename = sys.argv[1], sys.argv[2], sys.argv[3]

    funcname = sys.argv[1]
    if funcname.endswith('.pik'):  # used ez_map2
        func = pickle.load(open(funcname,'r'))
    else:  # used ez_map
        sys.path = [sys.argv[4]] + sys.path
        module = __import__(funcname)
        sys.path.pop(0)
        func = module.FUNC
    arglist = pickle.load(open(sys.argv[2],'r'))

    res = parallel_map(func, *arglist)

    if world.rank == 0:
        pickle.dump(res, open(sys.argv[3],'w'))

# end of file
