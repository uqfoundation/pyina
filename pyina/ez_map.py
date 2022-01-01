#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
The ez_map function is a helper to parallel_map to further
simplify parallel programming.  Primarily ez_map provides
a standard interface for parallel_map, and facilitates
running parallel jobs with serial python.


Usage
=====

A call to ez_map will roughly follow this example:
    >>> # get the parallel mapper
    >>> from pyina.ez_map import ez_map
    >>> # construct a target function
    >>> def host(id):
    ...     import socket
    ...     return "Rank: %d -- %s" % (id, socket.gethostname())
    ...
    >>> # launch the parallel map of the target function
    >>> results = ez_map(host, range(100), nodes = 10)
    >>> for result in results:
    ...     print(result)


Implementation
==============

A parallel application is launched by using a helper script (e.g. `ezrun.py`)
as an intermediary between the MPI implementation of the parallel map
(e.g. `pyina.mpi_pool.parallel_map`) and the user's serial python.

The system call that submits the mpi job is blocking.  Reasons are::
    1) If the main program exits before the parallel job starts,
       any temp files used by ez_map will be lost.
    2) User is supposed to want to use the return value of the map,
       so blocking at the result of map shouldn't be a big hinderance.
    3) If we were to allow the call to be asynchronous, we would need
       to implement some kind of 'deferred' mechanism or job monitoring.
 
Argument movement for the argument list and the returned results are
pickled, while the mapped function is either saved to and imported
from a temporary file (e.g. `pyina.ez_map.ez_map`), or transferred
through serialization (e.g. `pyina.ez_map.ez_map2`).  Either implementation
has it's own advantages and weaknesses, and one mapper may succeed in
a case where the other may fail.

"""

defaults = {
    'progname' : 'ezscatter',
    }
from pyina.mpi import defaults as ezdefaults
ezdefaults.update(defaults)

from .launchers import launch, mpirun_tasks, srun_tasks, aprun_tasks
from .launchers import serial_launcher, mpirun_launcher, srun_launcher
from .launchers import aprun_launcher, torque_launcher, moab_launcher
from .schedulers import torque_scheduler, moab_scheduler

HOLD = []
sleeptime = 30  #XXX: the time between checking for results

#def ez_map(func, arglist, nodes=None, launcher=None, mapper=None):
def ez_map(func, *arglist, **kwds):
    """higher-level map interface for selected mapper and launcher

maps function 'func' across arguments 'arglist'.  arguments and results
are stored and sent as pickled strings, while function 'func' is inspected
and written as a source file to be imported.

