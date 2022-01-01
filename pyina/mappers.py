#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pyina/blob/master/LICENSE
"""
tiny function wrapper to make ez_map interface for mappers more standard

provides:
 mapper_str = mapper()  interface

(for a the raw map function, use parallel_map directly) 
"""

__all__ = ['worker_pool','scatter_gather']


def worker_pool():
    """use the 'worker pool' strategy; hence one job is allocated to each
worker, and the next new work item is provided when a node completes its work"""
    #from mpi_pool import parallel_map as map
    #return map
    return "mpi_pool"

def scatter_gather():
    """use the 'scatter-gather' strategy; hence split the workload as equally
as possible across all available workers in a single pass"""
    #from mpi_scatter import parallel_map as map
    #return map
    return "mpi_scatter"


# backward compatibility
carddealer_mapper = worker_pool
equalportion_mapper = scatter_gather

def all_mappers():
    import mappers
    L = ["mappers.%s" % f for f in  dir(mappers) if f[-6:] == "mapper"]
    return L


if __name__=='__main__':
    print(all_mappers())

# EOF
