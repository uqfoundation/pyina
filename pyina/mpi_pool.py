#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

import sys
if sys.version < "3":
    from itertools import izip as zip
from mpi4py import MPI as mpi
import dill
try:
    getattr(mpi,'pickle',getattr(mpi,'_p_pickle',None)).dumps = dill.dumps
    getattr(mpi,'pickle',getattr(mpi,'_p_pickle',None)).loads = dill.loads
except AttributeError:
    pass
from pyina.tools import lookup
from pathos.helpers import ProcessPool as MPool
master = 0
comm = mpi.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
any_source = mpi.ANY_SOURCE
any_tag = mpi.ANY_TAG
EXITTAG = 0
__SKIP = [True]
import logging
log = logging.getLogger("mpi_pool")
log.addHandler(logging.StreamHandler())
def _debug(boolean):
    """print debug statements"""
    if boolean: log.setLevel(logging.DEBUG)
    else: log.setLevel(logging.WARN)
    return

def __queue(*inputs):
    "iterator that groups inputs by index (i.e. [(x[0], a[0]),(x[1], a[1])])"
    return zip(*inputs)

def __index(*inputs):
    """build an index iterator for the given inputs"""
    NJOBS = len(inputs[0])
    return iter(range(NJOBS))

def parallel_map(func, *seq, **kwds):
    """the worker pool strategy for mpi"""
    skip = not bool(kwds.get('onall', True))
    __SKIP[0] = skip

    NJOBS = len(seq[0])
    nodes = size if size <= NJOBS+skip else NJOBS+skip # nodes <= NJOBS+(master)
   #queue = __queue(*seq) #XXX: passing the *data*
    queue = __index(*seq) #XXX: passing the *index*
    results = [''] * NJOBS

    if rank == master:
        log.info("size: %s, NJOBS: %s, nodes: %s, skip: %s" % (size, NJOBS, nodes, skip))
        if nodes == 1: # the pool is just the master
            if skip: raise ValueError("There must be at least one worker node")
            return map(func, *seq)
        # spawn a separate process for jobs running on the master
        if not skip:
            pool = MPool(1) #XXX: poor pickling... use iSend/iRecv instead?
           #input = queue.next() #XXX: receiving the *data*
            input = lookup(seq, next(queue)) #XXX: receives an *index*
            log.info("MASTER SEND'ING(0)")
            mresult, mjobid = pool.apply_async(func, args=input), 0
        # farm out to workers: 1-N for indexing, 0 reserved for termination
        for worker in range(1, nodes): #XXX: don't run on master...
            # master send next job to worker 'worker' with tag='worker'
            log.info("WORKER SEND'ING(%s)" % (worker-skip,))
            comm.send(next(queue), worker, worker)

        # start receiving
        recvjob = 0; donejob = 0
        sendjob = nodes
        while recvjob < NJOBS:  # was: for job in range(NJOBS)
            log.info("--job(%s,%s)--" % (sendjob-skip, recvjob))
            if recvjob < NJOBS and donejob < nodes-1:
                status = mpi.Status()
                # master receive jobs from any_source and any_tag
                log.info("RECV'ING FROM WORKER")
                message = comm.recv(source=any_source,tag=any_tag,status=status)
                sender = status.source
                anstag = status.tag
                if anstag: recvjob += 1  # don't count a 'donejob'
                results[anstag-skip] = message # store the received message
                log.info("WORKER(%s): %s" % (anstag-skip, message))
                if (sendjob-skip < NJOBS): # then workers are not done
                    # master send next job to worker 'sender' with tag='jobid'
                    log.info("WORKER SEND'ING(%s)" % (sendjob-skip))
                    input = next(queue)
                    comm.send(input, sender, sendjob)
                    sendjob += 1
                else: # workers are done
                    # send the "exit" signal
                    log.info("WORKER SEND'ING(DONE)")
                    comm.send("done", sender, EXITTAG)
                    donejob += 1
            log.info("WORKER LOOP DONE")
            # check if the master is done
            log.info("--job(%s,%s)--" % (sendjob-skip, recvjob))
            if not skip and mresult.ready():
                log.info("RECV'ING FROM MASTER")
                results[mjobid] = mresult.get()
                log.info("MASTER(%s): %s" % (mjobid, results[mjobid]))
                recvjob += 1
                if (sendjob < NJOBS):
                    log.info("MASTER SEND'ING(%s)" % sendjob)
                   #input = queue.next() #XXX: receiving the *data*
                    input = lookup(seq, next(queue)) #XXX: receives an *index*
                    mresult, mjobid = pool.apply_async(func, args=input),sendjob
                    sendjob += 1
                else: mresult.ready = lambda : False
            log.info("MASTER LOOP DONE")
        log.info("WE ARE EXITING")
        if not skip:
            pool.close()
            pool.join()
    elif (nodes != size) and (rank >= nodes): # then skip this node...
        pass
    else: # then this is a worker node
        while True:
            # receive jobs from master @ any_tag
            status = mpi.Status()
            message = comm.recv(source=master, tag=any_tag, status=status)
            tag = status.tag
            if tag == EXITTAG: # worker is done
                break
            # worker evaluates received job
           #result = func(*message) #XXX: receiving the *data*
            result = func(*lookup(seq, message)) #XXX: receives an *index*
            # send result back to master
            comm.send(result, master, tag) #XXX: or write to results then merge?

    comm.barrier()
    return results


if __name__ == '__main__':
    _debug(False)
    def squared(x): return x**2
    x = range(10)
    y = parallel_map(squared, x)#, onall=False)
    if rank == master:
        print(("f: %s" % squared.__name__))
        print(("x: %s" % x))
        print(("y: %s" % y))


# EOF
