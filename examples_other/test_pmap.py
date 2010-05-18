#!/usr/bin/env python
#
# 
doc = """
# Tests parallel, master-slave. Version 0
# To run:  (use #nodes >= 2)

alias mpython='mpirun -np [#nodes] `which python`'
mpython test_pmap.py
"""
# pick either mapping strategy
#from pyina.parallel_map import parallel_map
from pyina.parallel_map2 import parallel_map


if __name__ == "__main__":

    import journal
    journal.info("mpirun").activate()

    # This will print the actions of destructors inside pyina
    #journal.debug("pyina.fini").activate()

    from pyina import mpi, ensure_mpi
    world = mpi.world

    ensure_mpi(size=2, doc=doc)

    def func(input):
        import time
        from pyina import mpi
        world = mpi.world
        time.sleep(0.0001)
        return "-%d" % world.rank

    inputlist = []
    if world.rank == 0:
        inputlist = [0] * 300

    for i in range(20):
        if world.rank == 0:
            print "iteration %d" % i
        out = parallel_map(func, inputlist, comm = world)

    if world.rank == 0:
        print ''.join(out)


# End of file
