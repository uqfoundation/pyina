#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
This module contains bindings to some common schedulers.

Base classes:
    Scheduler      - base class for cpu cluster scheduling

Schedulers:
    Torque         - 
    Moab           -
    Lsf            -

Usage
=====

A typical call to a pyina mpi map will roughly follow this example:

    >>> # instantiate and configure a scheduler
    >>> from pyina.schedulers import Torque
    >>> config = {'nodes'='32:ppn=4', 'queue':'dedicated', 'timelimit':'11:59'}
    >>> torque = Torque(**config)
    >>> 
    >>> # instantiate and configure a worker pool
    >>> from pyina.mpi import Mpi
    >>> pool = Mpi(scheduler=torque)
    >>>
    >>> # do a blocking map on the chosen function
    >>> results = pool.map(pow, [1,2,3,4], [5,6,7,8])


Notes
=====

The schedulers provided here are built through pipes and not direct bindings,
and are currently somewhat limited on inspecting the status of a submitted job
and killing a submitted job. Currently, the use of pre-built scheduler job
files are also not supported.

"""
"""
tiny function wrapper to provide ez_map interface with schedulers

provides:
 scheduler_obj = scheduler()  interface
"""

__all__ = ['Scheduler', 'Torque', 'Moab', 'Lsf']

from pyina.mpi import defaults
from subprocess import Popen, call
import os, os.path
import tempfile
import dill as pickle

import logging
log = logging.getLogger("schedulers")
log.addHandler(logging.StreamHandler())


class Scheduler(object):
    """
Scheduler base class for cpu cluster scheduling.
    """
    __nodes = 1
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
        if isinstance(self.timelimit, int):
            from pyina.tools import isoformat
            self.timelimit = isoformat(self.timelimit)
        self.queue = kwds.get('queue', defaults['queue'])
        self.workdir = kwds.get('workdir', os.environ.get('WORKDIR', os.path.curdir))
       #self.workdir = kwds.get('workdir', os.environ.get('WORKDIR', os.path.expanduser("~"))
        self.workdir = os.path.abspath(self.workdir)
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
                raise TypeError(msg)
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
        [env.update({'nodes':v}) for (k,v) in self.__dict__.items() if k.endswith('nodes')] # deal with self.__nodes
        return env
    def _prepare(self):
        """prepare the scheduler files (jobfile, outfile, and errfile)"""
        pid = '.' + str(os.getpid()) + '.'
        jobfilename = tempfile.mktemp(prefix='tmpjob'+pid, dir=self.workdir)
        outfilename = tempfile.mktemp(prefix='tmpout'+pid, dir=self.workdir)
        errfilename = tempfile.mktemp(prefix='tmperr'+pid, dir=self.workdir)
        self.jobfile = jobfilename
        self.outfile = outfilename
        self.errfile = errfilename
        d = {'jobfile':jobfilename,'outfile':outfilename,'errfile':errfilename}
        return d
    def _cleanup(self):
        """clean-up scheduler files (jobfile, outfile, and errfile)"""
        call('rm -f %s' % self.jobfile, shell=True)
        call('rm -f %s' % self.outfile, shell=True)
        call('rm -f %s' % self.errfile, shell=True)
        #print "called scheduler cleanup"
        return
    def fetch(self, outfile, subproc=None): #FIXME: call fetch after submit???
        """fetch result from the results file"""
        try:
            error = subproc.wait()           # block until all done
            res = pickle.load(open(outfile,'rb'))
        except:
            error = True
        if error:
            raise IOError("fetch failed: %s" % outfile)
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
            subproc = self.__launch(command)
           #pid = subproc.pid
            error = subproc.wait()           # block until all done
            if error: raise IOError("launch failed: %s" % command)
            return error
       #self._cleanup()
        return
    submit.__doc__ = _submit.__doc__.replace('prepare','submit').replace('command for','command to') #XXX: hacky
    def __launch(self, command):
        """launch mechanism for prepared launch command"""
        executable = command.split("|")[-1].split()[0]
        from pox.shutils import which
        if not which(executable):
            raise IOError("launch failed: %s not found" % executable)
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



# backward compatibility
class torque_scheduler(object):
    """torque scheduler -- configured for mpirun, srun, aprun, or serial"""
    mpirun = "torque_mpirun"
    srun = "torque_srun"
    aprun = "torque_aprun"
    serial = "torque_serial"
    pass

class moab_scheduler(object):
    """moab scheduler -- configured for mpirun, srun, aprun, or serial"""
    mpirun = "moab_mpirun"
    srun = "moab_srun"
    aprun = "moab_aprun"
    serial = "moab_serial"
    pass

def all_schedulers():
    import pyina.schedulers as schedulers
    L = ["schedulers.%s" % f for f in  dir(schedulers) if f[-9:] == "scheduler"]
    return L


if __name__=='__main__':
    print(all_schedulers())

# EOF
