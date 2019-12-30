#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

from pyina.mpi import defaults
from pyina.launchers import SerialMapper, Mpi, TorqueMpi
from pyina.launchers import all_launches
from pyina.schedulers import Torque

def test_launches():
    # default launch commands for all launchers
    print("***** defaults for all launchers *****")
    print(all_launches())
    print("**************************************", "\n")

def test_launcher():
    # configured launch commands for selected launchers
    serial = SerialMapper()
    print("non-python serial launch:", serial)
    settings = {'python':'', 'program':"hostname"}
    print(serial._launcher(settings), "\n")

    print("serial python launch:", serial)
    defaults['program'] = "tools.py"
    defaults['progargs'] = "12345"
    print(serial._launcher(defaults), "\n")

    qsub = Torque()
    serial.scheduler = qsub
    print("scheduled serial launch:", serial)
    settings = {'program':"tools.py", 'progargs':'12345'}
    print(serial._launcher(settings), "\n")

    mpi = Mpi()
    print("non-scheduled parallel launch:", mpi)
    print(mpi._launcher(settings), "\n")

    qsub.nodes = '4:ppn=2'
    mpi.nodes = mpi.njobs(qsub.nodes)
    print("scheduled parallel launch:", mpi, "| Torque")
    print(qsub._submit(mpi._launcher(settings)), "\n")

    mpi.scheduler = qsub
    print("scheduled parallel launch:", mpi)
    print(mpi._launcher(settings), "\n")

    _mpi = Mpi(scheduler=Torque(nodes='4:ppn=2'))
    print("scheduled parallel launch:", _mpi)
    print(_mpi._launcher(settings), "\n")

    _mpi = TorqueMpi(nodes='4:ppn=2')
    print("scheduled parallel launch:", _mpi)
    print(_mpi._launcher(settings), "\n")

    qsub.nodes = 1
    serial = SerialMapper()
    print("scheduled serial launch:", serial, "| Torque")
    print(qsub._submit(serial._launcher(settings)), "\n")


if __name__ == '__main__':
    test_launches()
    test_launcher()

# EOF
