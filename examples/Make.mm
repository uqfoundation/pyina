# -*- Makefile -*-

PROJECT = pyina
PACKAGE = examples

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
    test_ezmap.py \
    test_ezmap1.py \
    test_ezmap2.py \
    test_ezmap3.py \
    test_ezmap4.py \
    test_ezmap5.py \
    test_ezmap6.py \
    test_ezmap7.py \


#export:: export-package-python-modules
export:: export-binaries release-binaries



# End of file

