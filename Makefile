all: build-source-package

build-source-package: clean
	./setup.py sdist

install: clean
	./setup.py install

clean:
	rm -rf build dist concurrent_tree_crawler.egg-info
