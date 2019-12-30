#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2020 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

# old-style maps (deprecated)

import time

x = range(18)
delay = 0.01
items = 20


def busy_add(x,y, delay=0.01):
    for n in range(x):
       x += n
    for n in range(y):
       y -= n
    import time
    time.sleep(delay)
    return x + y

def busy_squared(x):
    import time, random
    time.sleep(0.01*random.random())
    return x*x

def squared(x):
    return x*x

def quad_factory(a=1, b=1, c=0):
    def quad(x):
        return a*x**2 + b*x + c
    return quad

square_plus_one = quad_factory(2,0,1)

x2 = list(map(squared, x))


def check_sanity(_map, nodes, verbose=False):
    if verbose:
        print(_map)
        print(("x: %s\n" % str(x)))

        print((type, _map.__name__))
    _config = {'type':"blocking", 'threads':False, 'nproc':nodes, 'ncpus':nodes}
    mapconfig = {'nodes':nodes}
    start = time.time()
    res = _map(squared, x, **mapconfig)
    end = time.time() - start
    if verbose:
        print(( "time to results:", end))
        print(( "y: %s\n" % str(res)))
    assert res == x2

    mapconfig.update(_config)
    res = _map(squared, x, **mapconfig)
    assert res == x2

    mapconfig.update({'program':'hostname','workdir':'.','file':''})
    res = _map(squared, x, **mapconfig)
    assert res == x2

    from pyina.mappers import worker_pool
    mapconfig.update({'mapper':worker_pool,'timelimit':'00:00:02'})
    res = _map(squared, x, **mapconfig)
    assert res == x2


def check_maps(_map, nodes, items=4, delay=0 ):
    _x = range(int(-items/2), int(items/2),2)
    _y = range(len(_x))
    _d = [delay]*len(_x)
    _z = [0]*len(_x)

   #print map
    res1 = list(map(busy_squared, _x))
    mapconfig = {'nodes':nodes}

   #print _map
    _res1 = _map(busy_squared, _x, **mapconfig)
    assert _res1 == res1

    res2 = list(map(busy_add, _x, _y, _d))
    _res2 = _map(busy_add, _x, _y, _d, **mapconfig)
    assert _res2 == res2
   #print ""


def test_ezmap():
    from pyina.ez_map import ez_map as _map
    nodes=4
    check_sanity( _map, nodes )
    check_maps( _map, nodes, items=items )

def test_ezmap2():
    from pyina.ez_map import ez_map2 as _map
    nodes=4
    check_sanity( _map, nodes )
    check_maps( _map, nodes, items=items )


if __name__ == '__main__':
    test_ezmap()
    test_ezmap2()
