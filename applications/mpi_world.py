#!/usr/bin/env python
#
# helper script to setup your mpi environment
__doc__ = """setup mpi python environment
options:
    -help             print this message
    -alias nnodes     set bash aliases for mpipython (nnodes is X in '-np X')
    -slaves nodes     set mpi world (nodes is the list of slave nodes)
    -kill             tear down mpi world

NOTE: make sure 'mpd &' was run before setting slave nodes!"""

import os

MASTERINFO = []

def launch(command,quiet=True):
    "launch a os.system command; if quiet, don't grab the output"
    print "launch: %s" % command
    stin,stout = os.popen4(command)
    stin.close()
    if quiet is True:
        outstr = None
    else:
        outstr = stout.readlines()
    stout.close()
   #print "result: %s" % outstr
    return outstr

def alias(nnodes):
    "set a bash shell alias to configure mpiexec to run python on nnodes"
    node = str(nnodes)
    alias = "mpython%s='mpiexec -np %s `which mpipython.exe`'" % (node,node)
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
        elif sys.argv[-2] == "-alias": 
            print "setting up mpi python..."
            nodes = sys.argv[-1]
            nodes = nodes.strip('[()]').split(',')
            for node in nodes:
                alias(int(node))
        else: # "-help"
            print __doc__
    else: # "-help"
        print __doc__


# End of file
