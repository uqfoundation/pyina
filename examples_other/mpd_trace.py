#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE
"""
run three basic tests of the MPI installation
"""

import subprocess
CPI = "~/src/mpich-1.0.7/examples/cpi"

command = 'mpdtrace'
print "\nlaunch: %s" % command
subprocess.call(command, shell=True)

command = 'mpdringtest 10'
print "\nlaunch: %s" % command
subprocess.call(command, shell=True)

command = 'mpiexec -n 4 hostname'
print "\nlaunch: %s" % command
subprocess.call(command, shell=True)

#command = 'mpiexec -n 1 %s' % CPI
#print "\nlaunch: %s" % command
#subprocess.call(command, shell=True)

# End of file
