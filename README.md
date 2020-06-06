pyina
=====
MPI parallel map and cluster scheduling

About Pyina
-----------
The ``pyina`` package provides several basic tools to make MPI-based
parallel computing more accessable to the end user. The goal of ``pyina``
is to allow the user to extend their own code to MPI-based parallel
computing with minimal refactoring.

The central element of ``pyina`` is the parallel map algorithm.
``pyina`` currently provides two strategies for executing the parallel-map,
where a strategy is the algorithm for distributing the work list of
jobs across the availble nodes.  These strategies can be used *"in-the-raw"*
(i.e. directly) to provide the map algorithm to a user's own mpi-aware code.
Further, in ``pyina.mpi`` ``pyina`` provides pipe and map implementations
(known as *"easy map"*) that hide the MPI internals from the user. With the
*"easy map"*, the user can launch their code in parallel batch mode -- using
standard python and without ever having to write a line of MPI code.

There are several ways that a user would typically launch their code in
parallel -- directly with ``mpirun`` or ``mpiexec``, or through the use of a
scheduler such as *torque* or *slurm*. ``pyina`` encapsulates several of these
*"launchers"*, and provides a common interface to the different methods of
launching a MPI job.

``pyina`` is part of ``pathos``, a python framework for heterogeneous computing.
``pyina`` is in active development, so any user feedback, bug reports, comments,
or suggestions are highly appreciated.  A list of issues is located at https://github.com/uqfoundation/pyina/issues, with a legacy list maintained at https://uqfoundation.github.io/pathos-issues.html.


Major Features
--------------
``pyina`` provides a highly configurable parallel map interface
to running MPI jobs, with:

* a map interface that extends the python ``map`` standard
* the ability to submit batch jobs to a selection of schedulers
* the ability to customize node and process launch configurations
* the ability to launch parallel MPI jobs with standard python
* ease in selecting different strategies for processing a work list


Current Release
---------------
The latest released version of ``pyina`` is available at:
    https://pypi.org/project/pyina

``pyina`` is distributed under a 3-clause BSD license.


Development Version 
[![Documentation Status](https://readthedocs.org/projects/pyina/badge/?version=latest)](https://pyina.readthedocs.io/en/latest/?badge=latest)
[![Travis Build Status](https://img.shields.io/travis/uqfoundation/pyina.svg?label=build&logo=travis&branch=master)](https://travis-ci.org/uqfoundation/pyina)
[![codecov](https://codecov.io/gh/uqfoundation/pyina/branch/master/graph/badge.svg)](https://codecov.io/gh/uqfoundation/pyina)
[![Downloads](https://pepy.tech/badge/pyina)](https://pepy.tech/project/pyina)
-------------------
You can get the latest development version with all the shiny new features at:
    https://github.com/uqfoundation

If you have a new contribution, please submit a pull request.


More Information
----------------
Probably the best way to get started is to look at the documentation at
http://pyina.rtfd.io. Also see ``pyina.examples`` and ``pyina.tests``
for a set of scripts that demonstrate the configuration and launching of
mpi-based parallel jobs using the *"easy map"* interface. Also see
``pyina.examples_other`` for a set of scripts that test the more raw
internals of ``pyina``. You can run the tests with ``python -m pyina.tests``.
A script is included for querying, setting up, and tearing down an MPI
environment, see ``python -m pyina`` for more information. The source code
is generally well documented, so further questions may be resolved by
inspecting the code itself. Please feel free to submit a ticket on github,
or ask a question on stackoverflow (**@Mike McKerns**).
If you would like to share how you use ``pyina`` in your work, please send
an email (to **mmckerns at uqfoundation dot org**).


Citation
--------
If you use ``pyina`` to do research that leads to publication, we ask that you
acknowledge use of ``pyina`` by citing the following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    https://uqfoundation.github.io/pathos.html

Please see https://uqfoundation.github.io/pathos.html or
http://arxiv.org/pdf/1202.1056 for further information.

