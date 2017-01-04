#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE
"""
Just a basic test. No physics.

To launch... either do, for example

mpiexec -np 4 `which python` test_mogi_bcast.py

or

python test_mogi_bcast.py
(with --launcher.nodes defaulting to 4)

"""

import mystic
from mpi.Application import Application
import logging
from time import sleep
from numpy import array

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

class SimpleApp(Application):

    def main(self):
        from pyina import mpi
        import random
        from mystic.models import mogi; forward_mogi = mogi.evaluate

        world = mpi.world
        size = world.size

        logging.info("I am rank %d of %d" % (world.rank, size))
        master = 0
        MPI_ANY_SOURCE = mpi.ANY_SOURCE
        MPI_ANY_TAG = mpi.ANY_TAG

        EXITTAG = 999
        if world.rank == master:
            # let's say I have a set of NJOBS points to test
            NJOBS = 100
            assert (EXITTAG > NJOBS)

            # all the "evaluation points" are the same, so broadcast to slaves
            eval_at = array([[1,2],[2,3]])
            recv = world.bcast(eval_at, master)
            # the universe of params
            params = [[random.random() for _ in range(4)] for _ in range(NJOBS)]
            # now farm out to the slaves
            numsent = 0
            for slave in range(1, size):
                logging.info("MASTER : First Send: Sending job %d to slave %d" % (numsent, slave))
                world.send(params[numsent], slave, numsent)
                numsent = numsent+1
            # start receiving
            for i in range(NJOBS):  
                logging.info("MASTER : Top of loop")
                status = mpi.Status()
                message = world.recv(source=MPI_ANY_SOURCE, tag=MPI_ANY_TAG, status=status)
                sender = status.source
                anstag = status.tag
                logging.info("MASTER : Received job %d from slave %d" % (anstag, sender))
                #sleep(3)
                if (numsent < NJOBS):
                    # send next job
                    logging.info("MASTER : Sending job %d to slave %d" % (numsent, sender))
                    world.send(params[numsent], sender, numsent)
                    numsent = numsent + 1
                else:
                    # done
                    logging.info("MASTER : Sending DONE signal to slave %d" % (sender))
                    world.send("", sender, EXITTAG)
        else:
            eval_at = world.bcast("", master)
            #logging.info("Rank %d has message %s" % (world.rank, eval_at))
            for iter in range(99999):
                # receive job
                logging.info("   SLAVE %d, iteration %d." % (world.rank, iter))
                status = mpi.Status()
                param = world.recv(source=master, tag=MPI_ANY_TAG, status=status)
                tag = status.tag
                if tag == EXITTAG:
                    logging.info("   SLAVE %d: is done." % world.rank)
                    return
                logging.info("   SLAVE %d receiving job %d ... running" % (world.rank, tag))
                res = forward_mogi(param, eval_at)
                # send result back to master
                logging.info("   SLAVE %d done running job %d, send results back to master" % (world.rank, tag))
                #sleep(2)
                world.send(res, master, tag)

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
    #journal.debug("pyina.mpi.world.recv").activate()
    
    app = SimpleApp()
    app.run()

# End of file
