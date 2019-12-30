#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
This module contains the base of map and pipe interfaces to the mpi4py module.

Pipe methods provided:
    ???

Map methods provided:
    map            - blocking and ordered worker pool        [returns: list]

Base classes:
    Mapper         - base class for pipe-based mapping


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
    >>> print pool.map(pow, [1,2,3,4], [5,6,7,8])

Several common configurations are available as pre-configured maps.
The following is identical to the above example:

    >>> # instantiate and configure a pre-configured worker pool
    >>> from pyina.launchers import TorqueMpiPool
    >>> config = {'nodes'='32:ppn=4', 'queue':'dedicated', 'timelimit':'11:59'}
    >>> pool = TorqueMpiPool(**config)
    >>>
    >>> # do a blocking map on the chosen function
    >>> print pool.map(pow, [1,2,3,4], [5,6,7,8])


Notes
=====

See pyina.launchers and pyina.schedulers for more launchers and schedulers.

"""
__all__ = ['_save', '_debug', 'Mapper', 'world']


##### shortcuts #####
from mpi4py import MPI
world = MPI.COMM_WORLD
# (also: world.rank, world.size)
import dill
try:
    getattr(MPI,'pickle',getattr(MPI,'_p_pickle',None)).dumps = dill.dumps
    getattr(MPI,'pickle',getattr(MPI,'_p_pickle',None)).loads = dill.loads
except AttributeError:
    pass
#####################

from subprocess import Popen, call
from pathos.abstract_launcher import AbstractWorkerPool
from pathos.helpers import cpu_count
import os, os.path, sys
import tempfile
from dill.temp import dump, dump_source
from pyina.tools import which_python, which_mpirun, which_strategy

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


_pid = '.' + str(os.getpid()) + '.'
defaults = {
    'nodes' : str(cpu_count()),
    'program' : which_strategy(lazy=True) or 'ezscatter', # serialize to tempfile
    'mpirun' : which_mpirun() or 'mpiexec',
    'python' : which_python(lazy=True) or 'python',
    'progargs' : '',

    'outfile' : 'results%sout' % _pid,
    'errfile' : 'errors%sout' % _pid,
    'jobfile' : 'job%sid' % _pid,

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
If source is not given, will attempt to minimially use TemporaryFiles.
If workdir is not given, will default to scheduler's workdir or $WORKDIR.
If scheduler is not given, will default to only run on the current node.
If timeout is not given, will default to scheduler's timelimit or INF.

For more details, see the docstrings for the "map" method, or the man page
for the associated launcher (e.g mpirun, mpiexec).
        """
        AbstractWorkerPool.__init__(self, *args, **kwds)
        self.scheduler = kwds.get('scheduler', None)
        self.scatter = True #bool(kwds.get('scatter', True))
        self.source = bool(kwds.get('source', False))
        self.workdir = kwds.get('workdir', None)
        self.timeout = kwds.get('timeout', None)
        if self.timeout == None:
            if self.scheduler:
                from pyina.tools import isoseconds
                self.timeout = isoseconds(self.scheduler.timelimit)
            else:
                from numpy import inf
                self.timeout = inf  #XXX: better than defaults.timelimit ?
        elif isinstance(self.timeout, str):
            from pyina.tools import isoseconds
            self.timeout = isoseconds(self.timeout)
        if self.workdir == None:
            if self.scheduler:
                self.workdir = self.scheduler.workdir
            else:
                self.workdir = os.environ.get('WORKDIR', os.path.curdir)
        self.workdir = os.path.abspath(self.workdir)
        return
    if AbstractWorkerPool.__init__.__doc__: __init__.__doc__ = AbstractWorkerPool.__init__.__doc__ + __init__.__doc__
    def __settings(self):
        """apply default settings, then update with given settings"""
        env = defaults.copy()
        [env.update({k:v}) for (k,v) in self.__dict__.items() if k in defaults]
        [env.update({'nodes':v}) for (k,v) in self.__dict__.items() if k.endswith('nodes')] # deal with self.__nodes
        return env
    def __launch(self, command):
        """launch mechanism for prepared launch command"""
        executable = command.split("|")[-1].split()[0]
        from pox import which
        if not which(executable):
            raise IOError("launch failed: %s not found" % executable)
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
    def _save_in(self, *args):
        """save input tempfiles
    - path to pickled function source (e.g. 'my_func.py or 'my_func.pik')
    - path to pickled function inputs (e.g. 'my_args.arg')
        """
        # should check 'if modfilename' and 'if argfilename'
        modfilename = args[0]
        argfilename = args[1]
        modext = os.path.splitext(os.path.basename(modfilename))[-1]
        argext = os.path.splitext(os.path.basename(argfilename))[-1]
        # getsource; FUNC
        call('cp -f %s modfile%s' % (modfilename, modext), shell=True)
        # pickled inputs
        call('cp -f %s argfile%s' % (argfilename, argext), shell=True)
        return
    def _save_out(self, *args):
        """save output tempfiles
    - path to pickled function output (e.g. 'my_results')
        """
        # should check 'if resfilename'
        resfilename = args[0]
        resext = os.path.splitext(os.path.basename(resfilename))[-1]
        # pickled output
        call('cp -f %s resfile%s' % (resfilename, resext), shell=True)
        return
    def _cleanup(self, *args):
        """clean-up any additional tempfiles
    - path to pickled function output (e.g. 'my_results')
    - path to pickled function source (e.g. 'my_func.py or 'my_func.pik')
    - path to pickled function inputs (e.g. 'my_args.arg')
        """
        resfilename = args[0]
        call('rm -f %s' % resfilename, shell=True)
        if not self.source:
            # do nothing
            return
        modfilename = args[1]
        argfilename = args[2]
        call('rm -f %sc' % modfilename, shell=True)
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
            kwds['onall'] = kwds.get('onall', True)
        else:
            kwds['onall'] = kwds.get('onall', True) #XXX: has pickling issues
        config = {}
        config['program'] = which_strategy(self.scatter, lazy=True)

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
        if _SAVE[0]:
            self._save_in(modfile.name, argfile.name) # func, pickled input
        # create any necessary job files
        if self.scheduler: config.update(self.scheduler._prepare())
        ######################################################################
        # build the launcher command
        command = self._launcher(config)
        log.info('(skipping): %s' % command)
        if log.level == logging.DEBUG:
            error = False
            res = []
        else:
            try:
                subproc = self.__launch(command) # sumbit the jobs
                #print "after __launch"
               #pid = subproc.pid                # get process id
                error = subproc.wait()           # block until all done
                ## just to be sure... here's a loop to wait for results file ##
                maxcount = self.timeout; counter = 0
                #print "before wait"
                while not os.path.exists(resfilename):
                    call('sync', shell=True)
                    from time import sleep
                    sleep(1); counter += 1
                    if counter >= maxcount:
                        print("Warning: exceeded timeout (%s s)" % maxcount)
                        break
                #print "after wait"
                # read result back
                res = dill.load(open(resfilename,'rb'))
                #print "got result"
            except:
                error = True
                #print "got error"
        ######################################################################

        # cleanup files
        if _SAVE[0] and log.level == logging.WARN:
            self._save_out(resfilename) # pickled output
        self._cleanup(resfilename, modfile.name, argfile.name)
        if self.scheduler and not _SAVE[0]: self.scheduler._cleanup()
        if error:
            raise IOError("launch failed: %s" % command)
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


# EOF
