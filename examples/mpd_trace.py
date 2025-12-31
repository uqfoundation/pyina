#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2026 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
run some basic tests of the MPI installation
"""

import subprocess

from pyina.tools import which_launcher
mpiexec = which_launcher()

if 'mpi' in mpiexec:
    command = '%s -info' % mpiexec
else:
    command = '%s --version' % mpiexec
print("\nlaunch: %s" % command)
subprocess.call(command, shell=True)

command = '%s -n 4 hostname' % mpiexec
print("\nlaunch: %s" % command)
subprocess.call(command, shell=True)

# End of file
