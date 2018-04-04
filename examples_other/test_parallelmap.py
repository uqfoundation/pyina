#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2018 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

doc = """
# An example of running parallel_map, BE VERY CAREFUL with this script, as
# it executes system calls. 
# By Default, it currently schedules 300 mostly harmless commands:
# inputlist = ["ls > xx.%%d" %% i for i in range(300)]

# To run:

alias mpython='mpiexec -np [#nodes] `which python`'
mpython test_parallelmap.py
"""

if __name__ == "__main__":

    from pyina.mpi_scatter import parallel_map
    from pyina.mpi_pool import parallel_map as parallel_map2

    from pyina import mpi, ensure_mpi
    world = mpi.world

    ensure_mpi()

    def func(input):
        """
        This function uses the safer subprocess module.
        """
        from subprocess import call
        if type(input) == list:
            print("Executing: %s" % ' '.join(input))
        else:
            print("Executing: %s" % input)
        retcode = call(input)
        return retcode

    def runshell(input):
        """
        This function just calls popen on the input string, and the stdout is printed.
        """
        from pyina import mpi
        from subprocess import Popen, PIPE
        print("%d of %d: executing: %s" % (mpi.world.rank, mpi.world.size, input))
        pipe = Popen(input, shell=True, stdout=PIPE).stdout
        pipe.readlines()
        return 0

    # Construct the shell commands to run
    inputlist = []
    if world.rank == 0:
        #inputlist = [ ["uname", "-a"]] * 300
        #inputlist = ["ls"] * 300
        #inputlist = [["echo","%d" % i] for i in range(300)]
        inputlist = ["ls > xx.%d" % i for i in range(300)]


    out = parallel_map2(runshell, inputlist)

    

# End of file
