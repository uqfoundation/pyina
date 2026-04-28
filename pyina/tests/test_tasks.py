#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2026 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

from pyina.schedulers import *
from pyina.launchers import *

nodes = '10:cpp=2:ppn=5'
nodes_ = '10:ppn=5:cpp=2'
_nodes = "'10:cpp=2:ppn=5'"

tasks = '50 -R "span[ptile=5,hosts=10]" -R "affinity[core(2)]"'
tasks_ = '50 -R "affinity[core(2)]" -R "span[hosts=10,ptile=5]"'
_tasks = '50 -d 2 -N 5'
_tasks_ = '50 --cpus-per-task=2 -N10 --ntasks-per-node=5'

scheduler = Lsf(nodes)
launcher = Alps(scheduler=scheduler)
assert launcher._nodes() == scheduler._nodes()
assert launcher._tasks() == _tasks
assert scheduler._tasks() == tasks_

scheduler = Lsf(tasks)
launcher = Alps(scheduler=scheduler)
assert launcher._nodes() == scheduler._nodes()
assert launcher._tasks() == _tasks
assert scheduler._tasks() == tasks

scheduler = Sbatch(nodes)
launcher = Slurm(scheduler=scheduler)
assert launcher._nodes() == scheduler._nodes()
assert launcher._tasks() == scheduler._tasks()

scheduler = Sbatch(_tasks_)
launcher = Slurm(scheduler=scheduler)
assert launcher._nodes() == scheduler._nodes()
assert launcher._tasks() == scheduler._tasks()

scheduler = Torque(nodes)
launcher = Slurm(scheduler=scheduler)
assert launcher._nodes() == scheduler._nodes()
assert launcher._tasks() == _tasks_
assert scheduler._tasks() == nodes

scheduler = Torque(nodes)
launcher = Alps(scheduler=scheduler)
assert launcher._nodes() == scheduler._nodes()
assert launcher._tasks() == _tasks
assert scheduler._tasks() == nodes
