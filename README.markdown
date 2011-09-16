About
=====
This project is a Python implementation of a generic concurrent tree-crawling algorithm. In practice, it can be used in task that requires couple of crawling threads to explore a tree-like structure e.g. when downloading documents from a hierarchical web site.

One of the main design goals of the program is flexibility of adjusting it to different application areas.

Project files and directory structure
=====================================
- Use `run_test.py` script to run the unit tests. Unit tests related to a certain source file are placed inside `test` directory which is placed in the same directory as the source file. This convention was introduced because we want the tests to be placed close to the source files but at the same time we want them to not pollute the source files directory.
- Use `make_documentation.sh` to generate API documentation from the source
- Use `run_sample_crawler.sh` to run a sample crawler that downloads files from a local web site to a temporary directory

The directory contains some configuration files for Eclipse and its PyDev plugin which are used to develop the project.
