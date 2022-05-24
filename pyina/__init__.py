#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

# author, version, license, and long description
__version__ = '0.2.6'
__author__ = 'Mike McKerns'

__doc__ = """
----------------------------------------------
pyina: MPI parallel map and cluster scheduling
----------------------------------------------

About Pyina
===========

The ``pyina`` package provides several basic tools to make MPI-based
parallel computing more accessable to the end user. The goal
of ``pyina`` is to allow the user to extend their own code to MPI-based
parallel computing with minimal refactoring.

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
or suggestions are highly appreciated.  A list of issues is located at https://github.com/uqfoundation/pyina/issues, with a legacy list maintained at https://uqfoundation.github.io/project/pathos/query.


Major Features
==============

``pyina`` provides a highly configurable parallel map interface
to running MPI jobs, with:

    - a map interface that extends the python ``map`` standard
    - the ability to submit batch jobs to a selection of schedulers
    - the ability to customize node and process launch configurations
    - the ability to launch parallel MPI jobs with standard python
    - ease in selecting different strategies for processing a work list


Current Release
===============

The latest released version of ``pyina`` is available at:

    https://pypi.org/project/pyina

``pyina`` is distributed under a 3-clause BSD license.


Development Version
===================

You can get the latest development version with all the shiny new features at:

    https://github.com/uqfoundation

If you have a new contribution, please submit a pull request.


Installation
============

``pyina`` can be installed with ``pip``::

    $ pip install pyina

A version of MPI must also be installed. Launchers in ``pyina`` that
submit to a scheduler will throw errors if the underlying scheduler is
not available, however a scheduler is not required for ``pyina`` to execute.


Requirements
============

``pyina`` requires:

    - ``python`` (or ``pypy``), **==2.7** or **>=3.7**
    - ``setuptools``, **>=42**
    - ``cython``, **>=0.29.22**
    - ``numpy``, **>=1.0**
    - ``mpi4py``, **>=1.3**
    - ``dill``, **>=0.3.5.1**
    - ``pox``, **>=0.3.1**
    - ``pathos``, **>=0.2.9**


More Information
================

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

Important classes and functions are found here:

    - ``pyina.mpi``           [the map API definition]
    - ``pyina.schedulers``    [all available schedulers] 
    - ``pyina.launchers``     [all available launchers] 

Mapping strategies are found here:

    - ``pyina.mpi_scatter``   [the scatter-gather strategy]
    - ``pyina.mpi_pool``      [the worker pool strategy]

``pyina`` also provides a convience script that helps navigate the
MPI environment. This script can be run from anywhere with::

    $ mpi_world

If may also be convienent to set a shell alias for the launch of 'raw'
mpi-python jobs. Set something like the following (for bash)::

    $ alias mpython1='mpiexec -np 1 `which python`'
    $ alias mpython2='mpiexec -np 2 `which python`'
    $ ...


Citation
========

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

"""

__license__ = """
Copyright (c) 2004-2016 California Institute of Technology.
Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
All rights reserved.

This software is available subject to the conditions and terms laid
out below. By downloading and using this software you are agreeing
to the following conditions.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met::

    - Redistribution of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    - Redistribution in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentations and/or other materials provided with the distribution.

    - Neither the names of the copyright holders nor the names of any of
      the contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

# shortcuts

# launchers
import pyina.launchers as launchers
import pyina.schedulers as schedulers

# mappers
import pyina.mpi as mpi

# strategies
import pyina.mpi_scatter as mpi_scatter
import pyina.mpi_pool as mpi_pool

# tools
from .tools import *

# backward compatibility
parallel_map = mpi_pool
parallel_map.parallel_map = mpi_pool.parallel_map
parallel_map2 = mpi_scatter
parallel_map2.parallel_map = mpi_scatter.parallel_map
#import ez_map
#import mappers


def license():
    """print license"""
    print(__license__)
    return

def citation():
    """print citation"""
    print (__doc__[-491:-118])
    return

# end of file
