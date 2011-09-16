#!/usr/bin/env python

"""
This script is responsible for initialization of the crawler for a task of
downloading pages from a sample web site.
"""

from sample_download_crawler import CmdLnMultithreadedCrawler
from crawler.html_multipage_navigator.cmdln_prog.navigators_creator import \
	CmdLnNavigatorsCreator

navigators_creator = CmdLnNavigatorsCreator()
crawler = CmdLnMultithreadedCrawler(navigators_creator)
crawler.run()