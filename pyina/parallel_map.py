#!/usr/bin/env python
#
debug = False

import logging

doc = """
# Does map in parallel using the carddealer strategy.
# Implemented as master-worker.
#
# usage: parallel_map(func, seq, master = 0, comm = mpi.COMM_WORLD )
#
# Deals out one item from the input sequence [seq] to each available
# resource, and waits to deal out the next item in the seq until one
# of the nodes is free (i.e. work is allocated as nodes become free).
"""

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
    logging.info("I am rank %d of %d" % (rank, size))

    EXITTAG = 0
    NJOBS = len(seq[0])
    nodes = size
    if size > NJOBS + 1:
        nodes = NJOBS + 1  # max workers required is NJOBS+1
   #if debug: print "size = %s; NJOBS = %s; seq = %s" % (size,NJOBS,seq)

    the_answers = [''] * NJOBS
    if rank == master:
        # now farm out to the slaves
        elemid = 1 # 1 indexing, 0 is reserved for termination
        for slave in range(1, nodes):
            logging.info("[parallel_map] MASTER : First Send: Sending job %d to slave %d" % (elemid, slave))
           #if debug:
           #    print "First send: elemid = %s; slave = %s" % (elemid,slave)
            my_seq = tuple([i[elemid-1] for i in seq])
           #if debug:
           #    print "seq[%s] = %s" % ((elemid-1),seq[elemid-1])
           #    print "my_seq = %s of %s" % (my_seq, type(my_seq))
            #XXX: SEND JOB (elemid) TO SLAVE (slave). JOB => (my_seq)
            comm.send(my_seq, slave, elemid)
            elemid = elemid+1
        # start receiving
        for i in range(NJOBS):  
            logging.info("[parallel_map]MASTER : Top of loop")
            #XXX: RECIEVE JOBS FROM ANY_SOURCE & ANY_TAG
            status = mpi.Status()
            message = comm.recv(source=mpi.ANY_SOURCE, tag=mpi.ANY_TAG, status=status)
            sender = status.source
            anstag = status.tag
            logging.info("[parallel_map] MASTER : Received job %d [%s] from slave %d" % (anstag, message, sender))
           #if debug:
           #    print "Master: anstag = %s; message = %s; sender = %s" % (anstag,message,sender)
            the_answers[anstag-1] = message
            if (elemid <= NJOBS):
                # send next job
                logging.info("[parallel_map] MASTER : Sending job %d to slave %d" % (elemid, sender))
               #if debug:
               #    print "Master send: elemid = %s; slave = %s" % (elemid,sender)
                the_seq = tuple([i[elemid-1] for i in seq])
               #if debug:
               #    print "_seq[%s] = %s" % ((elemid-1),"seq[elemid-1]")
               #    print "the_seq = %s of %s" % (the_seq, type(the_seq))
                #XXX: SEND JOB (elemid) TO SLAVE (sender). JOB => (the_seq)
                comm.send(the_seq, sender, elemid)
                elemid = elemid + 1
            else:
                # done
                logging.info("[parallel_map] MASTER : Sending DONE signal to slave %d" % (sender))
               #if debug:
               #    print "Master sending done: slave = %s" % slave
                #XXX: SEND EXITTAG TO SLAVE (sender). JOB => ("done")
                comm.send("done", sender, EXITTAG)
    elif (nodes != size) and (rank >= nodes):
        logging.info("Rank %d is here " % (rank))
       #if debug: print "Skipping %d" % (rank)
        pass
    else:
        logging.info("Rank %d is here " % (rank))
        import itertools
        counter = itertools.count(1)
        while 1:
            # receive job
            logging.info("[parallel_map] SLAVE %d, iteration %d." % (rank, counter.next()))
            #XXX: RECIEVE JOBS FROM MASTER @ ANY_TAG
            status = mpi.Status()
            message = comm.recv(source=master, tag=mpi.ANY_TAG, status=status)
            tag = status.tag
            if tag == EXITTAG:
                logging.info("[parallel_map] SLAVE %d: is done." % rank)
                break
            logging.info("[parallel_map] SLAVE %d receiving job %d ... running" % (rank, tag))
           #if debug: print "evaluating...  f(%s)" % message
            result = func(*message)
           #if debug:
           #    print "arg = %s; result = %s; tag = %s" % (message,result,tag)
            # send result back to master
            logging.info("[parallel_map] SLAVE %d done running job %d, send results [%s] back to master" % (rank, tag, result))
            #XXX: SEND RESULT TO MASTER. JOB => (result)
            comm.send(result, master, tag)

    comm.barrier()
    return the_answers


if __name__ == "__main__":
    pass


# End of file
