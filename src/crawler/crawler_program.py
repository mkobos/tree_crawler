import os
import logging

from common.file_helper import lenient_makedir
from common.logger import Logger
from crawler.crawlers_manager import CrawlersManager
from crawler.rw_lock_tree_accessor import RWLockTreeAccessor
from crawler.navigator_tree_wrapper import NavigatorTreeWrapper
from crawler.tree_saver_thread import TreeSaverThread
from crawler.abstract_node import NodeState
from crawler.xml_tree_serialization import XMLTreeReader

class CrawlerProgram:
	def __init__(self, navigators, sentinel, 
			log_file_path, state_file_path, save_period,
			logging_level=logging.ERROR):
		"""
		@param navigators: list of navigators to be used by the crawler.
			Each navigator will be run in a separate thread, thus the
			number of the threads is equal to the number of navigators.
		@type navigators: list of L{AbstractTreeNavigator}
		@param sentinel: a technical node which will be made parent of the 
			root node.
		@type sentinel: L{AbstractNode}
		@param log_file_path: path to the log file. If C{None}, no log file
			will be used
		@param state_file_path: path to the file where the state of the
			program will be saved
		@param save_period: time between saving the tree tree state
		@param logging_level: one of the logging level constants from C{logging}
		"""
		lenient_makedir(os.path.dirname(log_file_path))
		if os.path.exists(state_file_path):
			print "State file already exists. Loading the tree from this "\
				"file and changing nodes with state PROCESSING to OPEN "\
				"state... ",
			self.__load_state_file(state_file_path, sentinel)
			print "Done."
		else:
			lenient_makedir(os.path.dirname(state_file_path))
		self.__tree = RWLockTreeAccessor(sentinel)
		navigator_wrappers = []
		for navigator in navigators:
			navigator_wrapper = NavigatorTreeWrapper(navigator, self.__tree)
			navigator_wrappers.append(navigator_wrapper)
		self.__manager = CrawlersManager(self.__tree, navigator_wrappers)
		self.__saver_thread = \
			TreeSaverThread(state_file_path, self.__tree, save_period)
		self.__saver_thread.setDaemon(True)
		self.__saver_thread.start()
		self.__logging_level = logging_level
		self.__log_file_path = log_file_path
	
	def run(self):
		"""
		@return: sentinel node
		@rtype: L{AbstractNode}
		"""
		Logger.start(file_path=self.__log_file_path, 
			logging_level=self.__logging_level)
		self.__manager.start()
		self.__manager.wait_until_finish()
		self.__saver_thread.stop_activity()
		self.__saver_thread.join()
		Logger.stop()
		return self.__tree.get_sentinel()

	@staticmethod
	def __load_state_file(file_path, sentinel):
		with open(file_path) as f:
			reader = XMLTreeReader(f)
			reader.read(sentinel)
		CrawlerProgram.__change_state_from_PROCESSING_to_OPEN(sentinel.get_child("root"))
	
	@staticmethod
	def __change_state_from_PROCESSING_to_OPEN(node):
		if node.get_state() == NodeState.PROCESSING:
			node.set_state(NodeState.OPEN)
		for child in node.get_children():
			CrawlerProgram.__change_state_from_PROCESSING_to_OPEN(child)
