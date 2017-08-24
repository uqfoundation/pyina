#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
#
# helper script to setup your mpi environment

__doc__ = """
setup the MPI environment

Note:
    Options:
        * ``-help``         [prints this message]
        * ``-slaves nodes`` [set mpi world (nodes is a list of slave nodes)]
        * ``-kill``         [tear down mpi world]

Note:
    ``'mpd &'`` must be run before setting the slave nodes.

Examples::

    $ mpi_world.py -slaves [n00, n01, n02, n03]
    seting up mpi...
"""
#   -alias nnodes     set bash aliases for mpiexec (nnodes is X in '-np X')

from subprocess import Popen, PIPE, STDOUT
popen4 = {'shell':True, 'stdin':PIPE, 'stdout':PIPE, 'stderr':STDOUT, \
          'close_fds':True}

MASTERINFO = []

def launch(command,quiet=True):
    "launch a os.system command; if quiet, don't grab the output"
    print "launch: %s" % command
    p = Popen(command, **popen4)
    p.stdin.close()
    if quiet is True:
        outstr = None
    else:
        outstr = p.stdout.readlines()
    p.stdout.close()
   #print "result: %s" % outstr
    return outstr

def alias(nnodes):
    "set a bash shell alias to configure mpiexec to run python on nnodes"
    node = str(nnodes)
    alias = "mpython%s='mpiexec -np %s `which python`'" % (node,node)
    command = "alias %s" % alias
    print command
    raise NotImplementedError #FIXME: alias doesn't stick to user's console
    try:
        launch(command)
    except OSError:
        pass
    return

def set_master():
    "get master info"
    # launch('mpd &') #FIXME: doesn't work!
    try:
        outstr = launch('mpdtrace -l',quiet=False)
        master,ip = outstr[0].split()
        master,port = master.split("_")
        MASTERINFO = [master,int(port)]
    except:
        err = "did you run 'mpd &' first?"
        raise Exception, err
    return MASTERINFO

def set_slaves(nodelist,masterinfo=MASTERINFO):
    "run mpd on slave nodes"
    host = str(masterinfo[0])
    port = str(masterinfo[1])
    for node in nodelist:
        command = "rsh %s mpd -h %s -p %s &" % (node,host,port)
        launch(command)
    return

def kill_all():
    "kill the mpi world"
    launch("mpdallexit")
   #outstr = launch("ps | grep 'rsh'",quiet=False)
   #for line in outstr:
   #    print line
    return


if __name__=="__main__":
    import sys
    if sys.argv[-1] == "-kill":
        print "killing all..."
        kill_all()
    elif len(sys.argv) > 2:
        if sys.argv[-2] == "-slaves":
            print "seting up mpi..."
            MASTERINFO = set_master()
            nodes = sys.argv[-1]
            nodes = nodes.strip('[()]').split(',')
            set_slaves(nodes,MASTERINFO)
       #elif sys.argv[-2] == "-alias": 
       #    print "setting up mpi python..."
       #    nodes = sys.argv[-1]
       #    nodes = nodes.strip('[()]').split(',')
       #    for node in nodes:
       #        alias(int(node))
        else: # "-help"
            print __doc__
    else: # "-help"
        print __doc__


# End of file
