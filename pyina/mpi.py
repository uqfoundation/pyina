#!/usr/bin/env python
"""
This module contains map and pipe interfaces to the mpi4py module, and bindings
to some common schedulers.

Pipe methods provided:
    ???

Map methods provided:
    map            - blocking and ordered worker pool        [returns: list]

Base classes:
    Mapper         - base class for pipe-based mapping
    SerialMapper   - base class for pipe-based mapping with python
    ParallelMapper - base class for pipe-based mapping with mpi4py
    Scheduler      - base class for cpu cluster scheduling

Schedulers:
    Torque         - 
    Moab           -
    Lsf            -

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
    >>> from pyina.mpi import Torque
    >>> config = {'nodes'='32:ppn=4', 'queue':'dedicated', 'timelimit':'11:59'}
    >>> torque = Torque(**config)
    >>> 
    >>> # instantiate and configure a worker pool
    >>> from pyina.mpi import Mpi
    >>> pool = Mpi(scheduler=torque)
    >>>
    >>> # do a blocking map on the chosen function
    >>> results = pool.map(pow, [1,2,3,4], [5,6,7,8])

Several common configurations are available as pre-configured maps.
The following is identical to the above example:

    >>> # instantiate and configure a pre-configured worker pool
    >>> from pyina.mpi import TorqueMpiPool
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

The schedulers provided here are built through pipes and not direct bindings,
and are currently somewhat limited on inspecting the status of a submitted job
and killing a submitted job. Currently, the use of pre-built scheduler job
files are also not supported.

"""
__all__ = ['_save', '_debug', 'Mapper', 'SerialMapper', 'ParallelMapper',
           'Scheduler', 'Torque', 'Moab', 'Lsf', 'Mpi', 'Slurm', 'Alps',
           'MpiPool', 'MpiScatter', 'SlurmPool', 'SlurmScatter', 'AlpsPool',
           'AlpsScatter', 'TorqueMpi', 'TorqueSlurm', 'MoabMpi', 'MoabSlurm',
           'TorqueMpiPool', 'TorqueMpiScatter', 'TorqueSlurmPool',
           'TorqueSlurmScatter', 'MoabMpiPool', 'MoabMpiScatter',
           'MoabSlurmPool', 'MoabSlurmScatter', 'world']

##### shortcuts #####
from mpi4py import MPI
world = MPI.COMM_WORLD
# (also: world.rank, world.size)
#####################

from subprocess import Popen
from abstract import AbstractWorkerPool
import os, os.path
import tempfile
import dill as pickle
from dill.temp import dump, dump_source

_HOLD = []
_SAVE = [False]
import logging
log = logging.getLogger("mpi")
log.addHandler(logging.StreamHandler())
def _save(boolean):
    """if True, save temporary files after pickling; useful for debugging"""
    if boolean: _SAVE[0] = True
    else:
         _SAVE[0] = False
         _HOLD = []
    return
def _debug(boolean):
    """if True, print debuging info and save temporary files after pickling"""
    if boolean:
        log.setLevel(logging.DEBUG)
        _save(True)
    else:
        log.setLevel(logging.WARN)
        _save(False)
    return

defaults = {
    'nodes' : '1',
    'program' : '`which ezscatter.py`',  # serialize to tempfile
    'python' : '`which python`' , #XXX: pox.which or which_python?
    'progargs' : '',

    'outfile' : 'results.out',
    'errfile' : 'errors.out',
    'jobfile' : 'jobid',

    'scheduler' : '',
    'timelimit' : '00:02',
    'queue' : 'normal',

    'workdir' : '.'
    }


