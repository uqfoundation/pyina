# -*- Makefile -*-

PROJECT = pythia
PACKAGE = tools

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

export:: export-binaries release-binaries

# End of file
