# -*- Makefile -*-

PROJECT = pyina
PACKAGE = examples_other

PROJ_TIDY += xx.*
PROJ_CLEAN +=

all: export

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

#EXPORT_PYTHON_MODULES = \
EXPORT_BINS = \
    hello.py \
    pypi.py \
    nodes.py \
    test1.py \
    test2.py \
    test_pmap.py \
    test_parallelmap.py \
    log.py \
    mpd_trace.py \
    test_ports.py \
    test_mogi_bcast.py \
#   test_mogi_future.py \


#export:: export-package-python-modules
export:: export-binaries release-binaries



# End of file

