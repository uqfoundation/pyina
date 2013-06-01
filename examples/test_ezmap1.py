#!/usr/bin/env python

from pyina.launchers import MpiScatter

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())

print "Evaluate 10 items on 1 node (w/ 1 ppn) using scatter-gather:"
scat = MpiScatter('1:ppn=1')
res1 = scat.map(host, range(10)) 
print scat
print '\n'.join(res1)
print ''

print "Evaluate 10 items on 1 node (w/ 2 ppn) using scatter-gather:"
scat.nodes = '1:ppn=2'
res2 = scat.map(host, range(10)) 
print scat
print '\n'.join(res2)
print ''

# end of file
