#!/usr/bin/env python
#
debug = False

doc = """
# Does map in parallel.
#
# usage: parallel_map(func, seq, master = 0, comm = mpi.COMM_WORLD )
#
# Breaks up the input sequence [seq] into nproc pieces (in a balanced
# manner when len(nseq) isn't divisble by nproc) and sends them to the nodes.

# This doesn't scale well with the number of processors because
# of the 1 to many sends, and then the many to 1 gather.
"""

import logging

from mpi4py import MPI as mpi
from pyina.tools import get_workload

#def parallel_map(func, seq, master = 0, comm = mpi.COMM_WORLD ):
def parallel_map(func, *seq, **kwds):
    master = 0
    if kwds.has_key('master'): master=kwds['master']
    if kwds.has_key('comm'): comm=kwds['comm']
    else: comm=mpi.COMM_WORLD

    # assumes that only the master has the sequence when started
    # will gather result back to master when done, but master will 
    # do its share as well

    size = comm.Get_size()
    myid = comm.Get_rank()
    logging.info("I am rank %d of %d" % (myid, size))

    # create a private communicator
    private_comm = comm.Clone()

    NJOBS = len(seq[0])
    the_answers = [''] * NJOBS

    # each processor needs to do its set of jobs. 
    ib, ie = get_workload(myid, size, NJOBS)

    if myid == master:
        message = tuple([i[ib:ie] for i in seq])
        # send jobs to slaves
        for slave in range(1, size):
            ib, ie = get_workload(slave, size, NJOBS)
            logging.info("[parallel_map2] MASTER : Sending seq[%d:%d] to slave %d" % (ib, ie, slave))
            the_seq = tuple([i[ib:ie] for i in seq])
            private_comm.send(the_seq, slave, 0)
    else:
        logging.info("Rank %d is here " % (myid))
        # receive job
        logging.info("[parallel_map] SLAVE %d, receiving." % (myid))
        status = mpi.Status()
        message = private_comm.recv(source=master, tag=mpi.ANY_TAG, status=status)
        logging.info("[parallel_map] SLAVE %d, message received." % (myid))
        # no need to parse tags

    # now message is the part that each proc has to do
    my_results = map(func, *message)

    if myid == master:
        ib, ie = get_workload(myid, size, NJOBS)
        the_answers[ib:ie] = my_results[:]

    # at this point, all nodes must sent to master
    if myid != master:
        logging.info("[parallel_map2] SLAVE %d: Sending answer to master." % myid)
        private_comm.send(my_results, master, myid)
    else:
        # master needs to receive once for each slave
        for slave in range(1, size):
            logging.info("[parallel_map2] MASTER. Listening for slave.")
            status = mpi.Status()
            message = private_comm.recv(source=mpi.ANY_SOURCE, tag=mpi.ANY_TAG, status=status)
            sender = status.source
            anstag = status.tag
            logging.info("[parallel_map2] MASTER : Received answer from slave %d." % sender)
            ib, ie = get_workload(sender, size, NJOBS)
            the_answers[ib:ie] = message
            logging.info("[parallel_map2] MASTER : Received %s from slave %d." % (the_answers[ib:ie],sender))

    #comm.barrier()
    return the_answers


if __name__ == "__main__":
    pass


# End of file
