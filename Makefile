NOSE=nosetests

.PHONY: all tests clean list

tests:
	${NOSE}

clean:
	-find . -name "*.pyc" -o -name "*.pyo" -o -name "*.so" -o -name "#*#" | xargs rm -f

list:
	-find .

devenv:
	-virtualenv venv
	-printf "\n*** Remember to start your venv, like this '. ./venv/bin/activate'\n\n"

develop:
	-python setup.py develop
	-pip install -r requirements.txt

all: tests

