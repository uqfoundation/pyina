# -*- Makefile -*-

PROJECT = pyina
PACKAGE = pyina

BUILD_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py \
    const.py \
    mpiconsts.py \
    parallel_map.py \
    parallel_map2.py \
    ez_map.py \
    launchers.py \
    mappers.py \
    tools.py \


export:: export-python-modules
#export:: export-package-python-modules

# End of file
