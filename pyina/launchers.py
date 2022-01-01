#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
This module contains prepared launchers for parallel execution, including
bindings to some common combinations of launchers and schedulers.

Base classes:
    SerialMapper   - base class for pipe-based mapping with python
    ParallelMapper - base class for pipe-based mapping with mpi4py

Parallel launchers:
    Mpi            - 
    Slurm          - 
    Alps           - 

Pre-built combinations of the above launchers and schedulers:
    TorqueMpi, TorqueSlurm, MoabMpi, MoabSlurm

Pre-configured maps using the 'scatter-gather' strategy:
    MpiScatter, SlurmScatter, AlpsScatter, TorqueMpiScatter,
    TorqueSlurmScatter, MoabMpiScatter, MoabSlurmScatter

Pre-configured maps using the 'worker pool' strategy:
    MpiPool, SlurmPool, AlpsPool, TorqueMpiPool, TorqueSlurmPool,
    MoabMpiPool, MoabSlurmPool

Usage
=====

A typical call to a pyina mpi map will roughly follow this example:

    >>> # instantiate and configure a scheduler
    >>> from pyina.schedulers import Torque
    >>> config = {'nodes'='32:ppn=4', 'queue':'dedicated', 'timelimit':'11:59'}
    >>> torque = Torque(**config)
    >>> 
    >>> # instantiate and configure a worker pool
    >>> from pyina.launchers import Mpi
    >>> pool = Mpi(scheduler=torque)
    >>>
    >>> # do a blocking map on the chosen function
    >>> results = pool.map(pow, [1,2,3,4], [5,6,7,8])

Several common configurations are available as pre-configured maps.
The following is identical to the above example:

    >>> # instantiate and configure a pre-configured worker pool
    >>> from pyina.launchers import TorqueMpiPool
    >>> config = {'nodes'='32:ppn=4', 'queue':'dedicated', 'timelimit':'11:59'}
    >>> pool = TorqueMpiPool(**config)
    >>>
    >>> # do a blocking map on the chosen function
    >>> results = pool.map(pow, [1,2,3,4], [5,6,7,8])


Notes
=====

This set of parallel maps leverage the mpi4py module, and thus has many of the
limitations associated with that module. The function f and the sequences
in args must be serializable. The maps provided here...

<<< FIXME >>

functionality when run from a script, however are somewhat limited
when used in the python interpreter. Both imported and interactively-defined
functions in the interpreter session may fail due to the pool failing to
find the source code for the target function. For a work-around, try:

<<< END FIXME >>>
"""

__all__ = ['SerialMapper', 'ParallelMapper', 'Mpi', 'Slurm', 'Alps',
           'MpiPool', 'MpiScatter', 'SlurmPool', 'SlurmScatter', 'AlpsPool',
           'AlpsScatter', 'TorqueMpi', 'TorqueSlurm', 'MoabMpi', 'MoabSlurm',
           'TorqueMpiPool', 'TorqueMpiScatter', 'TorqueSlurmPool',
           'TorqueSlurmScatter', 'MoabMpiPool', 'MoabMpiScatter',
           'MoabSlurmPool', 'MoabSlurmScatter']

from pyina.mpi import Mapper, defaults
from pathos.abstract_launcher import AbstractWorkerPool
from pathos.helpers import cpu_count
from pyina.schedulers import Torque, Moab, Lsf

import logging
log = logging.getLogger("launchers")
log.addHandler(logging.StreamHandler())


class SerialMapper(Mapper):
    """
Mapper base class for pipe-based mapping with python.
    """
    def __init__(self, *args, **kwds):
        Mapper.__init__(self, *args, **kwds)
        self.nodes = 1 # always has one node... it's serial!
        return
    __init__.__doc__ = Mapper.__init__.__doc__
    def _launcher(self, kdict={}):
        """prepare launch command for pipe-based execution

