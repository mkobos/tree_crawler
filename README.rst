About
=====

This project is a Python library which implements a generic concurrent tree-crawling algorithm. In practice, it can be used in tasks that require a couple of crawling threads to explore a tree-like structure e.g. when downloading documents from a hierarchical web site.

This document contains a quite high-level description of the library. Apart from it, there are some documents placed on `http://github.com/mkobos/tree\_crawler/wiki <http://github.com/mkobos/tree_crawler/wiki>`_ which deal with some more detailed issues:

- design of the library and creating one's own crawler using the library,
- description of the concurrent tree crawling algorithm.

Main use-cases of the library
-----------------------------

Although the main application domain for this library is using it to crawl a web site with known tree-like structure, one of its main design goals was flexibility in adjusting it to different application areas. The library was consciously developed to be useful in the following 3 cases. These cases are listed here from the least to the most general (and from the one requiring the least implementation effort from the user of the library to the one requiring the most of it).

1. Crawling HTML web site with known and fixed tree-like structure. In this approach, the number of tree levels is fixed and each page on a certain tree level has basically the same structure (i.e. it is parsed by the same parser). On each level, the links to the pages of the lower level are not necessarily placed on one page, but can be distributed among many pages. See a sample testing web site ``concurrent_tree_crawler/test/data/original_site/issues_1.html`` for an example of such a site.
2. Crawling some other HTML web site with a tree-like structure.
3. Crawling some other tree-like structure.

Library features
================


-  Generic features of the library:
   
   -  **Resistance to abnormal program termination** (e.g. due to computer shutdown). The information about the part of the tree that has been already visited is saved in a file and restored at the next program start. This way e.g. the leaf nodes that have been already explored are not explored again.
   -  **Consistent dealing with navigation problems**. When a navigation problem occurs in a certain thread while exploring the tree (in case of a web site it might be e.g. a dead link or a malformed web page), the thread's browser is restarted and the node of the tree that caused the problem is marked as erroneous. For technical details, see the description of the ``AbstractTreeNavigator`` class.
   -  **Daily schedule of program activity**. The user can enter a daily time interval during which the program will be actively crawling the tree; the program will sleep during the rest of the time.
   -  **Logging program activity**. The user can choose between 3 levels of details of logging messages. The logging messages are printed to the standard output but their copy can be also saved in a file.
   -  **Handling same node name problem**. Some children of the same parent might have the same name. In case of web crawling, this might happen when the name of the node is based on a name of a link pointing to a web page corresponding to this node, and the there are many links with the same name. This is not desirable, because we assume that every child of a certain parent has different name. This assumption simplifies e.g. web crawling task when for each node we create a directory or a file with the name which is the same as the node name (and of course there cannot be two files with the same name in a single directory). To solve this problem, whenever it seems that a certain tree node has two or more children of the same name, the consecutive children are renamed according to the pattern: ``NAME-repetition_1``, ``NAME-repetition_2`` and so on.

-  Web site crawler-related features:
   
   -  **Throttling the download speed**. The user can set a maximal number of web pages to be visited by the crawler.
   -  **Handling many linked web pages corresponding to a single tree node**. A part of the library (class ``HTMLMultipageNavigator``) explicitly handles situation when there are many pages corresponding to a single tree node. See a sample testing web site ``concurrent_tree_crawler/test/data/original_site/issues_1.html`` for an example of such a site.
   -  **Handling the same web page -- different address problem**. Some web sites might be constructed so that the same web page might have a different address when viewed through browsers belonging to two different threads. It might be the case e.g. when each thread has to log in on the web site as a different user and the user name is appended to the address of each web page. As long as the user or the library can give the same name to those pages (see ``AbstractPageAnalyzer.get_links()`` function and ``PageLinks`` class for technical details), they are regarded by the library as the same page. This is usually pretty simple since the name of the link to the web page is the same even if the addresses differ.


How to use the library
======================

We will show how to run an example script that uses the library. The script uses a couple of threads to download the data from a sample local web page into a temporary directory. There are two main ways to obtain the script and to execute it.


1. Using the source from the repository. Steps:
   
   1. Download the source of the package from the repository (``git clone http://github.com/mkobos/tree_crawler``)
   2. In the source's root directory, run the script ``concurrent_tree_crawler/bin/run_sample_download_crawler.py``

2. Using the installed library. Steps:
   
   1. Install the ``concurrent_tree_crawler`` library in your system from the PyPi packages repository (e.g. by executing ``pip install --user concurrent_tree_crawler`` or ``easy_install --user concurrent_tree_crawler``)
   2. Download the `concurrent_tree_crawler/bin/run_sample_download_crawler.py <http://raw.github.com/mkobos/tree_crawler/master/concurrent_tree_crawler/bin/run_sample_download_crawler.py>`_ and `concurrent_tree_crawler/bin/sample_download_crawler.py <http://raw.github.com/mkobos/tree_crawler/master/concurrent_tree_crawler/bin/sample_download_crawler.py>`_ scripts from the source repository, place them in a single directory and run the ``run_sample_download_crawler.py`` script (but before that, make the scripts executable if needed).


For a more detailed information about creating one's own crawler using this library see `http://github.com/mkobos/tree\_crawler/wiki <http://github.com/mkobos/tree_crawler/wiki>`_.

Concurrent tree crawling algorithm
==================================

We use a set number of threads to concurrently explore a generic tree (we do not care at the moment whether it corresponds to a web site or not). The threads start their exploration of the nodes from the tree's root. Each thread tries to explore tree nodes which have not yet been explored by other threads (we use a modification of the breadth-search algorithm to minimize the number of situations when the threads get into each other's way).

In the case of web site crawling, it means that each thread has its own browser but tries not to open (and parse) web pages which have already been opened by other threads.

For a more detailed information about the generic algorithm see `http://github.com/mkobos/tree\_crawler/wiki <http://github.com/mkobos/tree_crawler/wiki>`_.

Project files and directory structure
=====================================


-  ``Makefile`` -- The makefile used for managing different tasks related to the source code.
-  ``utils/run_tests.py`` script runs the unit tests (or alternatively: ``make test`` or ``./setup.py test``) . Unit tests related to a certain source file are placed inside a ``test`` directory which is placed in the same directory as the source file. This convention was introduced because we want the tests to be placed close to the source files but at the same time we want them not to pollute the source files directory.
-  ``utils/make_documentation.sh`` script generates API documentation from the source (or alternatively: ``make docs-api``)
-  ``concurrent_tree_crawler/bin/run_sample_download_crawler.py`` script runs a sample crawler that downloads files from a local web site into a temporary directory

The main directory contains also some configuration files for Eclipse and its PyDev plugin which are used to develop the project.


