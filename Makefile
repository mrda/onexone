NOSE=nosetests

.PHONY: all tests clean list

tests:
	${NOSE}

clean:
	-find . -name "*.pyc" -o -name "*.pyo" -o -name "*.so" -o -name "#*#" | xargs rm -f

list:
	-find .

all: tests

