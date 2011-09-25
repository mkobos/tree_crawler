About
=====
This project is a Python library which implements a generic concurrent tree-crawling algorithm. In practice, it can be used in tasks that require a couple of crawling threads to explore a tree-like structure e.g. when downloading documents from a hierarchical web site.

Although the main application domain for this library is using it to crawl a web site with known tree-like structure, one of its main design goals was flexibility in adjusting it to different application areas. The library was consciously developed to be useful in the following 3 cases. These cases are listed here from the least to the most general (and from the one requiring the least implementation effort from the user of the library to the one requiring the most of it).

**Main use-cases of the library**:

1. Crawling HTML web site with known and fixed tree-like structure. In this approach, the number of tree levels is fixed and each page on a certain tree level has basically the same structure (i.e. it is parsed by the same parser). On each level, the links to the pages of the lower level are not necessarily placed on one page, but can be distributed among many pages. See a sample testing web site [concurrent_tree_crawler/test/data/original_site/issues_1.html][] for an example of such a site.
2. Crawling some other HTML web site with a tree-like structure.
3. Crawling some other tree-like structure.

For a more detailed information about creating one's own crawler using this library see [http://github.com/mkobos/tree_crawler/wiki][].

[concurrent_tree_crawler/test/data/original_site/issues_1.html]: concurrent_tree_crawler/test/data/original_site/issues_1.html
[http://github.com/mkobos/tree_crawler/wiki]: http://github.com/mkobos/tree_crawler/wiki

Application features
--------------------
- Generic features of the library:
	- **Resistance to abnormal program termination** (e.g. due to computer shutdown). The information about the part of the tree that has been already visited is saved in a file and restored at the next program start. This way e.g. the leaf nodes that have been already explored are not explored again.
	- **Consistent dealing with navigation problems**. When a navigation problem occurs in a certain thread while exploring the tree (in case of a web site it might be e.g. a dead link or a malformed web page), the thread's browser is restarted and the node of the tree that caused the problem is marked as erroneous. For technical details, see the description of the [AbstractTreeNavigator][] class.
	- **Daily schedule of program activity**. The user can enter a daily time interval during which the program will be actively crawling the tree; the program will sleep during the rest of the time.
	- **Logging program activity**. The user can choose between 3 levels of details of logging messages. The logging messages are printed to the standard output but their copy can be also saved in a file.
	- **Handling same node name problem**. Some children of the same parent might have the same name. In case of web crawling, this might happen when the name of the node is based on a name of a link pointing to a web page corresponding to this node, and the there are many links with the same name. This is not desirable, because we assume that every child of a certain parent has different name. This assumption simplifies e.g. web crawling task when for each node we create a directory or a file with the name which is the same as the node name (and of course there cannot be two files with the same name in a single directory). To solve this problem, whenever it seems that a certain tree node has two or more children of the same name, the consecutive children are renamed according to the pattern: `NAME-repetition_1`, `NAME-repetition_2` and so on.
- Web site crawler-related features:
	- **Throttling the download speed**. The user can set a maximal number of web pages to be visited by the crawler.
	- **Handling many linked web pages corresponding to a single tree node**. A part of the library (class [HTMLMultipageNavigator][]) explicitly handles situation when there are many pages corresponding to a single tree node. See a sample testing web site [concurrent_tree_crawler/test/data/original_site/issues_1.html][] for an example of such a site.
	- **Handling the same web page -- different address problem**. Some web sites might be constructed so that the same web page might have a different address when viewed through browsers belonging to two different threads. It might be the case e.g. when each thread has to log in on the web site as a different user and the user name is appended to the address of each web page. As long as the user or the library can give the same name to those pages (see [AbstractPageAnalyzer.get_links()][] function and [PageLinks][] class for technical details), they are regarded by the library as the same page. This is usually pretty simple since the name of the link to the web page is the same even if the addresses differ.

[AbstractTreeNavigator]: concurrent_tree_crawler/abstract_tree_navigator.py
[HTMLMultipageNavigator]: concurrent_tree_crawler/html_multipage_navigator/tree_navigator.py
[AbstractPageAnalyzer.get_links()]: concurrent_tree_crawler/html_multipage_navigator/abstract_page_analyzer.py
[PageLinks]: concurrent_tree_crawler/html_multipage_navigator/abstract_page_analyzer.py

Concurrent tree crawling algorithm
----------------------------------
We use a set number of threads to concurrently explore a generic tree (we do not care at the moment whether it corresponds to a web site or not). The threads start their exploration of the nodes from the tree's root. Each thread tries to explore tree nodes which have not yet been explored by other threads (we use a modification of the breadth-search algorithm to minimize the number of situations when the threads get into each other's way).

In the case of web site crawling, it means that each thread has its own browser but tries not to open (and parse) web pages which have already been opened by other threads.

For a more detailed information about the generic algorithm see [http://github.com/mkobos/tree_crawler/wiki][].

Requirements
============
The program uses the following python packages:

- `nose`
- `mechanize`

Project files and directory structure
=====================================
- Use `run_test.py` script to run the unit tests. Unit tests related to a certain source file are placed inside a `test` directory which is placed in the same directory as the source file. This convention was introduced because we want the tests to be placed close to the source files but at the same time we want them not to pollute the source files directory.
- Use `make_documentation.sh` to generate API documentation from the source
- Use `run_sample_crawler.sh` to run a sample crawler that downloads files from a local web site to a temporary directory

The main directory contains some configuration files for Eclipse and its PyDev plugin which are used to develop the project.
