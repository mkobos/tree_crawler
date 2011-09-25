all: build-source-package

build-source-package: clean
	./setup.py sdist

install: clean
	./setup.py install --user

test:
	./bin/run_tests.py

docs-api:
	./bin/make_documentation.sh

clean:
	rm -rf build dist concurrent_tree_crawler.egg-info docs-api tmp
