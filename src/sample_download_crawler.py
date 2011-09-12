#!/usr/bin/env python

import logging
from optparse import OptionParser
import os.path

from common.file_helper import lenient_makedir
from crawler.html_multipage_navigator.tree_navigator import \
	HTMLMultipageNavigator
from crawler.standard_node import StandardNode
from crawler.html_multipage_navigator.sample_page_analyzer import \
	PageAnalyzerFactory
from crawler.abstract_node import NodeState
from crawler.crawler_program import CrawlerProgram
from common.threads.token_bucket import TokenBucketFiller, StandardTokenBucket

__default_threads_no_string = '2'
__save_period = 0.1

def parse():
	usage="usage: %prog [-t DOWNLOAD_THREADS_NO] [-l LOG_FILE] "\
		"[--verbose] [--very_verbose] [--pages_download_limit]"\
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
	parser.add_option('-d', '--pages_download_limit', 
		dest='pages_download_limit',
		action='store', default=None,
		help='Maximal number of web pages downloads per second. '
		'By default no limit is imposed.')
	(options, args)=parser.parse_args()
	expected_args_no = 3
	if len(args) != expected_args_no:
		parser.error("incorrect number of arguments"
			"(got {} and {} expected)".format(len(args), expected_args_no))
	return (options, args)

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

def main():
	(options, args) = parse()
	(source_address, destination_dir, state_file_path) = args
	threads_no = int(options.threads_no)
	logging_level = get_logging_level(options)
	log_file_path = options.log_file
	lenient_makedir(destination_dir)
	
	pages_download_limit_per_second = None
	if options.pages_download_limit is not None:
		pages_download_limit_per_second = int(options.pages_download_limit)
	token_bucket = None
	token_filler = None
	if pages_download_limit_per_second is not None:
		token_bucket = StandardTokenBucket(pages_download_limit_per_second)
		token_filler = TokenBucketFiller(token_bucket, 1, 
			pages_download_limit_per_second)
		token_filler.start()

	analyzer_factory = PageAnalyzerFactory(destination_dir, token_bucket)
	navigators = []
	for _ in range(threads_no):
		navigators.append(
			HTMLMultipageNavigator(analyzer_factory, source_address))
	sentinel = StandardNode()
	prog = CrawlerProgram(navigators, sentinel, 
			log_file_path, state_file_path, __save_period, logging_level)
	print "Starting download with {} threads from address \"{}\" to "\
		"directory \"{}\"".format(threads_no, source_address, destination_dir)
	prog.run()
	root = sentinel.get_child("root")
	
	if pages_download_limit_per_second is not None:
		token_filler.stop()
	
	print "Done.\n"
	print get_tree_summary(root, state_file_path, log_file_path)

if __name__ == '__main__':
	main()