Further Input:
    nodes -- the number of parallel nodes
    launcher -- the launcher object
    scheduler -- the scheduler object
    mapper -- the mapper object
    timelimit -- string representation of maximum run time (e.g. '00:02')
    queue -- string name of selected queue (e.g. 'normal')
    """
    import dill as pickle
    import os.path, tempfile, subprocess
    from pyina.tools import which_strategy
    # mapper = None (allow for use of default mapper)
    if 'mapper' in kwds:
        mapper = kwds['mapper']
        if mapper() == "mpi_pool": scatter = False
        elif mapper() == "mpi_scatter": scatter = True
        else: raise NotImplementedError("Mapper '%s' not found." % mapper())
        ezdefaults['program'] = which_strategy(scatter, lazy=True)
    # override the defaults
    if 'nnodes' in kwds: ezdefaults['nodes'] = kwds['nnodes']
    if 'nodes' in kwds: ezdefaults['nodes'] = kwds['nodes']
    if 'timelimit' in kwds: ezdefaults['timelimit'] = kwds['timelimit']
    if 'queue' in kwds: ezdefaults['queue'] = kwds['queue']
    # set the scheduler & launcher (or use the given default)
    if 'launcher' in kwds: launcher = kwds['launcher']
    else: launcher = mpirun_launcher  #XXX: default = non_mpi?
    if 'scheduler' in kwds: scheduler = kwds['scheduler']
    else: scheduler = ''
    # set scratch directory (most often required for queue launcher)
    if 'workdir' in kwds: ezdefaults['workdir'] = kwds['workdir']
    else:
        if launcher in [torque_launcher, moab_launcher] \
        or scheduler in [torque_scheduler, moab_scheduler]:
            ezdefaults['workdir'] = os.path.expanduser("~")

    from dill.temp import dump, dump_source
    # write func source to a NamedTemporaryFile (instead of pickle.dump)
    # ezrun requires 'FUNC = <function>' to be included as module.FUNC
    modfile = dump_source(func, alias='FUNC', dir=ezdefaults['workdir'])
    # standard pickle.dump of inputs to a NamedTemporaryFile
    kwd = {'onall':kwds.get('onall',True)}
    argfile = dump((arglist,kwd), suffix='.arg', dir=ezdefaults['workdir'])
    # Keep the above return values for as long as you want the tempfile to exist

    resfilename = tempfile.mktemp(dir=ezdefaults['workdir'])
    modname = os.path.splitext(os.path.basename(modfile.name))[0] 
    ezdefaults['progargs'] = ' '.join([modname, argfile.name, resfilename, \
                                       ezdefaults['workdir']])
    #HOLD.append(modfile)
    #HOLD.append(argfile)

    if launcher in [torque_launcher, moab_launcher] \
    or scheduler in [torque_scheduler, moab_scheduler]:
        jobfilename = tempfile.mktemp(dir=ezdefaults['workdir'])
        outfilename = tempfile.mktemp(dir=ezdefaults['workdir'])
        errfilename = tempfile.mktemp(dir=ezdefaults['workdir'])
        ezdefaults['jobfile'] = jobfilename
        ezdefaults['outfile'] = outfilename
        ezdefaults['errfile'] = errfilename

    # get the appropriate launcher for the scheduler
    if scheduler in [torque_scheduler] and launcher in [mpirun_launcher]:
        launcher = torque_launcher
        ezdefaults['scheduler'] = scheduler().mpirun
    elif scheduler in [moab_scheduler] and launcher in [mpirun_launcher]:
        launcher = moab_launcher
        ezdefaults['scheduler'] = scheduler().mpirun

    elif scheduler in [torque_scheduler] and launcher in [srun_launcher]:
        launcher = torque_launcher
        ezdefaults['scheduler'] = scheduler().srun
    elif scheduler in [moab_scheduler] and launcher in [srun_launcher]:
        launcher = moab_launcher
        ezdefaults['scheduler'] = scheduler().srun

    elif scheduler in [torque_scheduler] and launcher in [aprun_launcher]:
        launcher = torque_launcher
        ezdefaults['scheduler'] = scheduler().aprun
    elif scheduler in [moab_scheduler] and launcher in [aprun_launcher]:
        launcher = moab_launcher
        ezdefaults['scheduler'] = scheduler().aprun

    elif scheduler in [torque_scheduler] and launcher in [serial_launcher]:
        launcher = torque_launcher
        ezdefaults['scheduler'] = scheduler().serial
    elif scheduler in [moab_scheduler] and launcher in [serial_launcher]:
        launcher = moab_launcher
        ezdefaults['scheduler'] = scheduler().serial
    #else: scheduler = None

    # counting on the function below to block until done.
    #print 'executing: ', launcher(ezdefaults)
    launch(launcher(ezdefaults)) #FIXME: use subprocessing

    if launcher in [torque_launcher, moab_launcher] \
    or scheduler in [torque_scheduler, moab_scheduler]:
        import time                              #BLOCKING
        while (not os.path.exists(resfilename)): #XXX: or out* to confirm start
            time.sleep(sleeptime) #XXX: wait for results... may infinite loop?
        subprocess.call('rm -f %s' % jobfilename, shell=True)
        subprocess.call('rm -f %s' % outfilename, shell=True)
        subprocess.call('rm -f %s' % errfilename, shell=True)

    # debuggery... output = function(inputs)
   #subprocess.call('cp -f %s modfile.py' % modfile.name, shell=True) # getsource; FUNC=func
   #subprocess.call('cp -f %s argfile.py' % argfile.name, shell=True) # pickled list of inputs
   #subprocess.call('cp -f %s resfile.py' % resfilename, shell=True)  # pickled list of output

    # read result back
    res = pickle.load(open(resfilename,'rb'))
    subprocess.call('rm -f %s' % resfilename, shell=True)
    subprocess.call('rm -f %sc' % modfile.name, shell=True)
    return res

#def ez_map2(func, arglist, nodes=None, launcher=None, mapper=None):
def ez_map2(func, *arglist, **kwds):
    """higher-level map interface for selected mapper and launcher

maps function 'func' across arguments 'arglist'.  arguments and results
are stored and sent as pickled strings, the function 'func' is also stored
and sent as pickled strings.  This is different than 'ez_map', in that
it does not use temporary files to store the mapped function.

Further Input:
    nodes -- the number of parallel nodes
    launcher -- the launcher object
    scheduler -- the scheduler object
    mapper -- the mapper object
    timelimit -- string representation of maximum run time (e.g. '00:02')
    queue -- string name of selected queue (e.g. 'normal')
