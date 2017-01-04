#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE
"""
Similar to test_mogi2, but with capabilities factored into a MasterSlaveController class

"""
raise NotImplementedError, "tests the desired (i.e. future) mpisolver interface..."

from pyina.solvers import mpisolver
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

if __name__ == "__main__":
    import journal
    journal.info("mpirun").activate()
    journal.debug("simple").activate()
    #journal.debug("pyina.receiveString").activate()
    from mystic.models import mogi; forward_mogi = mogi.evaluate
    
    app = mpisolver.MasterSlaveController()
    app.forward_model = forward_mogi
    app.inventory.launcher.inventory.nodes = 4
    app.run()

# End of file
