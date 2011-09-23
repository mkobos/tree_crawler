#!/usr/bin/env python

"""
This script is responsible for initialization of the crawler for a task of
downloading pages from a sample web site.
"""

from crawler.cmdln_multithreaded_crawler import CmdLnMultithreadedCrawler
from crawler.html_multipage_navigator.cmdln.navigators_creator import \
	CmdLnNavigatorsCreator
from crawler.html_multipage_navigator.cmdln.sample_levels_creator import \
	SampleCmdLnLevelsCreator

navigators_creator = CmdLnNavigatorsCreator(SampleCmdLnLevelsCreator())
crawler = CmdLnMultithreadedCrawler(navigators_creator)
crawler.run()