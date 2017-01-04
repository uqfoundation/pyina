#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

from __future__ import with_statement
from time import sleep
from itertools import izip


PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False

    import math
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def sleep_add1(x):
    if x < 4: sleep(x/10.0)
    return x+1

def sleep_add2(x):
    if x < 4: sleep(x/10.0)
    return x+2

def test_with_multipool(Pool): #XXX: amap and imap -- NotImplementedError
   #inputs = range(10)
   #with Pool() as pool1:
   #    res1 = pool1.amap(sleep_add1, inputs)
   #with Pool() as pool2:
   #    res2 = pool2.amap(sleep_add2, inputs)

    with Pool() as pool3:
       #for number, prime in izip(PRIMES, pool3.imap(is_prime, PRIMES)):
        for number, prime in izip(PRIMES, pool3.map(is_prime, PRIMES)):
            assert prime if number != PRIMES[-1] else not prime
           #print ('%d is prime: %s' % (number, prime))

   #assert res1.get() == [i+1 for i in inputs]
   #assert res2.get() == [i+2 for i in inputs]


if __name__ == '__main__':
    from pyina.launchers import MpiPool
    test_with_multipool(MpiPool)


# EOF
