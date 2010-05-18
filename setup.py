#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                       Patrick Hung & Mike McKerns, Caltech
#                        (C) 1998-2010  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from distutils.core import setup, Extension
from sys import platform
import os

mpi_incdir = os.environ['MPI_INCDIR']
mpi_libdir = os.environ['MPI_LIBDIR']

if platform[:3] == 'win':
    MPILIBS = []
else: #platform = linux or mac
    MPILIBS = []
    #if platform[:6] == 'darwin':
        #MPILIBS.remove('...')
        #MPILIBS.append('...')

setup(name="pyina",
    version="0.1a1",
    maintainer="Mike McKerns",
    maintainer_email="mmckerns@caltech.edu",
    license="BSD",
    platforms=["any"],
    description="a MPI-based parallel mapper and launcher",
    classifiers=(
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Physics Programming"),

    packages=['pyina','pyina.tools','pyina.applications'],
    package_dir={'pyina':'pyina','pyina.tools':'tools','pyina.applications':'applications'},

    scripts=[])


if __name__=='__main__':
    pass

# End of file
