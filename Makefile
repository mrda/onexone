NOSE=nosetests
VENV = ./venv
VENV3 = ./venv3

.PHONY: all build-env check-env check develop tests clean 

all:
	@echo "Choose 'make py2' or 'make py3'"
	exit 0

py2: build-env check-env check develop tests

py3: build-env3 check-env check develop tests

build-env: | $(VENV)
	@echo "Found $(VENV)"
	. venv/bin/activate; pip install -Ur requirements.txt

build-env3: | $(VENV3)
	@echo "Found $(VENV3)"
	. venv/bin/activate; pip install -Ur requirements.txt

$(VENV):
	@echo "*** $(VENV) doesn't exist"
	virtualenv venv	

$(VENV3):
	@echo "*** $(VENV3) doesn't exist"
	python3 -m venv venv

check-env:
	@if [ "z$(VIRTUAL_ENV)" = "z" ]; then \
            printf "\nPlease start your virtualenv,\nlike this '. ./venv/bin/activate'\n"; \
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
	rm -rf venv
	find . -iname "*.pyc" -o -iname "*.pyo" -o -iname "*.so" -o -iname "#*#" -delete