equivalent to:  (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
        """
        mydict = self.settings.copy()
        mydict.update(kdict)
        str = """%(python)s %(program)s %(progargs)s""" % mydict
        if self.scheduler:
            str = self.scheduler._submit(str)
        return str
    def map(self, func, *args, **kwds):
        return Mapper.map(self, func, *args, **kwds)
    map.__doc__ = ((Mapper.map.__doc__ or '')+(_launcher.__doc__ or '')) or None
    def __repr__(self):
        if self.scheduler:
            scheduler = self.scheduler.__class__.__name__
        else:
            scheduler = "None"
        mapargs = (self.__class__.__name__, scheduler)
        return "<pool %s(scheduler=%s)>" % mapargs
    pass

#FIXME: enable user to override 'mpirun'
class ParallelMapper(Mapper): #FIXME FIXME: stopped docs here
    """
Mapper base class for pipe-based mapping with mpi4py.
    """
    __nodes = None
    def __init__(self, *args, **kwds):
        """\nNOTE: if number of nodes is not given, will try to grab the number
of nodes from the associated scheduler, and failing will count the local cpus.
If workdir is not given, will default to scheduler's workdir or $WORKDIR.
If scheduler is not given, will default to only run on the current node.
If pickle is not given, will attempt to minimially use TemporaryFiles.

For more details, see the docstrings for the "map" method, or the man page
for the associated launcher (e.g mpirun, mpiexec).
        """
        Mapper.__init__(self, *args, **kwds)
        self.scatter = bool(kwds.get('scatter', False)) #XXX: hang w/ nodes=1 ?
       #self.nodes = kwds.get('nodes', None)
        if not len(args) and 'nodes' not in kwds:
            if self.scheduler:
                self.nodes = self.scheduler.nodes
            else:
                self.nodes = cpu_count()
        return
    if AbstractWorkerPool.__init__.__doc__: __init__.__doc__ = AbstractWorkerPool.__init__.__doc__ + __init__.__doc__
    def njobs(self, nodes):
        """convert node_string intended for scheduler to int number of nodes

compute int from node string. For example, parallel.njobs("4") yields 4
        """
        return int(str(nodes)) #XXX: this is a dummy function
    def _launcher(self, kdict={}):
        """prepare launch command for pipe-based execution

equivalent to:  (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
        """
        mydict = self.settings.copy()
        mydict.update(kdict)
        str = """%(python)s %(program)s %(progargs)s""" % mydict
        if self.scheduler:
            str = self.scheduler._submit(str)
        return str
    def map(self, func, *args, **kwds):
        return Mapper.map(self, func, *args, **kwds)
    map.__doc__ = ((Mapper.map.__doc__ or '')+(_launcher.__doc__ or '')) or None
    def __repr__(self):
        if self.scheduler:
            scheduler = self.scheduler.__class__.__name__
        else:
            scheduler = "None"
        mapargs = (self.__class__.__name__, self.nodes, scheduler)
        return "<pool %s(ncpus=%s, scheduler=%s)>" % mapargs
    def __get_nodes(self):
        """get the number of nodes in the pool"""
        return self.__nodes
    def __set_nodes(self, nodes):
        """set the number of nodes in the pool"""
        self.__nodes = self.njobs(nodes)
        return
    # interface
    nodes = property(__get_nodes, __set_nodes)
    pass

class Mpi(ParallelMapper):
    """
    """
    def njobs(self, nodes):
        """convert node_string intended for scheduler to mpirun node_string

compute mpirun task_string from node string of pattern = N[:TYPE][:ppn=P]
For example, mpirun.njobs("3:core4:ppn=2") yields 6
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
    def _launcher(self, kdict={}):
        """prepare launch command for parallel execution using mpirun

equivalent to:  mpiexec -np (nodes) (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
        """
        mydict = self.settings.copy()
        mydict.update(kdict)
       #if self.scheduler:
       #    mydict['nodes'] = self.njobs()
        str =  """%(mpirun)s -np %(nodes)s %(python)s %(program)s %(progargs)s""" % mydict
        if self.scheduler:
            str = self.scheduler._submit(str)
        return str
    def map(self, func, *args, **kwds):
        return ParallelMapper.map(self, func, *args, **kwds)
    map.__doc__ = ((ParallelMapper.map.__doc__ or '')+(_launcher.__doc__ or '')) or None
    pass

class Slurm(ParallelMapper):
    """
    """
    def njobs(self, nodes):
        """convert node_string intended for scheduler to srun node_string

compute srun task_string from node string of pattern = N[:ppn=P][,partition=X]
For example, srun.njobs("3:ppn=2,partition=foo") yields '3 -N2'
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
    def _launcher(self, kdict={}):
        """prepare launch for parallel execution using srun

equivalent to:  srun -n(nodes) (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4 -N1', ...}
        """
        mydict = self.settings.copy()
        mydict.update(kdict)
       #if self.scheduler:
       #    mydict['nodes'] = self.njobs()
        str =  """srun -n%(nodes)s %(python)s %(program)s %(progargs)s""" % mydict
        if self.scheduler:
            str = self.scheduler._submit(str)
        return str
    def map(self, func, *args, **kwds):
        return ParallelMapper.map(self, func, *args, **kwds)
    map.__doc__ = ((ParallelMapper.map.__doc__ or '')+(_launcher.__doc__ or '')) or None
    pass

class Alps(ParallelMapper):
    """
    """
    def njobs(self, nodes):
        """convert node_string intended for scheduler to aprun node_string

compute aprun task_string from node string of pattern = N[:TYPE][:ppn=P]
For example, aprun.njobs("3:core4:ppn=2") yields '3 -N 2'
        """
        nodestr = str(nodes)
        nodestr = nodestr.split(",")[0]  # remove appended -l expressions
        nodelst = nodestr.split(":")
        n = int(nodelst[0])
        nodelst = nodestr.split("ppn=")
        if len(nodelst) > 1:
            ppn = nodelst[1]
            ppn = int(ppn.split(":")[0])
            tasks = "%s -N %s" % (n, ppn)
        else:
            tasks = "%s" % n
        return tasks
    def _launcher(self, kdict={}):
        """prepare launch for parallel execution using aprun

equivalent to:  aprun -n (nodes) (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4 -N 1', ...}
        """
        mydict = self.settings.copy()
        mydict.update(kdict)
       #if self.scheduler:
       #    mydict['nodes'] = self.njobs()
        str =  """aprun -n %(nodes)s %(python)s %(program)s %(progargs)s""" % mydict
        if self.scheduler:
            str = self.scheduler._submit(str)
        return str
    def map(self, func, *args, **kwds):
        return ParallelMapper.map(self, func, *args, **kwds)
    map.__doc__ = ((ParallelMapper.map.__doc__ or '')+(_launcher.__doc__ or '')) or None
    pass


##### 'pre-configured' maps #####
# launcher + strategy
class MpiPool(Mpi):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = False
        Mpi.__init__(self, *args, **kwds)
    pass

class MpiScatter(Mpi):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = True
        Mpi.__init__(self, *args, **kwds)
    pass

class SlurmPool(Slurm):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = False
        Slurm.__init__(self, *args, **kwds)
    pass

class SlurmScatter(Slurm):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = True
        Slurm.__init__(self, *args, **kwds)
    pass

class AlpsPool(Alps):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = False
        Alps.__init__(self, *args, **kwds)
    pass

class AlpsScatter(Alps):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = True
        Alps.__init__(self, *args, **kwds)
    pass

# scheduler + launcher
class TorqueMpi(Mpi):
    def __init__(self, *args, **kwds):
        kwds['scheduler'] = Torque(*args, **kwds)
        kwds.pop('nodes', None)
        Mpi.__init__(self, **kwds)
    pass

class TorqueSlurm(Slurm):
    def __init__(self, *args, **kwds):
        kwds['scheduler'] = Torque(*args, **kwds)
        kwds.pop('nodes', None)
        Slurm.__init__(self, **kwds)
    pass

class MoabMpi(Mpi):
    def __init__(self, *args, **kwds):
        kwds['scheduler'] = Moab(*args, **kwds)
        kwds.pop('nodes', None)
        Mpi.__init__(self, **kwds)
    pass

class MoabSlurm(Slurm):
    def __init__(self, *args, **kwds):
        kwds['scheduler'] = Moab(*args, **kwds)
        kwds.pop('nodes', None)
        Slurm.__init__(self, **kwds)
    pass

# scheduler + launcher + strategy
class TorqueMpiPool(TorqueMpi):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = False
        TorqueMpi.__init__(self, *args, **kwds)
    pass

class TorqueMpiScatter(TorqueMpi):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = True
        TorqueMpi.__init__(self, *args, **kwds)
    pass

class TorqueSlurmPool(TorqueSlurm):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = False
        TorqueSlurm.__init__(self, *args, **kwds)
    pass

class TorqueSlurmScatter(TorqueSlurm):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = True
        TorqueSlurm.__init__(self, *args, **kwds)
    pass

class MoabMpiPool(MoabMpi):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = False
        MoabMpi.__init__(self, *args, **kwds)
    pass

class MoabMpiScatter(MoabMpi):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = True
        MoabMpi.__init__(self, *args, **kwds)
    pass

class MoabSlurmPool(MoabSlurm):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = False
        MoabSlurm.__init__(self, *args, **kwds)
    pass

class MoabSlurmScatter(MoabSlurm):
    def __init__(self, *args, **kwds):
        kwds['scatter'] = True
        MoabSlurm.__init__(self, *args, **kwds)
    pass



# backward compatibility
def launch(command):
    """ launch mechanism for prepared launch command"""
    mapper = Mapper()
    subproc = mapper._Mapper__launch(command)
   #pid = subproc.pid
    error = subproc.wait()           # block until all done
    if error: raise IOError("launch failed: %s" % command)
    return error

    
def mpirun_tasks(nodes):
    """
Helper function.
compute mpirun task_string from node string of pattern = N[:TYPE][:ppn=P]
For example, mpirun_tasks("3:core4:ppn=2") yields 6
    """
    mapper = Mpi()
    return mapper.njobs(nodes)


def srun_tasks(nodes):
    """
Helper function.
compute srun task_string from node string of pattern = N[:ppn=P][,partition=X]
For example, srun_tasks("3:ppn=2,partition=foo") yields '3 -N2'
    """
    mapper = Slurm()
    return mapper.njobs(nodes)


def aprun_tasks(nodes):
    """
Helper function.
compute aprun task_string from node string of pattern = N[:TYPE][:ppn=P]
For example, aprun_tasks("3:core4:ppn=2") yields '3 -N 2'
    """
    mapper = Alps()
    return mapper.njobs(nodes)


def serial_launcher(kdict={}):
    """
prepare launch for standard execution
syntax:  (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    """
    mapper = SerialMapper()
    return mapper._launcher(kdict)


def mpirun_launcher(kdict={}):
    """
prepare launch for parallel execution using mpirun
syntax:  mpiexec -np (nodes) (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    """
    mapper = Mpi()
    return mapper._launcher(kdict)


def srun_launcher(kdict={}):
    """
prepare launch for parallel execution using srun
syntax:  srun -n(nodes) (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4 -N1', ...}
    """
    mapper = Slurm()
    return mapper._launcher(kdict)


def aprun_launcher(kdict={}):
    """
prepare launch for parallel execution using aprun
syntax:  aprun -n(nodes) (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4 -N 1', ...}
    """
    mapper = Alps()
    return mapper._launcher(kdict)


def torque_launcher(kdict={}): #FIXME: update
    """
prepare launch for torque submission using mpiexec, srun, aprun, or serial
syntax:  echo \"mpiexec -np (nodes) (python) (program) (progargs)\" | qsub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)
syntax:  echo \"srun -n(nodes) (python) (program) (progargs)\" | qsub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)
syntax:  echo \"aprun -n (nodes) (python) (program) (progargs)\" | qsub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)
syntax:  echo \"(python) (program) (progargs)\" | qsub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4:nodetype:ppn=1', ...}
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    from .schedulers import torque_scheduler
    torque = torque_scheduler()  #FIXME: hackery
    if mydict['scheduler'] == torque.srun:
        mydict['tasks'] = srun_tasks(mydict['nodes'])
        str = """ echo \"srun -n%(tasks)s %(python)s %(program)s %(progargs)s\" | qsub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
    elif mydict['scheduler'] == torque.mpirun:
        mydict['tasks'] = mpirun_tasks(mydict['nodes'])
        str = """ echo \"%(mpirun)s -np %(tasks)s %(python)s %(program)s %(progargs)s\" | qsub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
    elif mydict['scheduler'] == torque.aprun:
        mydict['tasks'] = aprun_tasks(mydict['nodes'])
        str = """ echo \"aprun -n %(tasks)s %(python)s %(program)s %(progargs)s\" | qsub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
    else:  # non-mpi launch
        str = """ echo \"%(python)s %(program)s %(progargs)s\" | qsub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
    return str


def moab_launcher(kdict={}): #FIXME: update
    """
prepare launch for moab submission using srun, mpirun, aprun, or serial
syntax:  echo \"srun -n(nodes) (python) (program) (progargs)\" | msub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)
syntax:  echo \"%(mpirun)s -np (nodes) (python) (program) (progargs)\" | msub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)
syntax:  echo \"aprun -n (nodes) (python) (program) (progargs)\" | msub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)
syntax:  echo \"(python) (program) (progargs)\" | msub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4:ppn=1,partition=xx', ...}
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    from .schedulers import moab_scheduler
    moab = moab_scheduler()  #FIXME: hackery
    if mydict['scheduler'] == moab.mpirun:
        mydict['tasks'] = mpirun_tasks(mydict['nodes'])
        str = """ echo \"%(mpirun)s -np %(tasks)s %(python)s %(program)s %(progargs)s\" | msub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
    elif mydict['scheduler'] == moab.srun:
        mydict['tasks'] = srun_tasks(mydict['nodes'])
        str = """ echo \"srun -n%(tasks)s %(python)s %(program)s %(progargs)s\" | msub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
    elif mydict['scheduler'] == moab.aprun:
        mydict['tasks'] = aprun_tasks(mydict['nodes'])
        str = """ echo \"aprun -n %(tasks)s %(python)s %(program)s %(progargs)s\" | msub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
    else: # non-mpi launch
        str = """ echo \"%(python)s %(program)s %(progargs)s\" | msub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
    return str


def lsfmx_launcher(kdict={}): #FIXME: update
    """
prepare launch for Myrinet / LSF submission of parallel python using mpich_mx
syntax:  bsub -K -W(timelimit) -n (nodes) -o (outfile) -a mpich_mx -q (queue) -J (progname) mpich_mx_wrapper (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    #str = """ bsub -K -W%(timelimit)s -n %(nodes)s -o ./%%J.out -a mpich_mx -q %(queue)s -J %(progname)s mpich_mx_wrapper %(python)s %(program)s %(progargs)s""" % mydict
    str = """ bsub -K -W%(timelimit)s -n %(nodes)s -o %(outfile)s -a mpich_mx -q %(queue)s -J %(progname)s mpich_mx_wrapper %(python)s %(program)s %(progargs)s""" % mydict
    return str


def lsfgm_launcher(kdict={}): #FIXME: update
    """
prepare launch for Myrinet / LSF submission of parallel python using mpich_gm
syntax:  bsub -K -W(timelimit) -n (nodes) -o (outfile) -a mpich_gm -q (queue) -J (progname) gmmpirun_wrapper (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
    """
    mydict = defaults.copy()
    mydict.update(kdict)
    #str = """ bsub -K -W%(timelimit)s -n %(nodes)s -o ./%%J.out -a mpich_gm -q %(queue)s -J %(progname)s gmmpirun_wrapper %(python)s %(program)s %(progargs)s""" % mydict
    str = """ bsub -K -W%(timelimit)s -n %(nodes)s -o %(outfile)s -a mpich_gm -q %(queue)s -J %(progname)s gmmpirun_wrapper %(python)s %(program)s %(progargs)s""" % mydict
    return str


def all_launchers():
    import pyina.launchers as launchers
    L = ["launchers.%s" % f for f in  dir(launchers) if f[-8:] == "launcher"]
    return L


def all_launches(kdict = {}):
    import pyina.launchers as launchers, traceback, os.path
    stack = traceback.extract_stack()
    caller = stack[ -min(len(stack),2) ][0]
    #
    defaults['program'] = caller
    defaults['progname'] = os.path.basename(caller)
    #
    for key in defaults.keys():
        if key not in kdict:
            kdict[key] = defaults[key]
    L = all_launchers()
    #
    str = []
    for launcher in L:
        str.append(eval('%s(kdict)' % (launcher)))
        str.append('')
    return '\n'.join(str)


def __launch():
    doc = """
# Returns a sample command for launching parallel jobs. 
# Helpful in making docstrings, by allowing the following in your docstring
# "%%(launcher)s", and then doing string interpolation "{'launcher' : all_launches()}"
# and you will get:

%(launcher)s

# all_launches does a stack traceback to find the name of the program containing its caller.
# This allows interpolation of the __file__ variable into the mpi launch commands.

# Most flexibly, all_launches should be called with a dictionary. Here are the defaults. 
#  defaults = { 'timelimit' : '00:02',
#               'program' :  *name of the caller*,
#               'progname' :  *os.path.basename of the caller*,
#               'outfile' :  *path of the output file*,
#               'errfile' :  *path of the error file*,
#               'jobfile' :  *path of jobid file*,
#               'queue' :  'normal',
#               'python' :  '`which python`',
#               'nodes' :  '1',
#               'progargs' :  '',
#               'scheduler' :  '',
#             }
""" % {'launcher' : all_launches({'program':__file__, 'timelimit': '00:02', 'outfile':'./results.out'}) }
#""" % defaults.update({'launcher' : all_launches(**defaults)})
    return doc


if __name__=='__main__':
#   from mystic import helputil
#   helputil.paginate(__launch())

    print("python launch")
    defaults['program'] = "tools.py"
    launch(serial_launcher(defaults))

    print("serial launch")
    settings = {'python':'', 'program':"hostname"}
    launch(serial_launcher(settings))

# EOF
