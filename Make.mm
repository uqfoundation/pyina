# -*- Makefile -*-

PROJECT = pyina

BUILD_DIRS = \
    pyina \
    tools \
    applications \

OTHER_DIRS = \
    tests \
    examples \
    examples_other \

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
