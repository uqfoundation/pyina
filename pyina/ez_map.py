#!/usr/bin/env python

"""
The ez_map function is a helper to parallel_map to further
simplify parallel programming.  Primarily ez_map provides
a standard interface for parallel_map, and facilitates
running parallel jobs with serial python.


Usage
=====

A call to ez_map will roughly follow this example::

    >>> # get the parallel mapper
    >>> from pyina.ez_map import ez_map

    >>> # construct a target function
    >>> def host(id):
    ...     import socket
    ...     return "Rank: %d -- %s" % (id, socket.gethostname())

    >>> # launch the parallel map of the target function
    >>> results = ez_map(host, range(100), nnodes = 10)
    >>> print "\n".join(results)


Implementation
==============

A parallel application is launched by using a helper script (e.g. `ezrun.py`)
as an intermediary between the MPI implementation of the parallel map
(e.g. `pyina.parallel_map.parallel_map') and the user's serial python.

The system call that submits the mpi job is blocking.  Reasons are::
    1) If the main program exits before the parallel job starts,
       any temp files used by ez_map will be lost.
    2) User is supposed to want to use the return value of the map,
       so blocking at the result of map shouldn't be a big hinderance.
    3) If we were to allow the call to be asynchronous, we would need
       to implement some kind of 'deferred' mechanism or job monitoring.
 
Argument movement for the argument list and the returned results
pickled, while the mapped function is either saved to and imported
from a temporary file (e.g. `pyina.ez_map.ez_map`), or transferred
through serialization (e.g. `pyina.ez_map.ez_map2`).  Either implementation
has it's own advantages and weaknesses, and one mapper may succeed in
a case where the other may fail.

"""

def parse_from_history(object):
    """extract code blocks from a code object using stored history"""
    import readline, inspect
    lbuf = readline.get_current_history_length()
    code = [readline.get_history_item(i)+'\n' for i in range(1,lbuf)]
    lnum = 0
    codeblocks = []
    while lnum < len(code)-1:
       if code[lnum].startswith('def'):    
           block = inspect.getblock(code[lnum:])
           lnum += len(block)
           if block[0].startswith('def %s' % object.func_name):
               codeblocks.append(block)
       else:
           lnum +=1
    return codeblocks

def src(object):
    """Extract source code from python code object.

This function is designed to work with simple functions, and will not
work on any general callable. However, this function can extract source
code from functions that are defined interactively.
    """
    import inspect
    # no try/except (like the normal src function)
    if hasattr(object,'func_code') and object.func_code.co_filename == '<stdin>':
        # function is typed in at the python shell
        lines = parse_from_history(object)[-1]
    else:
        lines, lnum = inspect.getsourcelines(object)
    return ''.join(lines)

def func_pickle(func):
    """ write func source to a NamedTemporaryFile (instead of pickle.dump)
because ezrun requires 'FUNC = <function>' to be included as module.FUNC

NOTE: Keep the return value for as long as you want your file to exist !
    """
    import dill as pickle #XXX: to address costfactories
    import tempfile
    #XXX: assumes '.' is writable and on $PYTHONPATH
    file = tempfile.NamedTemporaryFile(suffix='.py', dir=ezdefaults['tmpdir'])
    file.write(''.join(src(func)))
    file.write('FUNC = %s\n' % func.func_name)
    file.flush()
    return file

def func_pickle2(func):
    """ standard pickle.dump of function to a NamedTemporaryFile """
    #XXX: below use '-%s.pik' % func.func_name ?
    return arg_pickle(func, suffix='.pik')

ezdefaults ={ 'timelimit' : '00:02',
              'file' : '`which ezrun2.py`',
              'progname' : 'ezrun2.py',
              'outfile' : 'results.out',
              'errfile' : 'errors.out',
              'jobfile' : 'jobid',
              'queue' : 'normal',
              'python' : '`which python`' ,
              'nodes' : '1',
              'progargs' : '',
              'tmpdir' : '.'
            }

from launchers import *

def arg_pickle(arglist, suffix='.arg'):
    """ standard pickle.dump of inputs to a NamedTemporaryFile """
    import dill as pickle
    import tempfile
    file = tempfile.NamedTemporaryFile(suffix=suffix, dir=ezdefaults['tmpdir'])
    pickle.dump(arglist, file)
    file.flush()
    return file

HOLD = []
sleeptime = 30  #XXX: the time between checking for results

