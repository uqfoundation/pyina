pyina
=====
a MPI-based parallel mapper and launcher

About Pyina
-----------
The pyina package provides several basic tools to make MPI-based
high-performance computing more accessable to the end user. The goal
of pyina is to allow the user to extend their own code to MPI-based
high-performance computing with minimal refactoring.

The central element of pyina is the parallel map-reduce algorithm.
Pyina currently provides two strategies for executing the parallel-map,
where a strategy is the algorithm for distributing the work list of
jobs across the availble nodes.  These strategies can be used "in-the-raw"
(i.e. directly) to provide map-reduce to a user's own mpi-aware code.
Further, pyina provides the "ez_map" interface, which is a map-reduce
implementation that hides the MPI internals from the user. With ez_map,
the user can launch their code in parallel batch mode -- using standard
python and without ever having to write a line of parallel python or MPI code.

There are several ways that a user would typically launch their code in
parallel -- directly with "mpirun" or "mpiexec", or through the use of a
scheduler such as torque or slurm. Pyina encapsulates several of these
'launchers', and provides a common interface to the different methods of
launching a MPI job.

Pyina is part of pathos, a python framework for heterogenous computing.
Pyina is in the early development stages, and any user feedback is
highly appreciated. Contact Mike McKerns [mmckerns at caltech dot edu]
with comments, suggestions, and any bugs you may find. A list of known
issues is maintained at http://trac.mystic.cacr.caltech.edu/project/pathos/query.


Major Features
--------------
Pyina provides a highly configurable parallel map-reduce interface
to running MPI jobs, with::
    * a map-reduce interface that extends the python 'map' standard
    * the ability to submit batch jobs to a selection of schedulers
    * the ability to customize node and process launch configurations
    * the ability to launch parallel MPI jobs with standard python
    * ease in selecting different strategies for processing a work list


Current Release
---------------
The latest released version of pyina is available from::
    http://trac.mystic.cacr.caltech.edu/project/pathos

Pyina is distributed under a modified BSD license.

Development Release
-------------------
You can get the latest development release with all the shiny new features at::
    http://dev.danse.us/packages.

or even better, fork us on our github mirror of the svn trunk::
    https://github.com/uqfoundation

Citation
--------
If you use pyina to do research that leads to publication, we ask that you
acknowledge use of pyina by citing the following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    http://trac.mystic.cacr.caltech.edu/project/pathos

More Information
----------------
Probably the best way to get started is to look at a few of the
examples provided within pyina. See `pyina.examples` for a
set of scripts that demonstrate the configuration and launching of
mpi-based parallel jobs using the `ez_map` interface. Also see
`pyina.examples_other` for a set of scripts that test the more raw
internals of pyina. The source code is also generally well documented,
so further questions may be resolved by inspecting the code itself, or through 
browsing the reference manual. For those who like to leap before
they look, you can jump right to the installation instructions. If the aforementioned documents
do not adequately address your needs, please send us feedback.

Pyina is an active research tool. There are a growing number of publications and presentations that
discuss real-world examples and new features of pyina in greater detail than presented in the user's guide. 
If you would like to share how you use pyina in your work, please send us a link.
