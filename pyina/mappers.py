#!/usr/bin/env python
#
# mmckerns@caltech.edu
#
doc = """
tiny function wrapper to make ez_map interface for mappers more standard

provides:
 mapper_str = mapper()  interface

(for a the raw map function, use parallel_map directly) 
"""


def carddealer_mapper():
    """deal work out to all available resources,
then deal out the next new work item when a node completes its work """
    #from parallel_map import parallel_map as map
    #return map
    return "parallel_map"


def equalportion_mapper():
    """split workload up equally across all available resources """
    #from parallel_map2 import parallel_map as map
    #return map
    return "parallel_map2"


def all_mappers():
    import mappers
    L = ["mappers.%s" % f for f in  dir(mappers) if f[-6:] == "mapper"]
    return L


if __name__=='__main__':
    print all_mappers()

# EOF
