NOSE=nosetests
VENV = ./venv

.PHONY: all build-env check-env check develop tests clean 

all: build-env check-env check develop tests

build-env: | $(VENV)
	@echo "--- Found $(VENV)"
	. venv/bin/activate; pip install -Ur requirements.txt

$(VENV):
	@echo "*** $(VENV) doesn't exist"
	virtualenv venv	

check-env:
	@if [ "z$(VIRTUAL_ENV)" = "z" ]; then \
            printf "***\n*** Remember to start your virtualenv,\n*** like this '. ./venv/bin/activate'\n***\n"; \
            exit 2; \
        else true; fi

check: check-env
	-pycodestyle onexone/*.py

develop: check-env
	python setup.py develop

tests: check-env
	${NOSE} -s

clean:
	rm -rf venv
	find . -iname "*.pyc" -o -iname "*.pyo" -o -iname "*.so" -o -iname "#*#" -delete


