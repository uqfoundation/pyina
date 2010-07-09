#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                       Patrick Hung & Mike McKerns, Caltech
#                        (C) 1997-2010  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
"""
prepared launchers for parallel execution
"""

import os

def launch(command):
    """ launch mechanism for prepared launch command"""
    error = os.system(command)
    if error: raise IOError, "launch failed"
    return error

    
def mpirun_tasks(nodes):
    """
Helper function.
compute mpirun task_string from node string of pattern = N[:TYPE][:ppn=P]
For example, mpirun_tasks("3:core4:ppn=2") yields 6
    """
    nodestr = str(nodes)
    nodestr = nodestr.split(",")[0]  # remove appended -l expressions
    nodelst = nodestr.split(":")
    n = int(nodelst[0])
    nodelst = nodestr.split("ppn=")
    if len(nodelst) > 1:
        ppn = nodelst[1]
        ppn = int(ppn.split(":")[0])
    else: ppn = 1
    tasks =  n*ppn
    return tasks


def srun_tasks(nodes):
    """
Helper function.
compute srun task_string from node string of pattern = N[:ppn=P][,partition=X]
For example, srun_tasks("3:ppn=2,partition=foo") yields '3 -N2'
    """
    nodestr = str(nodes)
    nodestr = nodestr.split(",")[0]  # remove appended -l expressions
    nodelst = nodestr.split(":")
    n = int(nodelst[0])
    nodelst = nodestr.split("ppn=")
    if len(nodelst) > 1:
        ppn = nodelst[1]
        ppn = int(ppn.split(":")[0])
        tasks = "%s -N%s" % (n, ppn)
    else:
        tasks = "%s" % n
    return tasks


def serial_launcher(kdict={}):
    """
prepare launch for standard execution
syntax:  (python) (file) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    str = """ %(python)s %(file)s %(progargs)s""" % mydict
    return str


def mpirun_launcher(kdict={}):
    """
prepare launch for parallel execution using mpirun
syntax:  mpirun -np (nodes) (python) (file) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    str =  """ mpirun -np %(nodes)s %(python)s %(file)s %(progargs)s""" % mydict
    return str


def srun_launcher(kdict={}):
    """
prepare launch for parallel execution using srun
syntax:  srun -n(nodes) (python) (file) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4 -N1', ...}
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    str =  """ srun -n%(nodes)s %(python)s %(file)s %(progargs)s""" % mydict
    return str


def torque_launcher(kdict={}):
    """
prepare launch for torque submission using mpirun
syntax:  echo \"mpirun -np (nodes) (python) (file) (progargs)\" | qsub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4:nodetype:ppn=1', ...}
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    mydict['tasks'] = mpirun_tasks(mydict['nodes'])
    str = """ echo \"mpirun -np %(tasks)s %(python)s %(file)s %(progargs)s\" | qsub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
    return str


def moab_launcher(kdict={}):
    """
prepare launch for moab submission using srun
syntax:  echo \"srun -n(nodes) (python) (file) (progargs)\" | qsub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4:ppn=1,partition=xx', ...}
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    mydict['tasks'] = srun_tasks(mydict['nodes'])
    str = """ echo \"srun -n%(tasks)s %(python)s %(file)s %(progargs)s\" | msub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
    return str


def lsfmx_launcher(kdict={}):
    """
prepare launch for Myrinet / LSF submission of parallel python using mpich_mx
syntax:  bsub -K -W(timelimit) -n (nodes) -o (outfile) -a mpich_mx -q (queue) -J (progname) mpich_mx_wrapper (python) (file) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    #str = """ bsub -K -W%(timelimit)s -n %(nodes)s -o ./%%J.out -a mpich_mx -q %(queue)s -J %(progname)s mpich_mx_wrapper %(python)s %(file)s %(progargs)s""" % mydict
    str = """ bsub -K -W%(timelimit)s -n %(nodes)s -o %(outfile)s -a mpich_mx -q %(queue)s -J %(progname)s mpich_mx_wrapper %(python)s %(file)s %(progargs)s""" % mydict
    return str


def lsfgm_launcher(kdict={}):
    """
prepare launch for Myrinet / LSF submission of parallel python using mpich_gm
syntax:  bsub -K -W(timelimit) -n (nodes) -o (outfile) -a mpich_gm -q (queue) -J (progname) gmmpirun_wrapper (python) (file) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    #str = """ bsub -K -W%(timelimit)s -n %(nodes)s -o ./%%J.out -a mpich_gm -q %(queue)s -J %(progname)s gmmpirun_wrapper %(python)s %(file)s %(progargs)s""" % mydict
    str = """ bsub -K -W%(timelimit)s -n %(nodes)s -o %(outfile)s -a mpich_gm -q %(queue)s -J %(progname)s gmmpirun_wrapper %(python)s %(file)s %(progargs)s""" % mydict
    return str


defaults = { 'timelimit' : '00:02',
             'file' : '',
             'progname' : '',
             'outfile' : './results.out',
             'errfile' : './errors.out',
             'jobfile' : './jobid',
             'queue' : 'normal',
             'python' : '`which python`' ,
             'nodes' : '1',
             'progargs' : ''
           }

 
def all_launchers():
    import launchers
    L = ["launchers.%s" % f for f in  dir(launchers) if f[-8:] == "launcher"]
    return L


def getstr(kdict = {}):
    import launchers, traceback, os.path
    stack = traceback.extract_stack()
    caller = stack[ -min(len(stack),2) ][0]
    #
    defaults['file'] = caller
    defaults['progname'] = os.path.basename(caller)
    #
    for key in defaults.keys():
        if not kdict.has_key(key):
            kdict[key] = defaults[key]
    L = all_launchers()
    #
    str = []
    for launcher in L:
        str.append(eval('%s(kdict)' % (launcher)))
        str.append('')
    return '\n'.join(str)


doc = """
# Returns a sample command for launching parallel jobs. 
# Helpful in making docstrings, by allowing the following in your docstring
# "%%(launcher)s", and then doing string interpolation "{'launcher' : getstr()}"
# and you will get:

%(launcher)s

# getstr does a stack traceback to find the name of the file containing its caller.
# This allows interpolation of the __file__ variable into the mpi launch commands.

# Most flexibly, getstr should be called with a dictionary. Here are the defaults. 
#  defaults = { 'timelimit' : '00:02',
#               'file' :  *name of the caller*,
#               'progname' :  *os.path.basename of the caller*,
#               'outfile' :  *path of the output file*,
#               'errfile' :  *path of the error file*,
#               'jobfile' :  *path of jobid file*,
#               'queue' :  'normal',
#               'python' :  '`which python`',
#               'nodes' :  '1',
#               'progargs' :  ''
#             }
""" % {'launcher' : getstr({'file':__file__, 'timelimit': '00:02', 'outfile':'./results.out'}) }


if __name__=='__main__':
    from mystic import helputil
    helputil.paginate(doc)

    print "python launch"
    defaults['file'] = "tools.py"
    launch(serial_launcher(defaults))

    print "serial launch"
    settings = {'python':'', 'file':"hostname"} #XXX: don't like file=hostname
    launch(serial_launcher(settings))

# EOF
