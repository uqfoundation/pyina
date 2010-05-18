#!/usr/bin/env python

__doc__ = """
# An example of running ez_map to process a batch file
# BE VERY CAREFUL with this script, as it executes system calls. 
# To run:

python parallel_batch.py [batchfile.txt] [#nodes]
"""

def runshell(input):
    """
    This function just calls popen on the input string, and the stdout is printed.
    """
    import socket
    from os import popen
    print "%s executing: %s" % (socket.gethostname(), input)
    popen(input).readlines()
    return 0

    
if __name__ == "__main__":

    import sys
    if len(sys.argv) > 2: nnodes = int(sys.argv[2])
    else: nnodes = 1

    try:
        from pyina.ez_map import ez_map

        batchfile = sys.argv[1]
        inputlist = []
        inputlist = open(batchfile).readlines()
        out = ez_map(runshell, inputlist, nnodes=nnodes)
    except:
        print __doc__


# End of file
