#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2024 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE

import os
import sys
# drop support for older python
if sys.version_info < (3, 8):
    unsupported = 'Versions of Python before 3.8 are not supported'
    raise ValueError(unsupported)

# get distribution meta info
here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)
from version import (__version__, __author__, __contact__ as AUTHOR_EMAIL,
                     get_license_text, get_readme_as_rst, write_info_file)
LICENSE = get_license_text(os.path.join(here, 'LICENSE'))
README = get_readme_as_rst(os.path.join(here, 'README.md'))

# write meta info file
write_info_file(here, 'pyina', doc=README, license=LICENSE,
                version=__version__, author=__author__)
del here, get_license_text, get_readme_as_rst, write_info_file

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
    version=__version__,
    description="MPI parallel map and cluster scheduling",
    long_description = README.strip(),
    author = __author__,
    author_email = AUTHOR_EMAIL,
    maintainer = __author__,
    maintainer_email = AUTHOR_EMAIL,
    license = 'BSD-3-Clause',
    platforms = ['Linux', 'Mac'],
    url = 'https://github.com/uqfoundation/pyina',
    download_url = 'https://pypi.org/project/pyina/#files',
    project_urls = {
        'Documentation':'http://pyina.rtfd.io',
        'Source Code':'https://github.com/uqfoundation/pyina',
        'Bug Tracker':'https://github.com/uqfoundation/pyina/issues',
    },
    python_requires = '>=3.8',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    packages=['pyina','pyina.tests'],
    package_dir={'pyina':'pyina','pyina.tests':'pyina/tests'},
    scripts=['scripts/ezpool','scripts/ezscatter','scripts/mpi_world'],
)

# force python-, abi-, and platform-specific naming of bdist_wheel
class BinaryDistribution(Distribution):
    """Distribution which forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True

# define dependencies
dill_version = 'dill>=0.3.8'
pox_version = 'pox>=0.3.4'
pathos_version = 'pathos>=0.3.2'
mystic_version = 'mystic>=0.4.2'
cython_version = 'cython>=0.29.30' #XXX: required to build numpy from source
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
