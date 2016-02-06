#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

from __future__ import with_statement
import os

# set version numbers
stable_version = '0.1a1'
target_version = '0.2a1'
is_release = False

# check if easy_install is available
try:
#   import __force_distutils__ #XXX: uncomment to force use of distutills
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# generate version number
if os.path.exists('pyina/info.py'):
    # is a source distribution, so use existing version
    from pyina.info import this_version
elif stable_version == target_version:
    # we are building a stable release
    this_version = target_version
else:
    # we are building a distribution
    this_version = target_version + '.dev0'
    if is_release:
      from datetime import date
      today = "".join(date.isoformat(date.today()).split('-'))
      this_version += "-" + today

# get the license info
with open('LICENSE') as file:
    license_text = file.read()

# generate the readme text
long_description = \
"""-----------------------------------------------
pyina: a MPI-based parallel mapper and launcher
-----------------------------------------------

The pyina package provides several basic tools to make MPI-based
high-performance computing more accessable to the end user. The goal
of pyina is to allow the user to extend their own code to MPI-based
high-performance computing with minimal refactoring.

The central element of pyina is the parallel map-reduce algorithm.
Pyina currently provides two strategies for executing the parallel-map,
where a strategy is the algorithm for distributing the work list of
jobs across the availble nodes.  These strategies can be used "in-the-raw"
(i.e. directly) to provide map-reduce to a user's own mpi-aware code.
Further, in "pyina.mpi" pyina provides pipe and map implementations
(known as "easy map") that hide the MPI internals from the user. With the
"easy map", the user can launch their code in parallel batch mode -- using
standard python and without ever having to write a line of MPI code.

There are several ways that a user would typically launch their code in
parallel -- directly with "mpirun" or "mpiexec", or through the use of a
scheduler such as torque or slurm. Pyina encapsulates several of these
'launchers', and provides a common interface to the different methods of
launching a MPI job.

Pyina is part of pathos, a python framework for heterogenous computing.
Pyina is in the early development stages, and any user feedback is
highly appreciated. Contact Mike McKerns [mmckerns at caltech dot edu]
with comments, suggestions, and any bugs you may find. A list of known
issues is maintained at http://dev.danse.us/trac/pathos/query.


Major Features
==============

Pyina provides a highly configurable parallel map-reduce interface
to running MPI jobs, with::

    - a map-reduce interface that extends the python 'map' standard
    - the ability to submit batch jobs to a selection of schedulers
    - the ability to customize node and process launch configurations
    - the ability to launch parallel MPI jobs with standard python
    - ease in selecting different strategies for processing a work list


Current Release
===============

The latest stable release version is pyina-%(relver)s. You can download it here.
The latest stable version of pyina is always available at:

    http://dev.danse.us/trac/pathos


Development Release
===================

If you like living on the edge, and don't mind the promise
of a little instability, you can get the latest development
release with all the shiny new features at:

    http://dev.danse.us/packages.


Installation
============

Pyina is packaged to install from source, so you must
download the tarball, unzip, and run the installer::

    [download]
    $ tar -xvzf pyina-%(thisver)s.tgz
    $ cd pyina-%(thisver)s
    $ python setup py build
    $ python setup py install

You will be warned of any missing dependencies and/or settings after
you run the "build" step above. Pyina depends on dill, pox, pathos, and
mpi4py, so you should install them first. A version of MPI must also be
installed. Pyina's launchers that submit to a scheduler will throw errors
if the underlying scheduler is not available, however a scheduler is not
required for pyina to execute.

The current implementation of pyina required slight modifications
to one external dependency. This dependency and installation
instructions are provided in the `pyina.external` directory for users
installing without setuptools.

Alternately, pyina can be installed with easy_install::

    [download]
    $ easy_install -f . pyina


Requirements
============

Pyina requires::

    - python, version >= 2.5, version < 3.0
    - numpy, version >= 1.0
    - mpi4py, version >= 1.2.1
    - dill, version >= 0.2.5
    - pox, version >= 0.2.2
    - pathos, version >= 0.2a.dev0

Optional requirements::

    - setuptools, version >= 0.6
    - pyre, version == 0.8
    - mystic, version >= 0.2a2.dev0


Usage Notes
===========

Probably the best way to get started is to look at a few of the
examples provided within pyina. See `pyina.examples` for a
set of scripts that demonstrate the configuration and launching of
mpi-based parallel jobs using the `easy map` interface. Also see
`pyina.examples_other` for a set of scripts that test the more raw
internals of pyina.

Important classes and functions are found here::

    - pyina.pyina.mpi           [the map-reduce API definition]
    - pyina.pyina.schedulers    [all available schedulers] 
    - pyina.pyina.launchers     [all available launchers] 

Mapping strategies are found here::

    - pyina.pyina.mpi_scatter   [the scatter-gather strategy]
    - pyina.pyina.mpi_pool      [the worker pool strategy]

Pyina also provides two convience scripts that help navigate the
MPI environment. These scripts are installed to a directory on the
user's $PATH, and thus can be run from anywhere::

    - machines.py               [list the available MPI nodes]
    - mpi_world.py              [setup/teardown of the MPI environment]

If may also be convienent to set a shell alias for the launch of 'raw'
mpi-python jobs. Set something like the following (for bash)::

    $ alias mpython1='mpiexec -np 1 `which python`'
    $ alias mpython2='mpiexec -np 2 `which python`'
    $ ...


License
=======

Pyina is distributed under a 3-clause BSD license.

    >>> import pyina
    >>> print pyina.license()


Citation
========

If you use pyina to do research that leads to publication,
we ask that you acknowledge use of pyina by citing the
following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    http://dev.danse.us/trac/pathos


More Information
================

Please see http://dev.danse.us/trac/pathos or http://arxiv.org/pdf/1202.1056 for further information.

""" % {'relver' : stable_version, 'thisver' : this_version}

