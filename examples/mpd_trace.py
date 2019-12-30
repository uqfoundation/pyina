#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
run some basic tests of the MPI installation
"""

import subprocess

command = 'mpiexec -info'
print("\nlaunch: %s" % command)
subprocess.call(command, shell=True)

command = 'mpiexec -n 4 hostname'
print("\nlaunch: %s" % command)
subprocess.call(command, shell=True)

# End of file
