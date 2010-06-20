# -*- Makefile -*-

PROJECT = pyina
PACKAGE = applications

PROJ_TIDY += *.log *.out xx.*
PROJ_CLEAN =

#--------------------------------------------------------------------------
#

#all: export
all: clean

#--------------------------------------------------------------------------
#

EXPORT_BINS = \
    machines_raw.py \
    mpd_trace.py \
    parallel_batch.py \
    parallel_batch_raw.py \

export:: export-binaries release-binaries


# End of file
