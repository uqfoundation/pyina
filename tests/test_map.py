# ...

def busy_add(x,y, delay):
    for n in range(x):
       x += n
    for n in range(y):
       y -= n
    import time
    time.sleep(delay)
    return x + y

if __name__ == '__main__':
    import time
    delay = 0.1
    items = 100
    print "CONFIG: delay = %s" % delay
    print "CONFIG: items = %s" % items
    print ""

    _x = range(-items/2,items/2,2)
    _y = range(len(_x))
    _d = [delay]*len(_x)

    print map
    start = time.time()
    res = map(busy_add, _x, _y, _d)
    print "time to queue:", time.time() - start
    start = time.time()
    _basic = list(res)
    print "time to results:", time.time() - start
    print ""

    from pyina.mpi import _debug, _save
    #_save(True)
    #_debug(True)
    from pyina.launchers import SerialMapper as S
    no_pool = S()#source=True)
    print no_pool
    start = time.time()
    res = no_pool.map(busy_add, _x, _y, _d)
    print "time to queue:", time.time() - start
    start = time.time()
    _no_pool = list(res)
    print "time to results:", time.time() - start

    assert _basic == _no_pool
    print ""

    from pyina.launchers import MpiPool as MPI
    mpi_pool = MPI(4)#source=True)
    print mpi_pool
    start = time.time()
    res = mpi_pool.map(busy_add, _x, _y, _d)
    print "time to queue:", time.time() - start
    start = time.time()
    _mpi_pool = list(res)
    print "time to results:", time.time() - start

    assert _basic == _mpi_pool
    print ""

    from pyina.launchers import MpiScatter as MPI
    mpi_pool = MPI(4)#source=True)
    print mpi_pool
    start = time.time()
    res = mpi_pool.map(busy_add, _x, _y, _d)
    print "time to queue:", time.time() - start
    start = time.time()
    _mpi_pool = list(res)
    print "time to results:", time.time() - start

    assert _basic == _mpi_pool

# EOF