#FIXME FIXME: __init__ and self for 'nodes' vs 'ncpus' is confused; see __repr__
class Mapper(AbstractWorkerPool):
    """
Mapper base class for pipe-based mapping.
    """
    def __init__(self, *args, **kwds):
        """\nNOTE: if number of nodes is not given, will default to 1.
If workdir is not given, will default to scheduler's workdir or $WORKDIR.
If scheduler is not given, will default to only run on the current node.
If source is not given, will attempt to minimially use TemporaryFiles.

For more details, see the docstrings for the "map" method, or the man page
for the associated launcher (e.g mpirun).
        """
        AbstractWorkerPool.__init__(self, *args, **kwds)
        self.scheduler = kwds.get('scheduler', None)
        self.scatter = True #bool(kwds.get('scatter', True))
        self.source = bool(kwds.get('source', False))
        self.workdir = kwds.get('workdir', None)
        if self.workdir == None:
            if self.scheduler:
                self.workdir = self.scheduler.workdir
            else:
                self.workdir = os.environ.get('WORKDIR', os.path.curdir)
        return
    __init__.__doc__ = AbstractWorkerPool.__init__.__doc__ + __init__.__doc__
    def __settings(self):
        env = defaults.copy()
        [env.update({k:v}) for (k,v) in self.__dict__.items() if k in defaults]
        return env
    def __launch(self, command):
        """launch mechanism for prepared launch command"""
        return Popen([command], shell=True) #FIXME: shell=True is insecure
    def _launcher(self, kdict={}):
        """prepare launch command based on current settings

equivalent to:  NotImplemented
        """
        mydict = self.settings.copy()
        mydict.update(kdict)
        str = "launch command missing" % mydict
        return str
    def _pickleargs(self, args, kwds):
        """pickle.dump args and kwds to tempfile"""
        # standard pickle.dump of inputs to a NamedTemporaryFile
        return dump((args, kwds), suffix='.arg', dir=self.workdir)
    def _modularize(self, func):
        """pickle.dump function to tempfile"""
        if not self.source:
            # standard pickle.dump of inputs to a NamedTemporaryFile
            return dump(func, suffix='.pik', dir=self.workdir)
        # write func source to a NamedTemporaryFile (instead of pickle.dump)
        # ez*.py requires 'FUNC = <function>' to be included as module.FUNC
        return dump_source(func, alias='FUNC', dir=self.workdir)
    def _modulenamemangle(self, modfilename):
        """mangle modulename string for use by mapper"""
        if not self.source:
            return modfilename
        return os.path.splitext(os.path.basename(modfilename))[0]
    def _cleanup(self, *args):
        """clean-up (or save) any additional tempfiles
    - path to pickled function source (e.g. 'my_func.py or 'my_func.pik')
    - path to pickled function inputs (e.g. 'my_args.arg')
        """
        if not self.source:
            # do nothing
            return
        # should check 'if modfilename' and 'if argfilename'
        modfilename = args[0]
        if _SAVE[0]:
            argfilename = args[1]
            os.system('cp -f %s modfile.py' % modfilename) # getsource; FUNC
            os.system('cp -f %s argfile.py' % argfilename) # pickled inputs
        os.system('rm -f %sc' % modfilename)
        return
    def map(self, func, *args, **kwds):
        """
The function 'func', it's arguments, and the results of the map are all stored
and shipped across communicators as pickled strings.

Optional Keyword Arguments:
    - onall  = if True, include master as a worker       [default: True]

NOTE: 'onall' defaults to True for both the scatter-gather and the worker
pool strategies. A worker pool with onall=True may have added difficulty
in pickling functions, due to asynchronous message passing with itself.

Additional keyword arguments are passed to 'func' along with 'args'.
        """
        # set strategy
        if self.scatter:
            strategy = "ezscatter.py"
            kwds['onall'] = kwds.get('onall', True)
        else:
            strategy = "ezpool.py"
            kwds['onall'] = kwds.get('onall', True) #XXX: has pickling issues
        config = {}
        config['program'] = '`which %s`' % strategy

        # serialize function and arguments to files
        modfile = self._modularize(func)
        argfile = self._pickleargs(args, kwds)
        # Keep the above handles as long as you want the tempfiles to exist
        if _SAVE[0]:
            _HOLD.append(modfile)
            _HOLD.append(argfile)
        # create an empty results file
        resfilename = tempfile.mktemp(dir=self.workdir)
        # process the module name
        modname = self._modulenamemangle(modfile.name)
        # build the launcher's argument string
        config['progargs'] = ' '.join([modname, argfile.name, \
                                       resfilename, self.workdir])

        #XXX: better with or w/o scheduler baked into command ?
        #XXX: better... if self.scheduler: self.scheduler.submit(command) ?
        #XXX: better if self.__launch modifies command to include scheduler ?
        ######################################################################
        # create any necessary job files
        if self.scheduler: config.update(self.scheduler._prepare())
        # build the launcher command
        command = self._launcher(config)
        log.info('(skipping): %s' % command)
        if log.level == logging.DEBUG:
            error = False
            res = []
        else:
            try:
                subproc = self.__launch(command) # sumbit the jobs
                error = subproc.wait()           # block until all done
                # read result back
                res = pickle.load(open(resfilename,'r'))
            except:
                error = True
        if self.scheduler: self.scheduler._cleanup()
        ######################################################################

        # cleanup files
        if _SAVE[0]:
            os.system('cp -f %s resfile.py' % resfilename)  # pickled output
        os.system('rm -f %s' % resfilename)
        self._cleanup(modfile.name, argfile.name)
        if error:
            raise IOError, "launch failed: %s" % command
        return res
   #def imap(self, func, *args, **kwds):
   #    """'non-blocking' and 'ordered'
   #    """
   #    return
   #def uimap(self, func, *args, **kwds):
   #    """'non-blocking' and 'unordered'
   #    """
   #    return
   #def amap(self, func, *args, **kwds):
   #    """'asynchronous' map(); use "get()" to retrieve results
   #    """
   #    return
    def __repr__(self):
        if self.scheduler:
            scheduler = self.scheduler.__class__.__name__
        else:
            scheduler = "None"
        mapargs = (self.__class__.__name__, self.nodes, scheduler)
        return "<pool %s(ncpus=%s, scheduler=%s)>" % mapargs
    # interface
    settings = property(__settings) #XXX: set?
    pass


