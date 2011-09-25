import logging
import datetime
import os.path
import argparse

from concurrent_tree_crawler.standard_node import StandardNode
from concurrent_tree_crawler.abstract_node import NodeState
from concurrent_tree_crawler.multithreaded_crawler import MultithreadedCrawler
from concurrent_tree_crawler.common.activity_schedule import \
	DaySchedule, AlwaysActiveSchedule

class CmdLnMultithreadedCrawler:
	"""
	A class that creates the L{MultithreadedCrawler} object based on 
	command-line parameters
	"""
		
	__default_threads_no = 2
	__save_period = 0.1
	
	def __init__(self, navigators_creator):
		"""@type navigators_creator: L{AbstractCmdLnNavigatorsCreator}"""
		self.__navigators_creator = navigators_creator

	def __parse(self):
		parser = argparse.ArgumentParser()
		parser.add_argument("state_file", 
			help="Path to file where the state of the algorithm is saved.")
		parser.add_argument("--threads", type=int,
			default=self.__default_threads_no, help="number of crawler threads")
		parser.add_argument("-v", "--verbose", action="append_const", 
			const=None,
			help="If used once, shows warnings while running the program; "
			"if used twice, shows debug info while running the program.")
		parser.add_argument("--log_file", 
			help="If this options is set, the logging information "
			"will be printed not only to standard output, but "
			"also to selected log file.")
		parser.add_argument("--daily_schedule", 
			help='Daily start and stop times of the crawler program in form of '
				'"start_time-end_time" e.g. "12:30-16:45" or "12-12:30:55". '
				'If this option is not set, '
				'no schedule is used and the program works '
				'until it finishes its task.')
		self.__navigators_creator.fill_parser(parser)
		args = parser.parse_args()
		return args

	@staticmethod
	def __get_schedule(schedule_string):
		if schedule_string is not None:
			start_time, end_time = _TimeParser.parse_time_interval(
				schedule_string)	
			return DaySchedule(start_time, end_time)
		else:
			return AlwaysActiveSchedule()

	@staticmethod
	def __get_tree_summary(root, state_file_path, log_file_path):
		msg = "Summary of the run:\n"
		if root.get_state() == NodeState.ERROR:
			msg += "There were some problems while exploring the tree. "\
				"As a result, probably not all tree nodes were properly processed. "\
				"See the state file ({}) to check which nodes weren't properly "\
				"processed (these are the nodes with \"ERROR\" state). ".format(
					os.path.abspath(state_file_path))
			if log_file_path is not None:
				msg += "You can also consult the log file ({}).".format(
					os.path.abspath(log_file_path))
		elif root.get_state() == NodeState.CLOSED:
			msg += "The whole tree has been explored; "\
				"all of the nodes were correctly processed."
		else:
			msg += "The tree has not been yet fully explored and processed."
		return msg

	@staticmethod
	def __get_logging_level(args):
		if len(args.verbose) == 0:
			return logging.ERROR
		elif len(args.verbose) == 1:
			return logging.WARNING
		else:
			return logging.DEBUG


	def run(self):
		args = self.__parse()
		threads_no = args.threads
		logging_level = self.__get_logging_level(args)
		log_file_path = args.log_file
		schedule = self.__get_schedule(args.daily_schedule)
		
		navigators = self.__navigators_creator.create(args, threads_no)

		sentinel = StandardNode()
		prog = MultithreadedCrawler(navigators, sentinel, schedule,
			log_file_path, args.state_file, self.__save_period, logging_level)
		print "Starting activity with {} threads, "\
			"activity daily schedule: {}".format(
				threads_no, args.daily_schedule)
		prog.run()
		root = sentinel.get_child("root")
		
		self.__navigators_creator.on_exit()
		
		print "Done.\n"
		print self.__get_tree_summary(root, args.state_file, log_file_path)

class _TimeParser:
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
		start_time = _TimeParser.parse_time(parts[0])
		end_time = _TimeParser.parse_time(parts[1])
		return (start_time, end_time)
