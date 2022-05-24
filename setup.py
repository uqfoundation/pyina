#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

import os
import sys
# drop support for older python
unsupported = None
if sys.version_info < (2, 7):
    unsupported = 'Versions of Python before 2.7 are not supported'
elif (3, 0) <= sys.version_info < (3, 7):
    unsupported = 'Versions of Python before 3.7 are not supported'
if unsupported:
    raise ValueError(unsupported)

# get distribution meta info
here = os.path.abspath(os.path.dirname(__file__))
meta_fh = open(os.path.join(here, 'pyina/__init__.py'))
try:
    meta = {}
    for line in meta_fh:
        if line.startswith('__version__'):
            VERSION = line.split()[-1].strip("'").strip('"')
            break
    meta['VERSION'] = VERSION
    for line in meta_fh:
        if line.startswith('__author__'):
            AUTHOR = line.split(' = ')[-1].strip().strip("'").strip('"')
            break
    meta['AUTHOR'] = AUTHOR
    LONG_DOC = ""
    DOC_STOP = "FAKE_STOP_12345"
    for line in meta_fh:
        if LONG_DOC:
            if line.startswith(DOC_STOP):
                LONG_DOC = LONG_DOC.strip().strip("'").strip('"').lstrip()
                break
            else:
                LONG_DOC += line
        elif line.startswith('__doc__'):
            DOC_STOP = line.split(' = ')[-1]
            LONG_DOC = "\n"
    meta['LONG_DOC'] = LONG_DOC
finally:
    meta_fh.close()

# get version numbers, long_description, etc
AUTHOR = meta['AUTHOR']
VERSION = meta['VERSION']
LONG_DOC = meta['LONG_DOC'] #FIXME: near-duplicate of README.md
#LICENSE = meta['LICENSE'] #FIXME: duplicate of LICENSE
AUTHOR_EMAIL = 'mmckerns@uqfoundation.org'

# check if setuptools is available
try:
    from setuptools import setup
    from setuptools.dist import Distribution
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    Distribution = object
    has_setuptools = False

# platform-specific instructions
sdkroot_set = False
if sys.platform[:3] == 'win':
    pass
else: #platform = linux or mac
     if sys.platform[:6] == 'darwin':
         # mpi4py has difficulty building on a Mac
         # see special installation instructions here:
         # http://mpi4py.scipy.org/docs/usrman/install.html
         import os
         try:
             sdkroot = os.environ['SDKROOT']
         except KeyError:
             sdkroot = '/'
             os.environ['SDKROOT'] = sdkroot
             sdkroot_set = True
         pass
     pass

# build the 'setup' call
setup_kwds = dict(
    name="pyina",
    version=VERSION,
    description="MPI parallel map and cluster scheduling",
    long_description = LONG_DOC,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    maintainer = AUTHOR,
    maintainer_email = AUTHOR_EMAIL,
    license = '3-clause BSD',
    platforms = ['Linux', 'Mac'],
    url = 'https://github.com/uqfoundation/pyina',
    download_url = 'https://pypi.org/project/pyina/#files',
    project_urls = {
        'Documentation':'http://pyina.rtfd.io',
        'Source Code':'https://github.com/uqfoundation/pyina',
        'Bug Tracker':'https://github.com/uqfoundation/pyina/issues',
    },
    python_requires = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    packages=['pyina','pyina.tests'],
    package_dir={'pyina':'pyina','pyina.tests':'tests'},
    scripts=['scripts/ezpool','scripts/ezscatter','scripts/mpi_world'],
)

# force python-, abi-, and platform-specific naming of bdist_wheel
class BinaryDistribution(Distribution):
    """Distribution which forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True

# define dependencies
sysversion = sys.version_info[:2]
dill_version = 'dill>=0.3.5.1'
pox_version = 'pox>=0.3.1'
pathos_version = 'pathos>=0.2.9'
mystic_version = 'mystic>=0.3.8'
cython_version = 'cython>=0.29.22' #XXX: required to build numpy from source
try:
    import ctypes # if using `pypy`, pythonapi is not found
    IS_PYPY = not hasattr(ctypes, 'pythonapi')
    IS_PYPY2 = IS_PYPY and sysversion < (3,0)
except:
    IS_PYPY = False
    IS_PYPY2 = False
if sysversion < (2,6) or sysversion == (3,0) or sysversion == (3,1):
    numpy_version = 'numpy>=1.0, <1.8.0'
    mpi4py_version = 'mpi4py>=1.3, !=3.0.2' # segfault 11 on MPI import
elif sysversion == (2,6) or sysversion == (3,2) or sysversion == (3,3):
    numpy_version = 'numpy>=1.0, <1.12.0'
    mpi4py_version = 'mpi4py>=1.3, !=3.0.2' # segfault 11 on MPI import
elif IS_PYPY2:
    numpy_version = 'numpy>=1.0, <1.16.0'
    mpi4py_version = 'mpi4py>=1.3, !=3.0.2, <3.1.0' # segfault 11 on MPI import
elif sysversion == (2,7) or sysversion == (3,4):
    numpy_version = 'numpy>=1.0, <1.17.0'
    mpi4py_version = 'mpi4py>=1.3, !=3.0.2' # segfault 11 on MPI import
elif sysversion == (3,5):
    numpy_version = 'numpy>=1.0, <1.19.0'
    mpi4py_version = 'mpi4py>=1.3, !=3.0.2' # segfault 11 on MPI import
elif sysversion == (3,6):# or IS_PYPY
    numpy_version = 'numpy>=1.0, <1.20.0'
    mpi4py_version = 'mpi4py>=1.3, !=3.0.2' # segfault 11 on MPI import
else:
    numpy_version = 'numpy>=1.0'
    mpi4py_version = 'mpi4py>=1.3, !=3.0.2' # segfault 11 on MPI import
# add dependencies
depend = [numpy_version, dill_version, pox_version, pathos_version, mpi4py_version]
extras = {'examples': [mystic_version]}
# rtd fails for mpi4py, so mock it instead
if os.environ.get('READTHEDOCS', None) == 'True': #NOTE: is on_rtd
    depend = depend[:-1]
# update setup kwds
if has_setuptools:
    setup_kwds.update(
        zip_safe=False,
        # distclass=BinaryDistribution,
        install_requires=depend,
        # extras_require=extras,
    )

# call setup
setup(**setup_kwds)

# if dependencies are missing, print a warning
try:
    import numpy
    import dill
    import pox
    import pathos
    import mpi4py #XXX: throws an error even though ok?
    #import cython
    #import mystic
except ImportError:
    print("\n***********************************************************")
    print("WARNING: One of the following dependencies may be unresolved:")
    print("    %s" % numpy_version)
    print("    %s" % dill_version)
    print("    %s" % pox_version)
    print("    %s" % pathos_version)
    print("    %s" % mpi4py_version)
    #print("    %s" % cython_version)
    #print("    %s (optional)" % mystic_version)
    print("***********************************************************\n")

if sdkroot_set:
    print("\n***********************************************************")
    print("WARNING: One of following variables was set to a default:")
    print("    SDKROOT %s" % sdkroot)
    print("***********************************************************\n")
else:
    pass

try:
    import mpi4py
except ImportError:
    print("""
You may need to set the environment variable "SDKROOT",
as shown in the instructions for installing ``mpi4py``:
  http://mpi4py.scipy.org/docs/usrman/install.html
""")


if __name__=='__main__':
    pass

# End of file
