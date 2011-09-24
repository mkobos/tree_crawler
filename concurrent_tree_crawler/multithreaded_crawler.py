import os
import logging
import time
import datetime

from concurrent_tree_crawler.common.file_helper import lenient_makedir
from concurrent_tree_crawler.common.logger import Logger
from concurrent_tree_crawler.common.activity_schedule import AlwaysActiveSchedule
from concurrent_tree_crawler.crawlers_manager import CrawlersManager
from concurrent_tree_crawler.rw_lock_tree_accessor import RWLockTreeAccessor
from concurrent_tree_crawler.navigator_tree_wrapper import NavigatorTreeWrapper
from concurrent_tree_crawler.tree_saver_thread import TreeSaverThread
from concurrent_tree_crawler.abstract_node import NodeState
from concurrent_tree_crawler.xml_tree_serialization import XMLTreeReader

class MultithreadedCrawler:
	"""
	Runs several threads to crawl the tree.
	
	It is also responsible for all the ancillary stuff: 
	makes sure that the	state of the tree is saved to disk, 
	sets up the logging level etc.
	"""
	
	def __init__(self, navigators, sentinel, activity_schedule=None,  
			log_file_path=None, state_file_path=None, save_period=None,
			logging_level=logging.ERROR):
		"""
		@param navigators: list of navigators to be used by the crawler.
			Each navigator will be run in a separate thread, thus the
			number of the threads is equal to the number of navigators.
		@type navigators: list of L{AbstractTreeNavigator}s
		@param sentinel: a technical node which will be made parent of the 
			root node.
		@type sentinel: L{AbstractNode}
		@param activity_schedule: if C{None}, no schedule is used and the 
			program works until it finishes crawling.
		@type activity_schedule: L{AbstractActivitySchedule} 
		@param log_file_path: path to the log file. If C{None}, no log file
			will be used.
		@param state_file_path: path to the file where the state of the
			program will be saved. If C{None}, the state will not be saved.
		@param save_period: time between saving the tree state. If
			C{state_file_path} is C{None}, this value is ignored.
		@param logging_level: one of the logging level constants from C{logging}
		"""
		if log_file_path is not None:
			lenient_makedir(os.path.dirname(log_file_path))
		if state_file_path is not None:
			if os.path.exists(state_file_path):
				print "State file already exists. Loading the tree from this "\
					"file and changing nodes with state PROCESSING to OPEN ... ",
				self.__load_state_file(state_file_path, sentinel)
				print "Done."
			else:
				lenient_makedir(os.path.dirname(state_file_path))
		self.__tree = RWLockTreeAccessor(sentinel)
		self.__navigators = navigators
		self.__manager = None
		self.__state_file_path = state_file_path
		self.__save_period = save_period
		self.__activity_schedule = activity_schedule
		if activity_schedule is None:
			self.__activity_schedule = AlwaysActiveSchedule()
		self.__logging_level = logging_level
		self.__log_file_path = log_file_path
	
	def run(self):
		"""
		@return: sentinel node
		@rtype: L{AbstractNode}
		"""
		self.__manager = self._create_crawlers_manager(
			self.__tree, self.__navigators)
		if self.__log_file_path is not None:
			Logger.start(file_path=self.__log_file_path, 
				logging_level=self.__logging_level)
		while True:
			activity_time = self.__sleep_until_activity_period()
			saver_thread = None
			if self.__state_file_path is not None:
				saver_thread = self.__start_tree_saver_thread()
			self.__manager.start()
			threads_finished = \
				self.__manager.wait_until_finish(timeout=activity_time)
			if self.__state_file_path is not None:
				saver_thread.stop_activity()
				saver_thread.join()
			if threads_finished:
				break
		if self.__log_file_path is not None:
			Logger.stop()
		return self.__tree.get_sentinel()

	def _create_crawlers_manager(self, tree, navigators):
		navigator_wrappers = []
		for navigator in navigators:
			navigator_wrapper = NavigatorTreeWrapper(navigator, tree)
			navigator_wrappers.append(navigator_wrapper)
		return CrawlersManager(tree, navigator_wrappers)

	def __start_tree_saver_thread(self):
		t = TreeSaverThread(
			self.__state_file_path, self.__tree, self.__save_period)
		t.setDaemon(True)
		t.start()
		return t

	def __sleep_until_activity_period(self):
		"""
		Sleep (stop program execution) until there's a time to wake up.

		@return: activity time, i.e. time until the start of the next 
			sleep period, C{None} if such time point cannot be determined 
			(as in case when the activity time will not stop in future).
		@rtype: number of seconds
		"""
		while True:
			now = datetime.datetime.now()
			info = self.__activity_schedule.get_activity_info(now)
			if info.future_mode_change is None:
				if info.is_in_activity_period:
					return None
				else:
					raise Exception("Going to sleep forever?")
			mode_change_time = (info.future_mode_change - now).total_seconds()
			if not info.is_in_activity_period:
				logging.info("Going to sleep for {:.1f} seconds "
							"(according to schedule)".format(
					mode_change_time))
				time.sleep(mode_change_time)
				logging.info("Awaken")
			else:
				logging.info("Starting activity for {:.1f} seconds "
							"(according to schedule)".format(
					mode_change_time))
				return mode_change_time

	@staticmethod
	def __load_state_file(file_path, sentinel):
		with open(file_path) as f:
			reader = XMLTreeReader(f)
			reader.read(sentinel)
		MultithreadedCrawler.__change_state_from_PROCESSING_to_OPEN(
			sentinel.get_child("root"))
	
	@staticmethod
	def __change_state_from_PROCESSING_to_OPEN(node):
		if node.get_state() == NodeState.PROCESSING:
			node.set_state(NodeState.OPEN)
		for child in node.get_children():
			MultithreadedCrawler.__change_state_from_PROCESSING_to_OPEN(child)