#def ez_map(func, arglist, nnodes=None, launcher=None, mapper=None):
def ez_map(func, *arglist, **kwds):
    """higher-level map interface for selected mapper and launcher

maps function 'func' across arguments 'arglist'.  arguments and results
are stored and sent as pickled strings, while function 'func' is inspected
and written as a source file to be imported.

Further Input:
    nnodes -- the number of parallel nodes
    launcher -- the launcher object
    mapper -- the mapper object
    timelimit -- string representation of maximum run time (e.g. '00:02')
    queue -- string name of selected queue (e.g. 'normal')
    """
    import dill as pickle
    import os.path, tempfile, os
    # mapper = None (allow for use of default mapper)
    if kwds.has_key('mapper'):
        mapper = kwds['mapper']
        if mapper() == "parallel_map": ezmap = "ezrun.py"
        elif mapper() == "parallel_map2": ezmap = "ezrun2.py"
        else: raise NotImplementedError, "Mapper '%s' not found." % mapper()
        ezdefaults['file'] = '`which %s`' % ezmap
    # override the defaults
    if kwds.has_key('nnodes'): ezdefaults['nodes'] = kwds['nnodes']
    if kwds.has_key('timelimit'): ezdefaults['timelimit'] = kwds['timelimit']
    if kwds.has_key('queue'): ezdefaults['queue'] = kwds['queue']
    # set the launcher (or use the given default)
    if kwds.has_key('launcher'): launcher = kwds['launcher']
    else: launcher = mpirun_launcher  #XXX: default = non_mpi?
    # set scratch directory (most often required for queue launcher)
    if kwds.has_key('tmpdir'): ezdefaults['tmpdir'] = kwds['tmpdir']
    else:
        if launcher in [torque_launcher]:
            ezdefaults['tmpdir'] = os.path.expanduser("~")

    modfile = func_pickle(func)
    argfile = arg_pickle(arglist)
    resfilename = tempfile.mktemp(dir=ezdefaults['tmpdir'])
    modname = os.path.splitext(os.path.basename(modfile.name))[0] 
    ezdefaults['progargs'] = ' '.join([modname, argfile.name, resfilename, \
                                       ezdefaults['tmpdir']])
    #HOLD.append(modfile)
    #HOLD.append(argfile)

    if launcher == torque_launcher:
        jobfilename = tempfile.mktemp(dir=ezdefaults['tmpdir'])
        outfilename = tempfile.mktemp(dir=ezdefaults['tmpdir'])
        errfilename = tempfile.mktemp(dir=ezdefaults['tmpdir'])
        ezdefaults['jobfile'] = jobfilename
        ezdefaults['outfile'] = outfilename
        ezdefaults['errfile'] = errfilename

    # counting on the function below to block until done.
    #print 'executing: ', launcher(ezdefaults)
    launch(launcher(ezdefaults))

    if launcher == torque_launcher:
        import time
        while (not os.path.exists(outfilename)): #XXX: could wait for resfile...
            time.sleep(sleeptime) #XXX: wait for results to show up
        os.system('rm -f %s' % jobfilename)
        os.system('rm -f %s' % outfilename)
        os.system('rm -f %s' % errfilename)

    # debuggery... output = function(inputs)
   #os.system('cp -f %s modfile.py' % modfile.name) # function src; FUNC=func
   #os.system('cp -f %s argfile.py' % argfile.name) # pickled list of inputs
   #os.system('cp -f %s resfile.py' % resfilename)  # pickled list of output

    # read result back
    res = pickle.load(open(resfilename,'r'))
    os.system('rm -f %s' % resfilename)
    os.system('rm -f %sc' % modfile.name)
    return res

#def ez_map2(func, arglist, nnodes=None, launcher=None, mapper=None):
def ez_map2(func, *arglist, **kwds):
    """higher-level map interface for selected mapper and launcher

maps function 'func' across arguments 'arglist'.  arguments and results
are stored and sent as pickled strings, the function 'func' is also stored
and sent as pickled strings.  This is different than 'ez_map', in that
it does not use temporary files to store the mapped function.

Further Input:
    nnodes -- the number of parallel nodes
    launcher -- the launcher object
    mapper -- the mapper object
    timelimit -- string representation of maximum run time (e.g. '00:02')
    queue -- string name of selected queue (e.g. 'normal')
"""
    import dill as pickle
    import os.path, tempfile, os
    # mapper = None (allow for use of default mapper)
    if kwds.has_key('mapper'):
        mapper = kwds['mapper']
        if mapper() == "parallel_map": ezmap = "ezrun.py"
        elif mapper() == "parallel_map2": ezmap = "ezrun2.py"
        else: raise NotImplementedError, "Mapper '%s' not found." % mapper()
        ezdefaults['file'] = '`which %s`' % ezmap
    # override the defaults
    if kwds.has_key('nnodes'): ezdefaults['nodes'] = kwds['nnodes']
    if kwds.has_key('timelimit'): ezdefaults['timelimit'] = kwds['timelimit']
    if kwds.has_key('queue'): ezdefaults['queue'] = kwds['queue']
    # set the launcher (or use the given default)
    if kwds.has_key('launcher'): launcher = kwds['launcher']
    else: launcher = mpirun_launcher  #XXX: default = non_mpi?
    # set scratch directory (most often required for queue launcher)
    if kwds.has_key('tmpdir'): ezdefaults['tmpdir'] = kwds['tmpdir']
    else:
        if launcher in [torque_launcher]:
            ezdefaults['tmpdir'] = os.path.expanduser("~")

    modfile = func_pickle2(func)
    argfile = arg_pickle(arglist)
    resfilename = tempfile.mktemp(dir=ezdefaults['tmpdir'])
    ezdefaults['progargs'] = ' '.join([modfile.name,argfile.name,resfilename, \
                                       ezdefaults['tmpdir']])
    #HOLD.append(modfile)
    #HOLD.append(argfile)

    if launcher == torque_launcher:
        jobfilename = tempfile.mktemp(dir=ezdefaults['tmpdir'])
        outfilename = tempfile.mktemp(dir=ezdefaults['tmpdir'])
        errfilename = tempfile.mktemp(dir=ezdefaults['tmpdir'])
        ezdefaults['jobfile'] = jobfilename
        ezdefaults['outfile'] = outfilename
        ezdefaults['errfile'] = errfilename

    # counting on the function below to block until done.
    #print 'executing: ', launcher(ezdefaults)
    launch(launcher(ezdefaults))

    if launcher == torque_launcher:
        import time
        while (not os.path.exists(outfilename)): #XXX: could wait for resfile...
            time.sleep(sleeptime) #XXX: wait for results to show up
        os.system('rm -f %s' % jobfilename)
        os.system('rm -f %s' % outfilename)
        os.system('rm -f %s' % errfilename)

    # read result back
    res = pickle.load(open(resfilename,'r'))
    os.system('rm -f %s' % resfilename)
    return res
    

if __name__ == '__main__':
    print "simple tests are in examples/test_ezmap*.py"

# end of file
