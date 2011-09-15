#!/usr/bin/env python

"""
This script is responsible for initialization and of the crawler for a task of
downloading a sample web page. It also handles user command-line interface
of the program.
"""

import logging
import datetime
from optparse import OptionParser
import os.path

from common.file_helper import lenient_makedir
from crawler.standard_node import StandardNode
from crawler.html_multipage_navigator.sample_page_analyzer import LevelsCreator
from crawler.html_multipage_navigator.tree_navigator import \
	HTMLMultipageNavigator
from crawler.html_multipage_navigator.web_browser import MechanizeBrowserCreator
from crawler.html_multipage_navigator.throttled_web_browser import \
	ThrottledWebBrowserCreator
from crawler.abstract_node import NodeState
from crawler.crawler_program import MultithreadedCrawler
from common.threads.token_bucket import TokenBucketFiller, StandardTokenBucket
from common.activity_schedule import DaySchedule, AlwaysActiveSchedule

__default_threads_no_string = '2'
__save_period = 0.1

def parse():
	usage="usage: %prog [-t DOWNLOAD_THREADS_NO] [-l LOG_FILE] "\
		"[--verbose] [--very_verbose] "\
		"[--pages_per_second_download_limit NUMBER] "\
		"[--daily_schedule START_TIME-END_TIME] "\
		"SOURCE_ADDRESS DESTINATION_DIR STATE_FILE"
	parser=OptionParser(usage=usage)
	parser.add_option('-t', '--threads', dest='threads_no', type='int',
		action='store', default=__default_threads_no_string,
		help='number of download threads ({} by default)'.format(
			__default_threads_no_string))
	parser.add_option('-v', '--verbose', dest='verbose',
		action='store_true', default=False,
		help='Show warnings while running the program')
	parser.add_option('-V', '--very_verbose', dest='very_verbose',
		action='store_true', default=False,
		help='Show debug info while running the program')
	parser.add_option('-l', '--log', dest='log_file', type='string',
		action='store', default=None,
		help='If this options is set, the logging information '
			'will not only be printed to standard output, but '
			'also to selected log file.')
	parser.add_option('-d', '--pages_per_second_download_limit', 
		dest='pages_download_limit',
		action='store', default=None,
		help='Maximal number of web pages downloads per second. '
		'By default no limit is imposed.')
	parser.add_option('-s', '--daily_schedule', 
		dest='daily_schedule', action='store', default=None,
		help='Every day start and stop times of the download in form of '
			'"start_time-end_time" eg. "12:30-16:45" or "12-12:30:55". '
			'If this option is not set, '\
			'no download schedule is used and the program works '\
			'until it finishes downloading.')
	(options, args)=parser.parse_args()
	expected_args_no = 3
	if len(args) != expected_args_no:
		parser.error("incorrect number of arguments"
			"(got {} and {} expected)".format(len(args), expected_args_no))
	return (options, args)

class TimeParser:
	@staticmethod
	def parse_time(string):
		elems = string.split(":")
		if len(elems) == 1:
			return datetime.time(hour=int(elems[0]))
		if len(elems) == 2:
			return datetime.time(hour=int(elems[0]), minute=int(elems[1]))
		if len(elems) == 3:
			return datetime.time(hour=int(elems[0]), 
				minute=int(elems[1]), second=int(elems[2]))
		raise Exception("Not supported time format \"{}\"".format(string))
	
	@staticmethod
	def parse_time_interval(string):
		"""
		Parse time interval string of format e.g. '04:56:04-12:44'
		
		@return: (start, end), where both values are of type C{date.datetime}
		"""
		parts = string.split("-")
		start_time = TimeParser.parse_time(parts[0])
		end_time = TimeParser.parse_time(parts[1])
		return (start_time, end_time)

def get_schedule(schedule_string):
	if schedule_string is not None:
		start_time, end_time = TimeParser.parse_time_interval(schedule_string)	
		return DaySchedule(start_time, end_time)
	else:
		return AlwaysActiveSchedule()

def get_tree_summary(root, state_file_path, log_file_path):
	msg = "Summary of the run:\n"
	if root.get_state() == NodeState.ERROR:
		msg += "There were some problems while exploring the tree. "\
			"As a result, probably not all tree nodes were properly processed. "\
			"See the state file ({}) to check which nodes weren't properly "\
			"processed (these are the nodes with \"ERROR\" state). ".\
			format(os.path.abspath(state_file_path))
		if log_file_path is not None:
			msg += "You can also consult the log file ({}).".format(
				os.path.abspath(log_file_path))
	elif root.get_state() == NodeState.CLOSED:
		msg += "The whole tree has been explored; "\
			"all of the nodes were correctly processed."
	else:
		msg += "The tree has not been yet fully explored and processed."
	return msg

def get_logging_level(options):
	log_level = logging.ERROR
	if options.verbose:
		log_level = logging.WARNING
	if options.very_verbose:
		log_level = logging.DEBUG
	return log_level

def get_token_filler_and_browser_creator(pages_download_limit_per_second):
	token_filler = None
	browser_creator = None
	if pages_download_limit_per_second is not None:
		token_bucket = StandardTokenBucket(pages_download_limit_per_second)
		browser_creator = ThrottledWebBrowserCreator(
			MechanizeBrowserCreator(), token_bucket)
		token_filler = TokenBucketFiller(token_bucket, 1, 
			pages_download_limit_per_second)
		token_filler.start()
	else:
		browser_creator = MechanizeBrowserCreator()
	return (token_filler, browser_creator)

def main():
	(options, args) = parse()
	(source_address, destination_dir, state_file_path) = args
	threads_no = int(options.threads_no)
	logging_level = get_logging_level(options)
	log_file_path = options.log_file
	schedule = get_schedule(options.daily_schedule)
	lenient_makedir(destination_dir)
	
	pages_download_limit_per_second = None
	if options.pages_download_limit is not None:
		pages_download_limit_per_second = float(options.pages_download_limit)
	(token_filler, browser_creator) = \
		get_token_filler_and_browser_creator(pages_download_limit_per_second)

	navigators = []
	for _ in range(threads_no):
		navigators.append(
			HTMLMultipageNavigator(source_address, 
				LevelsCreator.create(destination_dir), browser_creator))
	sentinel = StandardNode()
	prog = MultithreadedCrawler(navigators, sentinel, schedule,
		log_file_path, state_file_path, __save_period, logging_level)
	print "Starting download with {} threads from address \"{}\" to "\
		"directory \"{}\"".format(threads_no, source_address, destination_dir)
	print "Activity daily schedule: {}, "\
		"pages download limit per second: {}".format(
			options.daily_schedule, pages_download_limit_per_second)
	prog.run()
	root = sentinel.get_child("root")
	
	if token_filler is not None:
		token_filler.stop()
	
	print "Done.\n"
	print get_tree_summary(root, state_file_path, log_file_path)

if __name__ == '__main__':
	main()