"""
    import dill as pickle
    import os.path, tempfile, subprocess
    from pyina.tools import which_strategy
    # mapper = None (allow for use of default mapper)
    if 'mapper' in kwds:
        mapper = kwds['mapper']
        if mapper() == "mpi_pool": scatter = False
        elif mapper() == "mpi_scatter": scatter = True
        else: raise NotImplementedError("Mapper '%s' not found." % mapper())
        ezdefaults['program'] = which_strategy(scatter, lazy=True)
    # override the defaults
    if 'nnodes' in kwds: ezdefaults['nodes'] = kwds['nnodes']
    if 'nodes' in kwds: ezdefaults['nodes'] = kwds['nodes']
    if 'timelimit' in kwds: ezdefaults['timelimit'] = kwds['timelimit']
    if 'queue' in kwds: ezdefaults['queue'] = kwds['queue']
    # set the scheduler & launcher (or use the given default)
    if 'launcher' in kwds: launcher = kwds['launcher']
    else: launcher = mpirun_launcher  #XXX: default = non_mpi?
    if 'scheduler' in kwds: scheduler = kwds['scheduler']
    else: scheduler = ''
    # set scratch directory (most often required for queue launcher)
    if 'workdir' in kwds: ezdefaults['workdir'] = kwds['workdir']
    else:
        if launcher in [torque_launcher, moab_launcher] \
        or scheduler in [torque_scheduler, moab_scheduler]:
            ezdefaults['workdir'] = os.path.expanduser("~")

    from dill.temp import dump
    # standard pickle.dump of inputs to a NamedTemporaryFile
    modfile = dump(func, suffix='.pik', dir=ezdefaults['workdir'])
    kwd = {'onall':kwds.get('onall',True)}
    argfile = dump((arglist,kwd), suffix='.arg', dir=ezdefaults['workdir'])
    # Keep the above return values for as long as you want the tempfile to exist

    resfilename = tempfile.mktemp(dir=ezdefaults['workdir'])
    ezdefaults['progargs'] = ' '.join([modfile.name,argfile.name,resfilename, \
                                       ezdefaults['workdir']])
    #HOLD.append(modfile)
    #HOLD.append(argfile)

    if launcher in [torque_launcher, moab_launcher] \
    or scheduler in [torque_scheduler, moab_scheduler]:
        jobfilename = tempfile.mktemp(dir=ezdefaults['workdir'])
        outfilename = tempfile.mktemp(dir=ezdefaults['workdir'])
        errfilename = tempfile.mktemp(dir=ezdefaults['workdir'])
        ezdefaults['jobfile'] = jobfilename
        ezdefaults['outfile'] = outfilename
        ezdefaults['errfile'] = errfilename

    # get the appropriate launcher for the scheduler
    if scheduler in [torque_scheduler] and launcher in [mpirun_launcher]:
        launcher = torque_launcher
        ezdefaults['scheduler'] = scheduler().mpirun
    elif scheduler in [moab_scheduler] and launcher in [mpirun_launcher]:
        launcher = moab_launcher
        ezdefaults['scheduler'] = scheduler().mpirun

    elif scheduler in [torque_scheduler] and launcher in [srun_launcher]:
        launcher = torque_launcher
        ezdefaults['scheduler'] = scheduler().srun
    elif scheduler in [moab_scheduler] and launcher in [srun_launcher]:
        launcher = moab_launcher
        ezdefaults['scheduler'] = scheduler().srun

    elif scheduler in [torque_scheduler] and launcher in [aprun_launcher]:
        launcher = torque_launcher
        ezdefaults['scheduler'] = scheduler().aprun
    elif scheduler in [moab_scheduler] and launcher in [aprun_launcher]:
        launcher = moab_launcher
        ezdefaults['scheduler'] = scheduler().aprun

    elif scheduler in [torque_scheduler] and launcher in [serial_launcher]:
        launcher = torque_launcher
        ezdefaults['scheduler'] = scheduler().serial
    elif scheduler in [moab_scheduler] and launcher in [serial_launcher]:
        launcher = moab_launcher
        ezdefaults['scheduler'] = scheduler().serial
    #else: scheduler = None

    # counting on the function below to block until done.
    #print 'executing: ', launcher(ezdefaults)
    launch(launcher(ezdefaults)) #FIXME: use subprocessing

    if launcher in [torque_launcher, moab_launcher] \
    or scheduler in [torque_scheduler, moab_scheduler]:
        import time                              #BLOCKING
        while (not os.path.exists(resfilename)): #XXX: or out* to confirm start
            time.sleep(sleeptime) #XXX: wait for results... may infinite loop?
        subprocess.call('rm -f %s' % jobfilename, shell=True)
        subprocess.call('rm -f %s' % outfilename, shell=True)
        subprocess.call('rm -f %s' % errfilename, shell=True)

    # read result back
    res = pickle.load(open(resfilename,'rb'))
    subprocess.call('rm -f %s' % resfilename, shell=True)
    return res
    

if __name__ == '__main__':
    print("simple tests are in examples/test_ezmap*.py")

# end of file
