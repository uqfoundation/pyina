#!/usr/bin/env python
#
"""
Does map in parallel using the carddealer strategy.
Implemented as master-worker.

usage: parallel_map(func, seq, master = 0, comm = mpi.COMM_WORLD )

Deals out one item from the input sequence [seq] to each available
resource, and waits to deal out the next item in the seq until one
of the nodes is free (i.e. work is allocated as nodes become free).
"""
import logging
log = logging.getLogger("parallel_map")
log.addHandler(logging.StreamHandler())
def _debug(boolean):
    """print debug statements"""
    if boolean: log.setLevel(logging.DEBUG)
    else: log.setLevel(logging.WARN)
    return

from mpi4py import MPI as mpi

#def parallel_map(func, seq, master = 0, comm = mpi.COMM_WORLD ):
def parallel_map(func, *seq, **kwds):
    """parallel mapping using the carddealer mapping strategy"""
    master = 0
    if kwds.has_key('master'): master=kwds['master']
    if kwds.has_key('comm'): comm=kwds['comm']
    else: comm=mpi.COMM_WORLD

    size = comm.Get_size()
    rank = comm.Get_rank()

    EXITTAG = 0
    NJOBS = len(seq[0])
    nodes = size
    if size > NJOBS + 1:
        nodes = NJOBS + 1  # max workers required is NJOBS+1
    log.info("size = %s; NJOBS = %s; seq = %s" % (size,NJOBS,seq))

    the_answers = [''] * NJOBS
    if rank == master:
        # now farm out to the slaves
        elemid = 1 # 1 indexing, 0 is reserved for termination
        for slave in range(1, nodes):
            log.info("First send: elemid = %s; slave = %s" % (elemid,slave))
            my_seq = tuple([i[elemid-1] for i in seq])
            log.info("my_seq = %s of %s" % (my_seq, type(my_seq)))
            #XXX: SEND JOB (elemid) TO SLAVE (slave). JOB => (my_seq)
            comm.send(my_seq, slave, elemid)
            elemid = elemid+1
        # start receiving
        for i in range(NJOBS):  
            #XXX: RECIEVE JOBS FROM ANY_SOURCE & ANY_TAG
            status = mpi.Status()
            message = comm.recv(source=mpi.ANY_SOURCE, tag=mpi.ANY_TAG, status=status)
            sender = status.source
            anstag = status.tag
            log.info("Master: anstag = %s; message = %s; sender = %s" % (anstag,message,sender))
            the_answers[anstag-1] = message
            if (elemid <= NJOBS):
                # send next job
                log.info("Master send: elemid = %s; slave = %s" % (elemid,sender))
                the_seq = tuple([i[elemid-1] for i in seq])
                log.info("the_seq = %s of %s" % (the_seq, type(the_seq)))
                #XXX: SEND JOB (elemid) TO SLAVE (sender). JOB => (the_seq)
                comm.send(the_seq, sender, elemid)
                elemid = elemid + 1
            else:
                # done
                log.info("Master sending done: slave = %s" % slave)
                #XXX: SEND EXITTAG TO SLAVE (sender). JOB => ("done")
                comm.send("done", sender, EXITTAG)
    elif (nodes != size) and (rank >= nodes):
        log.info("Skipping %d" % (rank))
        pass
    else:
       #import itertools
       #counter = itertools.count(1)
        while 1:
            # receive job
       #    logging.info("worker %d, iteration %d." % (rank, counter.next()))
            #XXX: RECIEVE JOBS FROM MASTER @ ANY_TAG
            status = mpi.Status()
            message = comm.recv(source=master, tag=mpi.ANY_TAG, status=status)
            tag = status.tag
            if tag == EXITTAG:
                break
            log.info("evaluating...  f(%s)" % message)
            result = func(*message)
            log.info("arg = %s; result = %s; tag = %s" % (message,result,tag))
            # send result back to master
            #XXX: SEND RESULT TO MASTER. JOB => (result)
            comm.send(result, master, tag)

    comm.barrier()
    return the_answers


if __name__ == "__main__":
    pass


# End of file
