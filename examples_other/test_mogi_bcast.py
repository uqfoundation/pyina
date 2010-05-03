#!/usr/bin/env python
#
# 

"""
Just a basic test. No physics.

To launch... either do, for example

mpirun -np 4 `which mpipython.exe` test_mogi.py

or

test_mogi.py (with --launcher.nodes defaults to 4)

"""

import pyina, mystic
from mpi.Application import Application
import logging
import pickle
from time import sleep
from numpy import array

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

class SimpleApp(Application):

    def main(self):
        import mpi, random
        from mystic.models import mogi; forward_mogi = mogi.evaluate

        world = mpi.world()
        size = world.size

        logging.info("I am rank %d of %d" % (world.rank, size))
        master = 0
        MPI_ANY_SOURCE = pyina.mpi.MPI_ANY_SOURCE
        MPI_ANY_TAG = pyina.mpi.MPI_ANY_TAG

        EXITTAG = 999
        if world.rank == master:
            # let's say I have a set of NJOBS points to test
            NJOBS = 100
            assert (EXITTAG > NJOBS)

            # all the "evaluation points" are the same, so broadcast to slaves
            eval_at = array([[1,2],[2,3]])
            recv = pickle.loads(pyina._pyina.bcastString(world.handle(), master, pickle.dumps(eval_at)))
            # the universe of params
            params = [[random.random() for _ in range(4)] for _ in range(NJOBS)]
            # now farm out to the slaves
            numsent = 0
            for slave in range(1, size):
                logging.info("MASTER : First Send: Sending job %d to slave %d" % (numsent, slave))
                mpi._mpi.sendString(world.handle(), slave, numsent, pickle.dumps(params[numsent]))
                numsent = numsent+1
            # start receiving
            for i in range(NJOBS):  
                logging.info("MASTER : Top of loop")
                (message,status) = pyina._pyina.receiveString(world.handle(), MPI_ANY_SOURCE, MPI_ANY_TAG);
                sender = status['MPI_SOURCE']
                anstag = status['MPI_TAG']
                logging.info("MASTER : Received job %d from slave %d" % (anstag, sender))
                #sleep(3)
                if (numsent < NJOBS):
                    # send next job
                    logging.info("MASTER : Sending job %d to slave %d" % (numsent, sender))
                    mpi._mpi.sendString(world.handle(), sender, numsent, pickle.dumps(params[numsent]))
                    numsent = numsent + 1
                else:
                    # done
                    logging.info("MASTER : Sending DONE signal to slave %d" % (sender))
                    mpi._mpi.sendString(world.handle(), sender, EXITTAG, "")
        else:
            eval_at = pickle.loads(pyina._pyina.bcastString(world.handle(), master, ""))
            #logging.info("Rank %d has message %s" % (world.rank, eval_at))
            for iter in range(99999):
                # receive job
                logging.info("   SLAVE %d, iteration %d." % (world.rank, iter))
                (message,status) = pyina._pyina.receiveString(world.handle(), master, MPI_ANY_TAG);
                tag = status['MPI_TAG']
                if tag == EXITTAG:
                    logging.info("   SLAVE %d: is done." % world.rank)
                    return
                param = pickle.loads(message)
                logging.info("   SLAVE %d receiving job %d ... running" % (world.rank, tag))
                res = forward_mogi(param, eval_at)
                # send result back to master
                logging.info("   SLAVE %d done running job %d, send results back to master" % (world.rank, tag))
                #sleep(2)
                mpi._mpi.sendString(world.handle(), master, tag, pickle.dumps(res))

        return

    def _defaults(self):
        self.inventory.launcher.inventory.nodes = 4

    def __init__(self):
        Application.__init__(self, "simple")
        return


# main

if __name__ == "__main__":
    import journal
    journal.info("mpirun").activate()
    journal.debug("simple").activate()
    #journal.debug("pyina.receiveString").activate()
    
    app = SimpleApp()
    app.run()

# End of file
