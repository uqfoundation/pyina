# -*- Makefile -*-

PROJECT = pyina

BUILD_DIRS = \
    pyina \
    scripts \

OTHER_DIRS = \
    tests \
    examples \
    examples_other \
    applications \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

all: 
	$(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


# End of file
