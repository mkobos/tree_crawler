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

## Check if the metadata of the package meets minimal requirements to build
## a package. With option `--restructuredtext`, check also if the value of the
## parameter `long_description` of the function `setup` is a valid 
## restructuretext.
check-package-metatada:
	./setup.py check --restructuredtext

upload:
	./setup.py sdist upload --quiet
	./setup.py bdist_egg upload --quiet

clean:
	rm -rf build dist concurrent_tree_crawler.egg-info docs-api tmp MANIFEST
