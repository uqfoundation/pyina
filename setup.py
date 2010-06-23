#!/usr/bin/env python
#
# Michael McKerns
# mmckerns@caltech.edu

# check if easy_install is available
try:
#   import __force_distutils__ #XXX: uncomment to force use of distutills
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# platform-specific instructions
from sys import platform
if platform[:3] == 'win':
    pass
else: #platform = linux or mac
     if platform[:6] == 'darwin':
         # mpi4py has difficulty building on a Mac
         # see special installation instructions here:
         # http://mpi4py.scipy.org/docs/usrman/install.html
         pass
     pass

# build the 'setup' call
setup_code = """
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

    packages=['pyina'],
    package_dir={'pyina':'pyina'},
"""

# add dependencies
dill_version = '>=0.1a1'
mpi4py_version = '>=1.2.1'
pypar_version = '>=2.1.4'
mystic_version = '>=0.2a1'
if has_setuptools:
    setup_code += """
        zip_safe = False,
        install_requires = ('mpi4py%s','dill%s'),
""" % (mpi4py_version, dill_version)

# add the scripts, and close 'setup' call
setup_code += """
    scripts=['scripts/ezrun.py','scripts/ezrun2.py',
             'scripts/machines.py','scripts/mpi_world.py'])
"""

# exec the 'setup' code
exec setup_code

# if dependencies are missing, print a warning
try:
    import dill
    import mpi4py
    #import pypar
except ImportError:
    print "\n***********************************************************"
    print "WARNING: One of the following dependencies is unresolved:"
    print "    dill %s" % dill_version
    print "    mpi4py %s" % mpi4py_version
#   print "    pypar %s (optional)" % pypar_version
    print "***********************************************************\n"

try:
    import mpi4py
except ImportError:
    print """
For special instructions on installing '%s', please see:
  http://mpi4py.scipy.org/docs/usrman/install.html
""" % 'mpi4py'


if __name__=='__main__':
    pass

# End of file
