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
VENV3 = ./venv3
GUESS_PY=$(shell ./scripts/guess-python.sh)

.PHONY: all build-env build-env3 check-env check-env3 check develop tests \
       	clean python

# Autodetect which version of python we have available, and use that
# with a preference of python3
all:

ifeq ($(GUESS_PY),python3)
all: py3
endif

ifeq ($(GUESS_PY),python2)
all: py2
endif

ifeq ($(GUESS_PY),none)
all:
	@printf "*** No python found. Exiting...\n"; \
	exit 1;
endif

py2: build-env check-env check develop tests

py3: build-env3 check-env3 check develop tests

python:
	@echo "You're using: "
	@python --version

build-env: | $(VENV)
	@echo "You are using python2"
	. $(VENV)/bin/activate; pip install -Ur requirements.txt

build-env3: | $(VENV3)
	@echo "You are using python3"
	. $(VENV3)/bin/activate; pip install -Ur requirements.txt

$(VENV):
	@echo "*** $(VENV) doesn't exist"
	virtualenv $(VENV)

$(VENV3):
	@echo "*** $(VENV3) doesn't exist"
	python3 -m venv $(VENV3)

check-env:
	@if [ "z$(VIRTUAL_ENV)" = "z" ]; then \
            printf "\nPlease start your virtualenv,\nlike this "; \
            printf "'. $(VENV)/bin/activate'\n"; \
            printf "Then enter your 'make' command again\n\n"; \
            exit 1; \
        else true; fi

check-env3:
	@if [ "z$(VIRTUAL_ENV)" = "z" ]; then \
            printf "\nPlease start your virtualenv,\nlike this "; \
            printf "'. $(VENV3)/bin/activate'\n"; \
            printf "Then enter your 'make' command again\n\n"; \
            exit 1; \
        else true; fi

check: check-env
	-pycodestyle onexone/*.py
	-pycodestyle tests/*.py

develop: check-env
	python setup.py develop

tests: check-env
	${NOSE} -s

clean:
	rm -rf $(VENV) $(VENV3)
	find . -iname "*.pyc" -o -iname "*.pyo" -o -iname "*.so" \
	       	-o -iname "#*#" -delete
