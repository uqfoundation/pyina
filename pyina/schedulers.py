#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2026 The Uncertainty Quantification Foundation.
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
    Sbatch         -

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

__all__ = ['Scheduler', 'Torque', 'Moab', 'Lsf', 'Sbatch', 'Scheduled']

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
        from numbers import Integral
        if isinstance(self.timelimit, Integral):
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
    def _tasks(self, nodes=None):
        if nodes is None: nodes = self.nodes
        return nodes
    def _nodes(self, tasks=None):
        if tasks is None: tasks = self.nodes
        return tasks
    def __repr__(self):
        if isinstance(self.nodes, type("")):
            nodes = "%s" % self._nodes() #XXX: changed so always "'%s'"
        else: nodes = self.nodes
        if isinstance(self.timelimit, type("")):
            timelimit = "'%s'" % self.timelimit
        else: timelimit = self.timelimit
        if isinstance(self.queue, type("")):
            queue = "'%s'" % self.queue
        else: queue = self.queue
        subargs = (self.__class__.__name__, nodes, timelimit, queue)
        return "<scheduler %s(nodes='%s', timelimit=%s, queue=%s)>" % subargs
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
        str = """echo \"""" + command + """\" | """
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
        str = """echo \"""" + command + """\" | """
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
    def _tasks(self, nodes=None):
        if nodes is None: nodes = self.nodes

        # short-circuit if already in correct form
        if not isinstance(nodes, type('')): return nodes
        if ' -R ' in nodes: return nodes

        # extract n, ppn, cpp
        nodestr = str(nodes) #XXX: N=X, where can have X=1,2
        nodelst = nodestr.split(":")
        n = int(nodelst[0])
        nodes = ppn = cpp = None
        for i in nodelst:
            if i.startswith('ppn='):
                ppn = int(i.split('=')[1])
            elif i.startswith('cpp='):
                cpp = int(i.split('=')[1])

        # prepare task string from n,ppn,cpp
        tasks = ''
        if cpp is not None:
            tasks += ' -R "affinity[core(%s)]"' % cpp
        tasks += ' -R "span[hosts=%s' % n
        if ppn is not None:
            tasks += ',ptile=%s]"' % ppn
            n *= ppn
        else:
            tasks += ']"'
        return "".join(["%s" % n, tasks])
    def _nodes(self, tasks=None):
        if tasks is None: tasks = self.nodes

        # short-circuit if already in correct form
        if not isinstance(tasks, type('')): return tasks

        # split on '-R'
        _tasks = [n.strip() for n in tasks.split('-R')]

        # first argument has to be tasks
        task = _tasks[0].split()[0]

        # find argument that contains 'ptile='
        ppn = [i for i in _tasks if 'ptile=' in i][-1] if 'ptile=' in tasks else None
        # extract ppn from ptile
        if ppn: ppn = [i.split('=')[-1].strip() for i in ppn.split('[')[-1].split(']')[0].split(',') if 'ptile' in i][0]

        # find argument that contains 'hosts='
        n = [i for i in _tasks if 'hosts=' in i][-1] if 'hosts=' in tasks else None
        # extract n from hosts
        if n: n = [i.split('=')[-1].strip() for i in n.split('[')[-1].split(']')[0].split(',') if 'hosts' in i][0]

        # find argument that contains 'affinity' / 'core'
        cpp = [i for i in _tasks if 'core(' in i][-1] if 'core(' in tasks else None
        # extract cpp from core and affinity
        if cpp: cpp = [i.split(',')[0].split('(')[-1].split(')')[0].strip() for i in cpp.split('[')[-1].split(']')[0].split(':') if 'core' in i][0]

        # build node string
        cpp = ':cpp=%s' % cpp if cpp else ''
        cpp = ''.join([cpp, (':ppn=%s' % ppn) if ppn else ''])
        ppn = n if n else (("%s" % int(task)//int(ppn)) if ppn else task)
        return (ppn + cpp) if cpp else ppn
    def _submit(self, command, kdict={}):
        """prepare the given command for submission with bsub

equivalent to:  bsub -K -W (timelimit) -n (tasks) -o (outfile) -e (errfile) -q (queue) -J (progname) "(command)"

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
        mydict['nodes'] = self._tasks(mydict['nodes'])
        # nodes is of the form: '50 -R "span[ptile=5]" -R "affinity[core(2)]"'
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
# for sbatch
# https://slurm.schedmd.com/sbatch.html

class Sbatch(Scheduler):
    """
Scheduler that leverages the slurm sbatch scheduler.
    """
    def _submit(self, command, kdict={}):
        """prepare the given command for submission with sbatch

equivalent to:  sbatch -n (tasks) -t (timelimit) -o (outfile) -e (errfile) -q (queue) -p (queue) --reservation=(queue) --wrap=\"(command)\"

NOTES:
    run non-python commands with: {'python':'', ...} 
    fine-grained resource utilization with: {'nodes':'1-16:4', ...}
    fine-grained resource allocation with: {'queue':'debug:partition=fast', ...}
        """
        mydict = self.settings.copy()
        mydict.update(kdict) #XXX: parse nodes if 'ppn=x' provided
        mydict['queue'] = self._queue(mydict['queue'])
        mydict['nodes'] = self._tasks(mydict['nodes'])
        #mydict['nodes'] = self._nnodes(mydict['nodes'], command)
        str = '''sbatch -n %(nodes)s -t %(timelimit)s -o %(outfile)s -e %(errfile)s %(queue)s --wrap=\"''' % mydict + command + '''\" &> %(jobfile)s''' % mydict
        return str
    def _tasks(self, nodes=None):
        if nodes is None: nodes = self.nodes
        nodestr = str(nodes) #XXX: N=X, where can have X=1-4 or X=1,2,3
        if nodestr.startswith(('"',"'")): nodestr = nodestr[1:-1]
        # short-circuit if missing required string contents?
        if ':ppn=' not in nodestr and ':cpp=' not in nodestr: return nodes
        #nodestr = nodestr.split(",")[0]  # remove appended -l expressions
        nodelst = nodestr.split(":")
        n = int(nodelst[0])
        nodes = ppn = cpp = None
        for i in nodelst:
            if i.startswith('ppn='):
                ppn = int(i.split('=')[1])
            elif i.startswith('cpp='):
                cpp = int(i.split('=')[1])
            #elif i.startswith('N='):
            #    nodes = int(i.split('=')[1])
        tasks = ""
        if cpp is not None:
            tasks += " --cpus-per-task=%s" % cpp
        #if nodes is not None:
        tasks += " -N%s" % n # nodes
        if ppn is not None:
            tasks += " --ntasks-per-node=%s" % ppn
            n *= ppn
        tasks = "".join(["%s" % n, tasks])
        return tasks
    def _nodes(self, tasks=None):
        if tasks is None: tasks = self.nodes
        nodes = tasks
        nrepr = None
        nproc = 1
        ncpus = None
        if isinstance(nodes, type("")):
            # short-circuit if missing required string contents?
            if ':ppn=' in nodes or ':cpp=' in nodes: return nodes
            if ' --ntasks-per-node' in nodes:
                nrepr = nodes.replace(' --ntasks-per-node', ':ppn')
                nodes,nproc = nodes.split(' --ntasks-per-node=')
                nproc = int(nproc.strip())
            if ' -N' in nodes:
                nodes,ncpus = nodes.split(' -N')
                ncpus = int(ncpus.strip())
                if nrepr is not None:
                    nrepr = nrepr.replace(' -N%s' % ncpus, '')
            ## roll into single int ##
            #n = 1
            #for i in nodes.split(' --cpus-per-task='):
            #    n *= int(i)
            #nodes = n
            if ' --cpus-per-task' in nodes:
                if nrepr is None: nrepr = nodes
                nrepr = nrepr.replace(' --cpus-per-task', ':cpp').strip()
                nodes,nrepr = nrepr.split(':',1)
                nodes = (int(nodes.strip())//nproc) if ncpus is None else ncpus
                nrepr = ':'.join(['%s' % nodes, nrepr])
                nodes = "'%s'" % nrepr.strip()
            else:
                if nrepr is None: nodes = int(nodes.strip())
                else:
                    nodes = (int(nodes.strip())//nproc) if ncpus is None else ncpus
                    nodes = ("'%s:ppn=%s'" % (nodes, nproc)).strip()
        if isinstance(nodes, type('')) and nodes.startswith(("'",'"')): nodes = nodes[1:-1]
        return nodes
    def _queue(self, queue):
        """parse the given queue string into reservation, partition, qos
        """
        if queue.startswith('--'): return queue # is already in the right form
        qstr = queue.split(":")
        qall = [s for s in qstr if '=' not in s]
        qdict = dict(reservation=qall[-1], partition=qall[-1], qos=qall[-1]) if qall else {}
        qall = [s for s in qstr if '=' in s]
        qdict.update(s.split("=") for s in qall)
        if 'p' in qdict: qdict['partition'] = qdict.pop('p')
        if 'q' in qdict: qdict['qos'] = qdict.pop('q')
        return ' '.join(['--'+k+'='+v for k,v in qdict.items()])
    def _jobs(self, nodes):
        return self._ntasks(nodes)[0]
    def _nnodes(self, nodes, command):
        if command.startswith('srun '): # split tasks and nodes
            nodes = self._ntasks(nodes)[-1]
            return ('-N %s ' % nodes) if nodes else ''
        return ('-N %s ' % nodes) if nodes else ''
    def _ntasks(self, nodes):
        if isinstance(nodes, int):
            return str(nodes), ''
        nodes = nodes.split()
        if len(nodes) < 2:
            tasks = ' '.join(nodes)
            jobs = ''
        elif nodes[1].startswith('--cpus-per-task='):
            tasks = ' '.join(nodes[:2])
            jobs = ' '.join(nodes[2:])
        else:
            tasks = nodes[0]
            jobs = ' '.join(nodes[1:])
        return tasks, jobs
    def submit(self, command):
        Scheduler.submit(self, command)
        return
    submit.__doc__ = _submit.__doc__.replace('prepare','submit').replace('for submission','') #XXX: hacky
    pass

# schedule defaults
from pyina.tools import which_scheduler
sched = which_scheduler()
if sched == 'qsub':
    Scheduled = Torque
elif sched == 'msub':
    Scheduled = Moab
elif sched == 'bsub':
    Scheduled = Lsf
elif sched == 'sbatch':
    Scheduled = Sbatch
else:
    Scheduled = Scheduler
del sched, which_scheduler


# backward compatibility
def sbatch_queue(queue):
    """
Helper function.
compute sbatch queue_string from queuestring of pattern = R[:partition=P][qos=Q]
For example, sbatch_queue("p=foo:q=bar") yields '--partition=foo --qos=bar'
    """
    mapper = Sbatch()
    return mapper._queue(queue)

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

class sbatch_scheduler(object):
    """sbatch scheduler -- configured for mpirun, srun, aprun, or serial"""
    mpirun = "sbatch_mpirun"
    srun = "sbatch_srun"
    aprun = "sbatch_aprun"
    serial = "sbatch_serial"
    pass

def all_schedulers():
    import pyina.schedulers as schedulers
    L = ["schedulers.%s" % f for f in  dir(schedulers) if f[-9:] == "scheduler"]
    return L


if __name__=='__main__':
    print(all_schedulers())

# EOF
