# -*- Makefile -*-

PROJECT = pyina
PACKAGE = scripts

PROJ_TIDY += *.log *.out xx.*
PROJ_CLEAN =

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
#

EXPORT_BINS = \
    ezrun.py \
    ezrun2.py \
    machines.py \
    mpi_world.py \

export:: export-binaries release-binaries

# End of file
