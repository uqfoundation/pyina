#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                       Patrick Hung & Mike McKerns, Caltech
#                        (C) 1997-2010  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


"""
pyina: a MPI-based parallel mapper and launcher

The pyina package provides several basic tools to make MPI-based high-performance
computing more accessable to the end user.  The goal of pyina is to allow the user
to extend their package to MPI-based high-performance computing with minimal
refactoring of their own code.

The central element of pyina is the parallel map-reduce algorithm.  Pyina provides two strategies for executing the parallel-map, where a stragegy is the algorithm
for distributing the work list of jobs across the availble nodes.  These strategies
can be used in the "raw" (i.e. directly) to provide map-reduce to a user's own
mpi-active code.  However, pyina also provides the "ez_map" interface, which
provides a map-reduce interface that does not expose MPI internals to the user.
With ez_map, the user can launch their code using MPI with nearly zero refactoring
of their own code.

There are several ways that a user will want to launch their MPI code -- directly
with "mpirun" or "mpiexec", or by using a scheduler such as torque or slurm.
Pyina provides several 'launchers' that encapsulate the different methods of
launching a MPI job.

Pyina is part of pathos, a python package for heterogenous computing.
Pyina is in the early development stages, and any user feedback is
highly appreciated. Contact Mike McKerns [mmckerns at caltech dot edu]
with comments, suggestions, and any bugs you may find. A list of known
issues is maintained at http://dev.danse.us/trac/pathos/query.


Major Features
==============

Pyina provides ...
    -
    -
    - 


Current Release
===============

This release version is pyina-0.1a1. You can download it here.
The latest version of pyina is available from::
    http://dev.danse.us/trac/pathos

Pyina is distributed under a modified BSD license.


Installation
============

Pyina is packaged to install from source, so you must
download the tarball, unzip, and run the installer::
    [download]
    $ tar -xvzf pyina-0.1a1.tgz
    $ cd pyina-0.1a1
    $ python setup py build
    $ python setup py install

You will be warned of any missing dependencies and/or settings after
you run the "build" step above. Pyina depends on dill and mpi4py,
so you should install them first. A version of MPI must also be
installed. The launchers that post to a scheduler will throw errors
if the underlying scheduler is not available, although a scheduler
is not required for pyina to execute.

Alternately, pyina can be installed with easy_install::
    [download]
    $ easy_install -f . pyina


Requirements
============

Pyina requires::
    - python, version >= 2.5, version < 3.0
    - mpi4py, version >= 1.2.1
    - dill, version >= 0.1a1

Optional requirements::
    - setuptools, version >= 0.6
    - pyre, version >= 0.8
    - mystic, version >= 0.1a1


Usage Notes
===========

Probably the best way to get started is to look at a few of the
examples provided within pyina. See `pyina.examples` for a
set of scripts that demonstrate the configuration and launching of
mpi-based parallel jobs using the `ez_map` interface. Also see
`pyina.examples_other` for a set of scripts that test the more raw
internals of pyina.

Important classes and functions are found here::
    - pyina.pyina.ez_map        [the map-reduce API definition]
    - pyina.pyina.mappers       [all available strategies] 
    - pyina.pyina.launchers     [all available launchers] 

Mapping strategies are found here:
    - pyina.pyina.parallel_map  [the card-dealer strategy]
    - pyina.pyina.parallel_map2 [the equal-portion strategy]


If may also be convienent to set a shell alias for the launch of 'raw'
mpi-python jobs. Set something like the following (for bash):
    $ alias mpython1='mpiexec -np 1 `which python`'
    $ alias mpython2='mpiexec -np 2 `which python`'
    $ ...


More Information
================

Please see http://dev.danse.us/trac/pathos/pyina for further information.
"""

__license__ = """
This software is part of the open-source DANSE project at the California
Institute of Technology, and is available subject to the conditions and
terms laid out below. By downloading and using this software you are
agreeing to the following conditions.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met::

    - Redistribution of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    - Redistribution in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentations and/or other materials provided with the distribution.

    - Neither the name of the California Institute of Technology nor
      the names of its contributors may be used to endorse or promote
      products derived from this software without specific prior written
      permission.

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

Copyright (c) 2010 California Institute of Technology. All rights reserved.


If you use this software to do productive scientific research that leads to
publication, we ask that you acknowledge use of the software by citing the
following paper in your publication::

    "pathos: a framework for heterogeneous computing",
     Michael McKerns and Michael Aivazis, unpublished;
     http://dev.danse.us/trac/pathos

"""
# shortcuts
from mpi4py import MPI as mpi
mpi.world = mpi.COMM_WORLD
# (also: mpi.world.rank, mpi.world.size)

# launchers
import launchers

# mappers
#import pp_map
import ez_map
import mappers

# strategies
import parallel_map, parallel_map2

# tools
from tools import *

#def copyright():
#    """print copyright and reference"""
#    print __license__[-439:]
#    return

# end of file
