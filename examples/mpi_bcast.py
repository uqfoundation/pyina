#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

doc = """
A basic demonstration of low-level MPI communication.

To launch:

mpiexec -np 4 `which python` mpi_bcast.py
"""

import mystic
import logging
from time import sleep
from numpy import array

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

class SimpleApp(object):

    def __call__(self):
        from pyina import mpi, ensure_mpi
        import random
        from mystic.models import mogi; forward_mogi = mogi.evaluate

        ensure_mpi(size=2, doc=doc)

        world = mpi.world
        size = world.size
        stat = mpi.MPI.Status

        logging.info("I am rank %d of %d" % (world.rank, size))
        master = 0

        EXITTAG = 999
        if world.rank == master:
            # let's say I have a set of NJOBS points to test
            NJOBS = 100
            assert (EXITTAG > NJOBS)

            # all the "evaluation points" are the same, so broadcast to workers
            eval_at = array([[1,2],[2,3]])
            recv = world.bcast(eval_at, master)
            # the universe of params
            params = [[random.random() for _ in range(4)] for _ in range(NJOBS)]
            # now farm out to the workers
            numsent = 0
            for worker in range(1, size):
                logging.info("MASTER : First Send: Sending job %d to worker %d" % (numsent, worker))
                world.send(params[numsent], worker, numsent)
                numsent = numsent+1
            # start receiving
            for i in range(NJOBS):  
                logging.info("MASTER : Top of loop")
                status = stat()
                message = world.recv(status=status)
                sender = status.source
                anstag = status.tag
                logging.info("MASTER : Received job %d from worker %d" % (anstag, sender))
                #sleep(3)
                if (numsent < NJOBS):
                    # send next job
                    logging.info("MASTER : Sending job %d to worker %d" % (numsent, sender))
                    world.send(params[numsent], sender, numsent)
                    numsent = numsent + 1
                else:
                    # done
                    logging.info("MASTER : Sending DONE signal to worker %d" % (sender))
                    world.send("", sender, EXITTAG)
        else:
            eval_at = world.bcast("", master)
            #logging.info("Rank %d has message %s" % (world.rank, eval_at))
            for iter in range(99999):
                # receive job
                logging.info("   WORKER %d, iteration %d." % (world.rank, iter))
                status = stat()
                param = world.recv(source=master, status=status)
                tag = status.tag
                if tag == EXITTAG:
                    logging.info("   WORKER %d: is done." % world.rank)
                    return
                logging.info("   WORKER %d receiving job %d ... running" % (world.rank, tag))
                res = forward_mogi(param, eval_at)
                # send result back to master
                logging.info("   WORKER %d done running job %d, send results back to master" % (world.rank, tag))
                #sleep(2)
                world.send(res, master, tag)
        return


# main

if __name__ == "__main__":
    
    app = SimpleApp()
    app()

# End of file
