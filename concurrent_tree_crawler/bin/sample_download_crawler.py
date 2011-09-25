#!/usr/bin/env python

"""
This script initializes the crawler to downloade pages from a sample web site.
"""

def set_path_to_package_root():
	"""
	Calling this function esures that: 1) if this script is placed inside
	the C{concurrent_tree_crawler} package files, when importing the 
	C{concurrent_tree_crawler} package it uses these package files, 
	2) otherwise, in situtation when the script is in some other place and
	we want to use the library C{concurrent_tree_crawler} installed in the
	system, it uses this library when importing the C{concurrent_tree_crawler}.
	"""
	import sys
	import os.path
	sys.path[0]=os.path.join(sys.path[0], '../..')
set_path_to_package_root()

from concurrent_tree_crawler.cmdln_multithreaded_crawler import \
	CmdLnMultithreadedCrawler
from concurrent_tree_crawler.html_multipage_navigator.cmdln.navigators_creator \
	import CmdLnNavigatorsCreator
from concurrent_tree_crawler.html_multipage_navigator.cmdln.sample_levels_creator \
	import SampleCmdLnLevelsCreator

navigators_creator = CmdLnNavigatorsCreator(SampleCmdLnLevelsCreator())
crawler = CmdLnMultithreadedCrawler(navigators_creator)
crawler.run()