class Scheduler(object):
    """
Scheduler base class for cpu cluster scheduling.
    """
    __nodes = defaults['nodes']
    def __init__(self, *args, **kwds):
        """
Important class members:
    nodes       - number (and potentially description) of workers
    queue       - name of the scheduler queue [default: 'normal']
    timelimit   - upper limit of clocktime for each scheduled job
    workdir     - associated $WORKDIR for scratch calculations/files

Other class members:
    jobfile     - name of the 'job' file pyina.mpi builds for the scheduler
    outfile     - name of the 'output' file the scheduler will write to
    errfile     - name of the 'error' file the scheduler will write to

NOTE: The format for timelimit is typically 'HH:MM' or 'HH:MM:SS', while
the format for nodes is typically 'n' or some variant of 'n:ppn=m' where
'n' is number of nodes and 'm' is processors per node.  For more details,
see the docstrings for the "sumbit" method, or the man page for the
associated scheduler.
        """
        self.__init(*args, **kwds)
        self.timelimit = kwds.get('timelimit', defaults['timelimit'])
        self.queue = kwds.get('queue', defaults['queue'])
        self.workdir = kwds.get('workdir', os.environ.get('WORKDIR', os.path.curdir))
       #self.workdir = kwds.get('workdir', os.environ.get('WORKDIR', os.path.expanduser("~"))
        self.jobfile = kwds.get('jobfile', defaults['jobfile'])
        self.outfile = kwds.get('outfile', defaults['outfile'])
        self.errfile = kwds.get('errfile', defaults['errfile'])

       #self.nodes = kwds.get('nodes', defaults['nodes'])
        return
    def __init(self, *args, **kwds):
        """default filter for __init__ inputs
        """
        # allow default arg for 'nodes', but not if in kwds
        if len(args):
            try:
                nodes = kwds['nodes']
                msg = "got multiple values for keyword argument 'nodes'"
                raise TypeError, msg
            except KeyError:
                nodes = args[0]
        else: nodes = kwds.get('nodes', self.__nodes)
        try: self.nodes = nodes
        except TypeError: pass  # then self.nodes is read-only
        return
    def __settings(self):
        """fetch the settings for the map (from defaults and self.__dict__)"""
        env = defaults.copy()
        [env.update({k:v}) for (k,v) in self.__dict__.items() if k in defaults]
        return env
    def _prepare(self):
        """prepare the scheduler files (jobfile, outfile, and errfile)"""
        jobfilename = tempfile.mktemp(dir=self.workdir)
        outfilename = tempfile.mktemp(dir=self.workdir)
        errfilename = tempfile.mktemp(dir=self.workdir)
        self.settings['jobfile'] = jobfilename
        self.settings['outfile'] = outfilename
        self.settings['errfile'] = errfilename
        return self.settings
    def _cleanup(self):
        """clean-up (or save) scheduler files (jobfile, outfile, and errfile)"""
        if not _SAVE[0]: #XXX: deleted when config gc'd?
            os.system('rm -f %s' % self.settings['jobfile'])
            os.system('rm -f %s' % self.settings['outfile'])
            os.system('rm -f %s' % self.settings['errfile'])
        return
    def fetch(self, outfile, subproc=None): #FIXME: what the hell is this???
        """fetch result from the results file"""
        try:
            error = subproc.wait()           # block until all done
            res = pickle.load(open(outfile,'r'))
        except:
            error = True
        if error:
            raise IOError, "fetch failed: %s" % outfile
        return res
    def _submit(self, command, kdict={}):
        """prepare the given command for the scheduler

equivalent to:  (command)
        """
        mydict = self.settings.copy()
        mydict.update(kdict)
        str = command #% mydict
        return str
    def submit(self, command):
        self._prepare()
        command = self._submit(command)
        log.info('(skipping): %s' % command)
        if log.level != logging.DEBUG:
            return self.__launch(command)
       #self._cleanup()
        return
    submit.__doc__ = _submit.__doc__.replace('prepare','submit').replace('command for','command to') #XXX: hacky
    def __launch(self, command):
        """launch mechanism for prepared launch command"""
        return Popen([command], shell=True) #FIXME: shell=True is insecure
    def __repr__(self):
        subargs = (self.__class__.__name__, self.nodes, self.timelimit, self.queue)
        return "<scheduler %s(nodes=%s, timelimit=%s, queue=%s)>" % subargs
    # interface
    settings = property(__settings) #XXX: set?
    pass

