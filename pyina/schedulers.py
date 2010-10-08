#!/usr/bin/env python
#
# mmckerns@caltech.edu
#
"""
tiny function wrapper to provide ez_map interface with schedulers

provides:
 scheduler_obj = scheduler()  interface
"""

class torque_scheduler(object):
    """torque scheduler object -- configured for mpirun, srun, or serial"""
    mpirun = "torque_mpirun"
    srun = "torque_srun"
    serial = "torque_serial"
    pass

class moab_scheduler(object):
    """moab scheduler object -- configured for mpirun, srun, or serial"""
    mpirun = "moab_mpirun"
    srun = "moab_srun"
    serial = "moab_serial"
    pass

def all_schedulers():
    import schedulers
    L = ["schedulers.%s" % f for f in  dir(schedulers) if f[-9:] == "scheduler"]
    return L


if __name__=='__main__':
    print all_schedulers()

# EOF
