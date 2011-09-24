#!/usr/bin/env python

"""
This script is responsible for initialization of the crawler to execute 
a task of downloading pages from a sample web site.
"""

from cmdln_multithreaded_crawler import CmdLnMultithreadedCrawler
from html_multipage_navigator.cmdln.navigators_creator import \
	CmdLnNavigatorsCreator
from html_multipage_navigator.cmdln.sample_levels_creator import \
	SampleCmdLnLevelsCreator

navigators_creator = CmdLnNavigatorsCreator(SampleCmdLnLevelsCreator())
crawler = CmdLnMultithreadedCrawler(navigators_creator)
crawler.run()