#!/usr/bin/env python
 
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
