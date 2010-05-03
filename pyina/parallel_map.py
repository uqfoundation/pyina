#!/usr/bin/env python
#
# 

import logging
import pickle
import pyina.launchers as launchers

doc = """
# Does map in parallel, master-slave. Version 0
#
# usage: parallel_map(func, seq, master = 0, comm = mpi.world() )
#
# Deals out one item from the input sequence [seq] to each available
# resource, and waits to deal out the next item in the seq until one
# of the nodes is free (i.e. work is allocated as nodes become free).

%(launchers)s
""" % { 'file' : __file__, 'launchers' : launchers.getstr({'nodes' : '6'}) }


#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(levelname)s %(message)s',
#                    datefmt='%a, %d %b %Y %H:%M:%S')

import mpi, journal

from pyina._pyina import sendString, receiveString
import mpiconsts

#def parallel_map(func, seq, master = 0, comm = mpi.world() ):
def parallel_map(func, *seq, **kwds):
    master = 0
    if kwds.has_key('master'): master=kwds['master']
    if kwds.has_key('comm'): comm=kwds['comm']
    else: comm=mpi.world()

    # provide same error behavior as 'map'
   #def identity(*args): return args
   #test = map(identity,*seq)

    size = comm.size
    logging.info("I am rank %d of %d" % (comm.rank, size))
    MPI_ANY_SOURCE = mpiconsts.mpi.MPI_ANY_SOURCE
    MPI_ANY_TAG = mpiconsts.mpi.MPI_ANY_TAG
    MPI_TAG_UB = mpiconsts.mpi.MPI_TAG_UB

    EXITTAG = 0
    NJOBS = len(seq[0])
    nodes = size
    if size > NJOBS + 1:
        nodes = NJOBS + 1  # max workers required is NJOBS+1
    #print "size = %s; NJOBS = %s; seq = %s" % (size,NJOBS,seq)

    the_answers = [''] * NJOBS
    if comm.rank == master:
        # now farm out to the slaves
        elemid = 1 # 1 indexing, 0 is reserved for termination
        for slave in range(1, nodes):
            logging.info("[parallel_map] MASTER : First Send: Sending job %d to slave %d" % (elemid, slave))
            journal.debug('parallel_map').log("MASTER : First Send: Sending job %d to slave %d" % (elemid, slave))
            #print "First send: elemid = %s; slave = %s" % (elemid,slave)
            my_seq = tuple([i[elemid-1] for i in seq])
            #print "seq[%s] = %s" % ((elemid-1),seq[elemid-1])
            #print "my_seq = %s" % my_seq
            sendString(comm.handle(), slave, elemid, pickle.dumps(my_seq))
            elemid = elemid+1
        # start receiving
        for i in range(NJOBS):  
            logging.info("[parallel_map]MASTER : Top of loop")
            (message,status) = receiveString(comm.handle(), MPI_ANY_SOURCE, MPI_ANY_TAG);
            sender = status['MPI_SOURCE']
            anstag = status['MPI_TAG']
            try:
                unpickled_msg = pickle.loads(message)
            except:
                print "this message [len = %d] from sender %d won't pickle... : %s " % (len(message), sender, message)
                raise
            logging.info("[parallel_map] MASTER : Received job %d [%s] from slave %d" % (anstag, unpickled_msg, sender))
            #print "Master: anstag = %s; un_msg = %s; sender = %s" % (anstag,unpickled_msg,sender)
            the_answers[anstag-1] = unpickled_msg
            if (elemid <= NJOBS):
                # send next job
                logging.info("[parallel_map] MASTER : Sending job %d to slave %d" % (elemid, sender))
                #print "Master send: elemid = %s; slave = %s" % (elemid,slave)
                the_seq = tuple([i[elemid-1] for i in seq])
                #print "_seq[%s] = %s" % ((elemid-1),"seq[elemid-1]")
                #print "the_seq = %s" % the_seq
                sendString(comm.handle(), sender, elemid, pickle.dumps(the_seq))
                elemid = elemid + 1
            else:
                # done
                logging.info("[parallel_map] MASTER : Sending DONE signal to slave %d" % (sender))
                #print "Master sending done: slave = %s" % slave
                sendString(comm.handle(), sender, EXITTAG, "done")
    elif (nodes != size) and (comm.rank >= nodes):
        logging.info("Rank %d is here " % (comm.rank))
        #print "Skipping %d" % (comm.rank)
        pass
    else:
        logging.info("Rank %d is here " % (comm.rank))
        import itertools
        counter = itertools.count(1)
        while 1:
            # receive job
            logging.info("[parallel_map] SLAVE %d, iteration %d." % (comm.rank, counter.next()))
            (message,status) = receiveString(comm.handle(), master, MPI_ANY_TAG);
            tag = status['MPI_TAG']
            if tag == EXITTAG:
                logging.info("[parallel_map] SLAVE %d: is done." % comm.rank)
                break
            func_arg = pickle.loads(message)
            logging.info("[parallel_map] SLAVE %d receiving job %d ... running" % (comm.rank, tag))
            result = func(*func_arg)
            #print "arg = %s; result = %s" % (func_arg,result)
            # send result back to master
            logging.info("[parallel_map] SLAVE %d done running job %d, send results [%s] back to master" % (comm.rank, tag, result))
            to_send = pickle.dumps(result)
            sendString(comm.handle(), master, tag, to_send)

    comm.barrier()
    return the_answers


if __name__ == "__main__":
    pass


# End of file
