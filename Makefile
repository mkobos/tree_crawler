all: build-source-package

build-source-package: clean
	./setup.py sdist

install: clean
	./setup.py install --user

uninstall:
	pip uninstall concurrent_tree_crawler

test:
	./utils/run_tests.py

docs-api:
	./utils/make_documentation.sh

upload:
	./setup.py sdist upload --quiet
	./setup.py bdist_egg upload --quiet

clean:
	rm -rf build dist concurrent_tree_crawler.egg-info docs-api tmp MANIFEST