# write readme file
with open('README', 'w') as file:
    file.write(long_description)

# generate 'info' file contents
def write_info_py(filename='pyina/info.py'):
    contents = """# THIS FILE GENERATED FROM SETUP.PY
this_version = '%(this_version)s'
stable_version = '%(stable_version)s'
readme = '''%(long_description)s'''
license = '''%(license_text)s'''
"""
    with open(filename, 'w') as file:
        file.write(contents % {'this_version' : this_version,
                               'stable_version' : stable_version,
                               'long_description' : long_description,
                               'license_text' : license_text })
    return

# write info file
write_info_py()

# platform-specific instructions
sdkroot_set = False
from sys import platform
if platform[:3] == 'win':
    pass
else: #platform = linux or mac
     if platform[:6] == 'darwin':
         # mpi4py has difficulty building on a Mac
         # see special installation instructions here:
         # http://mpi4py.scipy.org/docs/usrman/install.html
         import os
         try:
             sdkroot = os.environ['SDKROOT']
         except KeyError:
             sdkroot = '/'
             os.environ['SDKROOT'] = sdkroot
             sdkroot_set = True
         pass
     pass

# build the 'setup' call
setup_code = """
setup(name="pyina",
    version='%s',
    maintainer="Mike McKerns",
    maintainer_email="mmckerns@caltech.edu",
    license="BSD",
    platforms=["Linux, Unix, Mac OSX"],
    description="a MPI-based parallel mapper and launcher",
    long_description = '''%s''',
    classifiers=(
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Physics Programming"),

    packages=['pyina'],
    package_dir={'pyina':'pyina'},
""" % (target_version, long_description)

# add dependencies
numpy_version = '>=1.0'
dill_version = '>=0.2.5'
pox_version = '>=0.2.2'
pathos_version = '>=0.2a1.dev0'
mpi4py_version = '>=1.2.1'
if platform[:6] == 'darwin':
  mpi4py_version = '>=1.2.2-pyina'
pypar_version = '>=2.1.4'
mystic_version = '>=0.2a2.dev0'
if has_setuptools:
    setup_code += """
        zip_safe = False,
        install_requires = ('numpy%s', 'mpi4py%s', 'dill%s', 'pox%s', 'pathos%s'),
        dependency_links = ["http://dev.danse.us/packages/"],
""" % (numpy_version, mpi4py_version, dill_version, pox_version, pathos_version)

# add the scripts, and close 'setup' call
setup_code += """
    scripts=['scripts/ezpool.py','scripts/ezscatter.py',
             'scripts/machines.py','scripts/mpi_world.py'])
"""

# exec the 'setup' code
exec setup_code

# if dependencies are missing, print a warning
try:
    import numpy
    import dill
    import pox
    import pathos
    import mpi4py #XXX: throws an error even though ok?
    #import pypar
except ImportError:
    print "\n***********************************************************"
    print "WARNING: One of the following dependencies may be unresolved:"
    print "    numpy %s" % numpy_version
    print "    dill %s" % dill_version
    print "    pox %s" % pox_version
    print "    pathos %s" % pathos_version
    print "    mpi4py %s" % mpi4py_version
#   print "    pypar %s (optional)" % pypar_version
    print "***********************************************************\n"

if sdkroot_set:
    print "\n***********************************************************"
    print "WARNING: One of following variables was set to a default:"
    print "    SDKROOT %s" % sdkroot
    print "***********************************************************\n"
else:
    pass

try:
    import mpi4py
except ImportError:
    print """
There is a bug in the mpi4py installer for MacOSX,
and a patch has been submitted to the mpi4py developers.
Until this patch is accepted in a release,
a modified version of mpi4py will be available here:
  http://dev.danse.us/packages/
or from the "external" directory included in the pyina source distribution.

Further, you may need to set the environment variable "SDKROOT",
as shown in the instructions for installing mpi4py:
  http://mpi4py.scipy.org/docs/usrman/install.html
"""


if __name__=='__main__':
    pass

# End of file
