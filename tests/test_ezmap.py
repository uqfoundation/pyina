#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

# old-style maps (deprecated)

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
    time.sleep(2*random.random())
    return x*x

def squared(x):
    return x*x

def quad_factory(a=1, b=1, c=0):
    def quad(x):
        return a*x**2 + b*x + c
    return quad

square_plus_one = quad_factory(2,0,1)


def test1(_map, nodes):
    print _map
    print "x: %s\n" % str(x)
    _config = {'type':"blocking", 'threads':False, 'nproc':nodes, 'ncpus':nodes}
    mapconfig = {'nodes':nodes}

    print type, _map.__name__
    start = time.time()
    res = _map(squared, x, **mapconfig)
    print "time to results:", time.time() - start
    print "y: %s\n" % str(res)
    mapconfig.update(_config)
    _res = _map(squared, x, **mapconfig)
    assert _res == res
    mapconfig.update({'program':'hostname','workdir':'.','file':''})
    _res = _map(squared, x, **mapconfig)
    assert _res == res
    from pyina.mappers import worker_pool
    mapconfig.update({'mapper':worker_pool,'timelimit':'00:00:02'})
    _res = _map(squared, x, **mapconfig)
    assert _res == res


def test2(_map, nodes, items=4, delay=0 ):
    _x = range(-items/2,items/2,2)
    _y = range(len(_x))
    _d = [delay]*len(_x)

    print map
    res1 = map(busy_squared, _x)
    mapconfig = {'nodes':nodes}

    print _map
    _res1 = _map(busy_squared, _x, **mapconfig)
    assert _res1 == res1

    res2 = map(busy_add, _x, _y, _d)
    _res2 = _map(busy_add, _x, _y, _d, **mapconfig)
    assert _res2 == res2
    print ""


if __name__ == '__main__':
    import time
    x = range(18)
    items = 20
    maxtries = 20

   ### can handle multiple variables
    from pyina.ez_map import ez_map as _map
   #from pyina.ez_map import ez_map2 as _map

    nodes=4
    test1( _map, nodes )
    test2( _map, nodes, items=items )


# EOF
