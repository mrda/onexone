#
# onexone top-level Makefile
#
# Copyright (C) 2018 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

NOSE=nosetests
VENV = ./venv
GUESS_PY=$(shell ./scripts/guess-python.sh)

.PHONY: all build-env check-env check develop tests clean python

all: build-env check-env check develop tests

# Building the environment is dependent upon which verson of python
# we'll use.  We prefer python3 if it is available
$(VENV):

ifeq ($(GUESS_PY),python3)
$(VENV):
	@echo "You are using python3"
	@echo "*** $(VENV) doesn't exist"
	python3 -m venv $(VENV)
endif

ifeq ($(GUESS_PY),python2)
$(VENV):
	@echo "You are using python2"
	@echo "*** $(VENV) doesn't exist"
	virtualenv $(VENV)
all: py2
endif

ifeq ($(GUESS_PY),none)
$(VENV):
	@printf "*** No python found. Exiting...\n"; \
	exit 1;
endif

python:
	@echo "You're using: "
	@python --version

build-env: | $(VENV)
	. $(VENV)/bin/activate; pip install -Ur requirements.txt

check-env:
	@if [ "z$(VIRTUAL_ENV)" = "z" ]; then \
            printf "\nPlease start your virtualenv,\nlike this "; \
            printf "'. $(VENV)/bin/activate'\n"; \
            printf "Then enter your 'make' command again\n\n"; \
            exit 1; \
        else true; fi

check: check-env
	-pycodestyle --show-source onexone tests

develop: check-env
	python setup.py develop

tests: check-env
	${NOSE} -s --with-coverage --cover-branches --cover-erase --cover-html --cover-package=onexone

clean:
	rm -rf $(VENV)
	find . -iname "*.pyc" -o -iname "*.pyo" -o -iname "*.so" \
	       	-o -iname "#*#" -delete
