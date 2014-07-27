#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

# construct a target function
def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

def test_equal():
    # get the parallel mapper
    from pyina.ez_map import ez_map
    from pyina.ez_map import ez_map2

    # launch the parallel map of the target function
    results = ez_map(host, range(10), nodes=4)
    results2 = ez_map2(host, range(10), nodes=4)
    assert "\n".join(results) == "\n".join(results2)


if __name__ == '__main__':
    test_equal()


# EOF
