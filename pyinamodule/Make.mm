PROJECT = pyina
PACKAGE = _pyina
MODULE = _pyina

include std-pythonmodule.def
include local.def

PROJ_CXX_SRCLIB = -lpyrempi -ljournal

PROJ_SRCS = \
    dummy.cc

# End of file

