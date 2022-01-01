#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

from mpi4py import MPI as mpi
import dill
try:
    getattr(mpi,'pickle',getattr(mpi,'_p_pickle',None)).dumps = dill.dumps
    getattr(mpi,'pickle',getattr(mpi,'_p_pickle',None)).loads = dill.loads
except AttributeError:
    pass
from pyina.tools import get_workload, balance_workload, lookup
master = 0
comm = mpi.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
any_source = mpi.ANY_SOURCE
any_tag = mpi.ANY_TAG
EXITTAG = 0
__SKIP = [None]


def __queue(*inputs):
    "iterator that groups inputs by index (i.e. [(x[0], a[0]),(x[1], a[1])])"
   #NJOBS = len(inputs[0])
   #return (lookup(inputs, *get_workload(i, size, NJOBS, skip=__SKIP[0])) for i in range(size))
    load = __index(*inputs)
    return (lookup(inputs, next(load)) for i in range(size))

def __index(*inputs):
    """build an index iterator for the given inputs"""
    NJOBS = len(inputs[0])
    return (get_workload(i, size, NJOBS, skip=__SKIP[0]) for i in range(size)) 
   #return izip(*balance_workload(size, NJOBS, skip=__SKIP[0]))


def parallel_map(func, *seq, **kwds):
    """the scatter-gather strategy for mpi"""
    skip = not bool(kwds.get('onall', True))
    if skip is False: skip = None
    else:
        if size == 1:
            raise ValueError("There must be at least one worker node")
        skip = master
    __SKIP[0] = skip

    NJOBS = len(seq[0])
#   queue = __queue(*seq) #XXX: passing the *data*
    queue = __index(*seq) #XXX: passing the *index*
    results = [''] * NJOBS

    if rank == master:
        # each processor needs to do its set of jobs. 
        message = next(queue)
        # send jobs to workers
        for worker in range(1, size):
            # master sending seq[ib:ie] to worker 'worker'
            comm.send(next(queue), worker, 0)
    else:
        # worker 'rank' receiving job
        status = mpi.Status()
        message = comm.recv(source=master, tag=any_tag, status=status)
        # message received; no need to parse tags

    # now message is the part of seq that each worker has to do
#   result = map(func, *message) #XXX: receiving the *data*
    result = list(map(func, *lookup(seq, *message))) #XXX: receives an *index*

    if rank == master:
        _b, _e = get_workload(rank, size, NJOBS, skip=skip)
       #_b, _e = balance_workload(size, NJOBS, rank, skip=skip)
        results[_b:_e] = result[:]

    # at this point, all nodes must sent to master
    if rank != master:
        # worker 'rank' sending answer to master
        comm.send(result, master, rank)
    else:
        # master needs to receive once for each worker
        for worker in range(1, size):
            # master listening for worker
            status = mpi.Status()
            message = comm.recv(source=any_source, tag=any_tag, status=status)
            sender = status.source
           #anstag = status.tag
            # master received answer from worker 'sender'
            ib, ie = get_workload(sender, size, NJOBS, skip=skip)
           #ib, ie = balance_workload(size, NJOBS, sender, skip=skip)
            results[ib:ie] = message
            # master received results[ib:ie] from worker 'sender'

    #comm.barrier()
    return results


if __name__ == '__main__':
    def squared(x): return x**2
    x = range(10)
    y = parallel_map(squared, x)#, onall=False)
    if rank == master:
        print("f: %s" % squared.__name__)
        print("x: %s" % x)
        print("y: %s" % y)


# EOF
