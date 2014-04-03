#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

if __name__ == '__main__':
    # get the parallel mapper
   #from pyina.ez_map import ez_map
    from pyina.ez_map import ez_map2 as ez_map

    # construct a target function
    def host(id):
        import socket
        return "Rank: %d -- %s" % (id, socket.gethostname())

    # launch the parallel map of the target function
    results = ez_map(host, range(10), nodes=4)
    print "\n".join(results)

    # print launch command for all launchers
    from pyina.launchers import all_launches
    print "\n", all_launches()


# EOF
