#!/usr/bin/env python

__doc__ = """
# print rank - hostname info
# To run:

alias mpython='mpirun -np [#nodes] `which python`'
mpython machines_raw.py
"""

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())


if __name__ == '__main__':

    try:
        from pyina.mpi_scatter import parallel_map
        import pyina
        world = pyina.mpi.world

        hostnames = parallel_map(host, range(world.size))

        if world.rank == 0:
            print '\n'.join(hostnames)
    except:
        print __doc__
        

# end of file