class Torque(Scheduler):
    """
Scheduler that leverages the torque scheduler.
    """
    def _submit(self, command, kdict={}):
        """prepare the given command for submission with qsub

equivalent to:  echo \"(command)\" | qsub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4:nodetype:ppn=1', ...}
        """
        mydict = self.settings.copy()
        mydict.update(kdict)
        str = """ echo \"""" + command + """\" | """
        str += """qsub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
        return str
    def submit(self, command):
        Scheduler.submit(self, command)
        return
    submit.__doc__ = _submit.__doc__.replace('prepare','submit').replace('for submission','') #XXX: hacky
    pass

class Moab(Scheduler):
    """
Scheduler that leverages the moab scheduler.
    """
    def _submit(self, command, kdict={}):
        """prepare the given command for submission with msub
`
equivalent to:  echo \"(command)\" | msub -l nodes=(nodes) -l walltime=(timelimit) -o (outfile) -e (errfile) -q (queue)

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'4:ppn=1,partition=xx', ...}
        """
        mydict = self.settings.copy()
        mydict.update(kdict)
        str = """ echo \"""" + command + """\" | """
        str += """msub -l nodes=%(nodes)s -l walltime=%(timelimit)s -o %(outfile)s -e %(errfile)s -q %(queue)s &> %(jobfile)s""" % mydict
        return str
    def submit(self, command):
        Scheduler.submit(self, command)
        return
    submit.__doc__ = _submit.__doc__.replace('prepare','submit').replace('for submission','') #XXX: hacky
    pass

class Lsf(Scheduler):
    """
Scheduler that leverages the lsf scheduler.
    """
    def __init__(self, *args, **kwds):
        Scheduler.__init__(self, *args, **kwds)
        mpich = kwds.get('mpich', '') # required for mpich_gm and mpich_mx
        if mpich in ['gm', 'mpich_gm', 'mpich-gm']: mpich = 'gm'
        elif mpich in ['mx', 'mpich_mx', 'mpich-mx']: mpich = 'mx'
        self.mpich = mpich
        return
    __init__.__doc__ = Scheduler.__init__.__doc__
    def _submit(self, command, kdict={}):
        """prepare the given command for submission with bsub

equivalent to:  bsub -K -W (timelimit) -n (nodes) -o (outfile) -e (errfile) -q (queue) -J (progname) "(command)"

NOTES:
    if mpich='mx', uses "-a mpich_mx mpich_mx_wrapper" instead of given launcher
    if mpich='gm', uses "-a mpich_gm gmmpirun_wrapper" instead of given launcher
    run non-python commands with: {'python':'', ...} 
        """
        mydict = self.settings.copy()
        # DISCOVER THE CALLER
       #import traceback
       #stack = traceback.extract_stack()
       #caller = stack[ -min(len(stack),2) ][0]
       #mydict['program'] = caller
        caller = mydict['program']
        progname = os.path.basename(caller)
        mydict['progname'] = progname.lstrip('`which ').rstrip('`')
        mydict.update(kdict)
       #str = """ bsub -K -W %(timelimit)s -n %(nodes)s -o ./%%J.out -e %(errfile)s -q %(queue)s -J %(progname)s -a mpich_gm gmmpirun_wrapper %(python)s %(program)s %(progargs)s &> %(jobfile)s""" % mydict
       #str = """ bsub -K -W %(timelimit)s -n %(nodes)s -o %(outfile)s -e %(errfile)s -q %(queue)s -J %(progname)s -a mpich_gm gmmpirun_wrapper %(python)s %(program)s %(progargs)s &> %(jobfile)s""" % mydict

       #str = """ echo \"""" + command + """\" | """
       #str += """bsub -K -W %(timelimit)s -n %(nodes)s -o %(outfile)s -e %(errfile)s -q %(queue)s -J %(progname)s %(esubapp) &> %(jobfile)s""" % mydict

        def _get_comm(comm):
            t = [] # should never return empty...
            s = comm.split()[1:] # strip off the launcher
            for x in s:
                if x.startswith('-') or x.isdigit(): continue
                t = s[s.index(x):] # don't want -n %(nodes)s either
                break
            return ' '.join(t)
        if self.mpich == 'gm':
            mydict['command'] = 'gmmpirun_wrapper ' + _get_comm(command)
            mydict['esubapp'] = "-a mpich_gm"
        elif self.mpich == 'mx':
            mydict['command'] = 'mpich_mx_wrapper ' + _get_comm(command)
            mydict['esubapp'] = "-a mpich_mx"
        else:
            mydict['command'] = command #'"' + command + '"'
            mydict['esubapp'] = ""
        str = """bsub -K -W %(timelimit)s -n %(nodes)s -o %(outfile)s -e %(errfile)s -q %(queue)s -J %(progname)s %(esubapp)s %(command)s &> %(jobfile)s""" % mydict
        return str
    def submit(self, command):
        Scheduler.submit(self, command)
        return
    submit.__doc__ = _submit.__doc__.replace('prepare','submit').replace('for submission','') #XXX: hacky
    pass
# some references for bsub and mpich_*:
# http://www.cisl.ucar.edu/docs/LSF/7.0.3/command_reference/bsub.cmdref.html
# http://www.mun.ca/hpc/lsf/examples.html
# http://its2.unc.edu/dci_components/lsf/mpich_parallel.htm
# http://ait.web.psi.ch/services/linux/hpc/mpich/using_mpich_gm.html

class SerialMapper(Mapper):
    """
Mapper base class for pipe-based mapping with python.
    """
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
    map.__doc__ = Mapper.map.__doc__ + _launcher.__doc__
    def __repr__(self):
        if self.scheduler:
            scheduler = self.scheduler.__class__.__name__
        else:
            scheduler = "None"
        mapargs = (self.__class__.__name__, scheduler)
        return "<pool %s(scheduler=%s)>" % mapargs
    pass

class ParallelMapper(Mapper): #FIXME FIXME: stopped docs here
    """
Mapper base class for pipe-based mapping with mpi4py.
    """
    __nodes = None
    def __init__(self, *args, **kwds):
        """\nNOTE: if number of nodes is not given, will try to grab the
number of nodes from the associated scheduler, and failing will default to 1.
If workdir is not given, will default to scheduler's workdir or $WORKDIR.
If scheduler is not given, will default to only run on the current node.
If pickle is not given, will attempt to minimially use TemporaryFiles.

For more details, see the docstrings for the "map" method, or the man page
for the associated launcher (e.g mpirun).
        """
        Mapper.__init__(self, *args, **kwds)
        self.scatter = bool(kwds.get('scatter', False)) #XXX: hang w/ nodes=1 ?
       #self.nodes = kwds.get('nodes', None)
        if not len(args) and not kwds.has_key('nodes'):
            if self.scheduler:
                self.nodes = self.scheduler.nodes
            else:
                self.nodes = '1'
        return
    __init__.__doc__ = AbstractWorkerPool.__init__.__doc__ + __init__.__doc__
    def njobs(self, nodes):
        """convert node_string intended for scheduler to int number of nodes

compute int from node string. For example, parallel.njobs("4") yields 4
        """
        return int(str(nodes)) #XXX: this is a dummy function
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

equivalent to:  mpirun -np (nodes) (python) (program) (progargs)

NOTES:
    run non-python commands with: {'python':'', ...} 
        """
        mydict = self.settings.copy()
        mydict.update(kdict)
       #if self.scheduler:
       #    mydict['nodes'] = self.njobs()
        str =  """mpirun -np %(nodes)s %(python)s %(program)s %(progargs)s""" % mydict
        if self.scheduler:
            str = self.scheduler._submit(str)
        return str
    def map(self, func, *args, **kwds):
        return ParallelMapper.map(self, func, *args, **kwds)
    map.__doc__ = ParallelMapper.map.__doc__ + _launcher.__doc__
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
    map.__doc__ = ParallelMapper.map.__doc__ + _launcher.__doc__
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
    map.__doc__ = ParallelMapper.map.__doc__ + _launcher.__doc__
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


# EOF
