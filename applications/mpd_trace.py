#!/usr/bin/env python
#
# 
import os
CPI = "~/src/mpich-1.0.7/examples/cpi"

command = 'mpdtrace'
print "\nlaunch: %s" % command
os.system(command)

command = 'mpdringtest 10'
print "\nlaunch: %s" % command
os.system(command)

command = 'mpiexec -n 4 hostname'
print "\nlaunch: %s" % command
os.system(command)

#command = 'mpiexec -n 1 %s' % CPI
#print "\nlaunch: %s" % command
#os.system(command)

# End of file
