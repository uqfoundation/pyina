from pyina.mpi import defaults
from pyina.launchers import SerialMapper, Mpi, TorqueMpi
from pyina.schedulers import Torque

def test_launch():
    serial = SerialMapper()
    print "non-python serial launch:", serial
    settings = {'python':'', 'program':"hostname"}
    print serial._launcher(settings), "\n"

    print "serial python launch:", serial
    defaults['program'] = "tools.py"
    print serial._launcher(defaults), "\n"

    qsub = Torque()
    serial.scheduler = qsub
    print "scheduled serial launch:", serial
    settings = {'program':"tools.py"}
    print serial._launcher(settings), "\n"

    mpi = Mpi()
    print "non-scheduled parallel launch:", mpi
    print mpi._launcher(settings), "\n"

    qsub.nodes = '4:ppn=2'
    mpi.nodes = mpi.njobs(qsub.nodes)
    print "scheduled parallel launch:", "<inline>"
    print qsub._submit(mpi._launcher(settings)), "\n"

    mpi.scheduler = qsub
    print "scheduled parallel launch:", mpi
    print mpi._launcher(settings), "\n"

    print "scheduled parallel launch:", "<inline>"
    print Mpi(scheduler=Torque(nodes='4:ppn=2'))._launcher(settings), "\n"

    print "scheduled parallel launch:", "<inline>"
    print TorqueMpi(nodes='4:ppn=2')._launcher(settings), "\n"

    print "scheduled serial launch:", "<inline>"
    qsub.nodes = 1
    print qsub._submit(SerialMapper()._launcher(settings)), "\n"

if __name__ == '__main__':
    test_launch()
