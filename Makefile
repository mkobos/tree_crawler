all: build-source-package

build-source-package:
	rm -rf build dist
	./setup.py sdist

install:
	rm -rf build dist
	./setup.py install

clean:
	rm -rf dist
