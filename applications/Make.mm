# -*- Makefile -*-

PROJECT = pyina
PACKAGE = applications

PROJ_TIDY += *.log *.out xx.*
PROJ_CLEAN =

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
#

EXPORT_BINS = \
    parallel_batch_raw.py \
    parallel_batch.py \
    machines_raw.py \
    machines.py \
    mpiversion.py \
    mpi_world.py \
    mpd_trace.py \

export:: export-binaries release-binaries


# version
# $Id: Make.mm,v 1.4 2007/08/06 06:17:22 patrickh Exp $

# End of file
