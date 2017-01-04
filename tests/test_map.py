#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

verbose = False
delay = 0.01
items = 100


def busy_add(x,y, delay=0.01):
    for n in range(x):
       x += n
    for n in range(y):
       y -= n
    import time
    time.sleep(delay)
    return x + y


def timed_pool(pool, items=100, delay=0.1, verbose=False):
    _x = range(-items/2,items/2,2)
    _y = range(len(_x))
    _d = [delay]*len(_x)

    if verbose: print pool
    import time
    start = time.time()
    res = pool.map(busy_add, _x, _y, _d)
    _t = time.time() - start
    if verbose: print "time to queue:", _t
    start = time.time()
    _sol_ = list(res)
    t_ = time.time() - start
    if verbose: print "time to results:", t_, "\n"
    return _sol_


class BuiltinPool(object):
    def map(self, *args):
        return map(*args)

std = timed_pool(BuiltinPool(), items, delay=0, verbose=False)


def test_serial(source=False):
    from pyina.launchers import SerialMapper as S
    pool = S(source=source)
    res = timed_pool(pool, items, delay, verbose)
    assert res == std

def test_pool(source=False):
    from pyina.launchers import MpiPool as MPI
    pool = MPI(4, source=source)
    res = timed_pool(pool, items, delay, verbose)
    assert res == std

def test_scatter(source=False):
    from pyina.launchers import MpiScatter as MPI
    pool = MPI(4, source=source)
    res = timed_pool(pool, items, delay, verbose)
    assert res == std


if __name__ == '__main__':
    from pyina.mpi import _debug, _save
    #_save(True)
    #_debug(True)

    if verbose:
        print "CONFIG: delay = %s" % delay
        print "CONFIG: items = %s" % items
        print ""

    test_serial()
    test_pool()
    test_scatter()

    test_serial(source=True)
    test_pool(source=True)
    test_scatter(source=True)


# EOF
