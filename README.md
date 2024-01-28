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
standard Python and without ever having to write a line of MPI code.

There are several ways that a user would typically launch their code in
parallel -- directly with ``mpirun`` or ``mpiexec``, or through the use of a
scheduler such as *torque* or *slurm*. ``pyina`` encapsulates several of these
*"launchers"*, and provides a common interface to the different methods of
launching a MPI job.

``pyina`` is part of ``pathos``, a Python framework for heterogeneous computing.
``pyina`` is in active development, so any user feedback, bug reports, comments,
or suggestions are highly appreciated.  A list of issues is located at https://github.com/uqfoundation/pyina/issues, with a legacy list maintained at https://uqfoundation.github.io/project/pathos/query.


Major Features
--------------
``pyina`` provides a highly configurable parallel map interface
to running MPI jobs, with:

* a map interface that extends the Python ``map`` standard
* the ability to submit batch jobs to a selection of schedulers
* the ability to customize node and process launch configurations
* the ability to launch parallel MPI jobs with standard Python
* ease in selecting different strategies for processing a work list


Current Release
[![Downloads](https://static.pepy.tech/personalized-badge/pyina?period=total&units=international_system&left_color=grey&right_color=blue&left_text=pypi%20downloads)](https://pepy.tech/project/pyina)
[![Stack Overflow](https://img.shields.io/badge/stackoverflow-get%20help-black.svg)](https://stackoverflow.com/questions/tagged/pyina)
---------------
The latest released version of ``pyina`` is available at:
    https://pypi.org/project/pyina

``pyina`` is distributed under a 3-clause BSD license.


Development Version
[![Support](https://img.shields.io/badge/support-the%20UQ%20Foundation-purple.svg?style=flat&colorA=grey&colorB=purple)](http://www.uqfoundation.org/pages/donate.html)
[![Documentation Status](https://readthedocs.org/projects/pyina/badge/?version=latest)](https://pyina.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/uqfoundation/pyina.svg?label=build&logo=travis&branch=master)](https://travis-ci.com/github/uqfoundation/pyina)
[![codecov](https://codecov.io/gh/uqfoundation/pyina/branch/master/graph/badge.svg)](https://codecov.io/gh/uqfoundation/pyina)
-------------------
You can get the latest development version with all the shiny new features at:
    https://github.com/uqfoundation

If you have a new contribution, please submit a pull request.


Installation
------------
``pyina`` can be installed with ``pip``::

    $ pip install pyina

A version of MPI must also be installed. Launchers in ``pyina`` that
submit to a scheduler will throw errors if the underlying scheduler is
not available, however a scheduler is not required for ``pyina`` to execute.


Requirements
------------
``pyina`` requires:

* ``python`` (or ``pypy``), **>=3.8**
* ``setuptools``, **>=42**
* ``cython``, **>=0.29.30**
* ``numpy``, **>=1.0**
* ``mpi4py``, **>=1.3**
* ``dill``, **>=0.3.8**
* ``pox``, **>=0.3.4**
* ``pathos``, **>=0.3.2**


More Information
----------------
Probably the best way to get started is to look at the documentation at
http://pyina.rtfd.io. Also see https://github.com/uqfoundation/pyina/tree/master/examples and ``pyina.tests`` for a set of scripts that demonstrate the
configuration and launching of mpi-based parallel jobs using the *"easy map"*
interface. You can run the tests with ``python -m pyina.tests``. A script is
included for querying, setting up, and tearing down an MPI environment, see
``python -m pyina`` for more information. The source code is generally well
documented, so further questions may be resolved by inspecting the code itself.
Please feel free to submit a ticket on github, or ask a question on
stackoverflow (**@Mike McKerns**). If you would like to share how you use
``pyina`` in your work, please send an email (to **mmckerns at uqfoundation dot
org**).

Important classes and functions are found here:

* ``pyina.mpi``           [the map API definition]
* ``pyina.schedulers``    [all available schedulers] 
* ``pyina.launchers``     [all available launchers] 

Mapping strategies are found here:

* ``pyina.mpi_scatter``   [the scatter-gather strategy]
* ``pyina.mpi_pool``      [the worker pool strategy]

``pyina`` also provides a convience script that helps navigate the
MPI environment. This script can be run from anywhere with::

    $ mpi_world

If may also be convienent to set a shell alias for the launch of 'raw'
mpi-python jobs. Set something like the following (for bash)::

    $ alias mpython1='mpiexec -np 1 `which python`'
    $ alias mpython2='mpiexec -np 2 `which python`'
    $ ...


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
    https://uqfoundation.github.io/project/pathos

Please see https://uqfoundation.github.io/project/pathos or
http://arxiv.org/pdf/1202.1056 for further information.

