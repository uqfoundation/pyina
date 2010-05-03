#!/usr/bin/env python
#
# 

import pyina.launchers as launchers

doc = """
# Does map in parallel.
#
# usage: parallel_map(func, seq, master = 0, comm = mpi.world() )
#
# Breaks up the input sequence [seq] into nproc pieces (in a balanced
# manner when len(nseq) isn't divisble by nproc) and sends them to the nodes.

%(launchers)s

# This doesn't scale well with the number of processors because
# of the 1 to many sends, and then the many to 1 gather.
""" % { 'file' : __file__, 'launchers' : launchers.getstr() }

from mpi.Application import Application
import logging
import pickle

#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(levelname)s %(message)s',
#                    datefmt='%a, %d %b %Y %H:%M:%S')


import mpi, journal

import mpiconsts
import pyina
from pyina._pyina import sendString, receiveString
from pyina.tools import get_workload

#def parallel_map(func, seq, master = 0, comm = mpi.world() ):
def parallel_map(func, *seq, **kwds):
    master = 0
    if kwds.has_key('master'): master=kwds['master']
    if kwds.has_key('comm'): comm=kwds['comm']
    else: comm=mpi.world()

    # assumes that only the master has the sequence when started
    # will gather result back to master when done, but master will 
    # do its share as well

    size = comm.size
    myid = comm.rank
    logging.info("I am rank %d of %d" % (myid, size))

    # create a private communicator
    input_comm = comm.handle()
    private_comm = pyina._pyina.commDup(input_comm)

    MPI_ANY_SOURCE = mpiconsts.mpi.MPI_ANY_SOURCE
    MPI_ANY_TAG = mpiconsts.mpi.MPI_ANY_TAG

    NJOBS = len(seq[0])
    the_answers = [''] * NJOBS

    # each processor needs to do its set of jobs. 
    ib, ie = get_workload(myid, size, NJOBS)

    if myid == master:
        my_seq = tuple([i[ib:ie] for i in seq])
        # send jobs to slaves
        for slave in range(1, size):
            ib, ie = get_workload(slave, size, NJOBS)
            logging.info("[parallel_map2] MASTER : Sending seq[%d:%d] to slave %d" % (ib, ie, slave))
            the_seq = tuple([i[ib:ie] for i in seq])
            sendString(private_comm, slave, 0, pickle.dumps(the_seq))
    else:
        logging.info("Rank %d is here " % (myid))
        # receive job
        logging.info("[parallel_map] SLAVE %d, receiving." % (myid))
        (message,status) = receiveString(private_comm, master, MPI_ANY_TAG);
        logging.info("[parallel_map] SLAVE %d, message received." % (myid))
        # no need to parse tags
        my_seq = pickle.loads(message)

    # now my_seq is the part that each proc has to do
    my_results = map(func, *my_seq)

    if myid == master:
        ib, ie = get_workload(myid, size, NJOBS)
        the_answers[ib:ie] = my_results[:]

    # at this point, all nodes must sent to master
    if myid != master:
        logging.info("[parallel_map2] SLAVE %d: Sending answer to master." % myid)
        sendString(private_comm, master, myid, pickle.dumps(my_results))
    else:
        # master needs to receive once for each slave
        for slave in range(1, size):
            logging.info("[parallel_map2] MASTER. Listening for slave.")
            (message,status) = receiveString(private_comm, MPI_ANY_SOURCE, MPI_ANY_TAG);
            sender, anstag  = status['MPI_SOURCE'], status['MPI_TAG']
            logging.info("[parallel_map2] MASTER : Received answer from slave %d." % sender)
            ib, ie = get_workload(sender, size, NJOBS)
            the_answers[ib:ie] = pickle.loads(message)
            logging.info("[parallel_map2] MASTER : Received %s from slave %d." % (the_answers[ib:ie],sender))

    #comm.barrier()
    return the_answers


if __name__ == "__main__":
    pass


# End of file
