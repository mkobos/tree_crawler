import threading
import logging

from concurrent_tree_crawler.common.threads.ex_thread import ExThread
from concurrent_tree_crawler.abstract_tree_navigator import NavigationException
from concurrent_tree_crawler.abstract_tree_accessor import NodeAction

class CrawlerThread(ExThread):	
	def __init__(self, navigator, tree, status_queue=None):
		"""
		@type navigator: L{NavigatorTreeWrapper}
		@type tree: L{AbstractTreeAccessor}
		@type status_queue: L{Queue.Queue}
		"""
		ExThread.__init__(self, status_queue)
		self.__nav = navigator
		self.__tree = tree
		self.__should_stop = False

	def run_with_exception(self):
		while not self.__should_stop:
			self.__nav.start_in_sentinel()
			try:
				while not self.__should_stop:
					ret = self.__analyze_children_and_move_to_next_node()
					if ret == True:
						self.__log("Exiting")
						return
			except NavigationException as _:
				pass

	def stop_activity(self):
		self.__should_stop = True

	def __analyze_children_and_move_to_next_node(self):
		"""
		@return: C{True} if the whole tree has been explored.
		"""
		possible_children_names = self.__nav.get_possible_children()
		node_info = self.__tree.update_and_get_child(
			self.__nav.get_current_node(), possible_children_names)
		if node_info is None:
			self.__log("No traversable children available")
			return self.__nav.move_to_parent()
		else:
			(child, action) = node_info
			self.__log("Obtained child \"{}\" with action {}".format(
				child.get_name(), NodeAction.to_str(action)))
			self.__nav.move_to_child(child)
			if action == NodeAction.TO_PROCESS:
				is_leaf = self.__nav.process_node_and_check_if_is_leaf()
				self.__tree.set_node_type(child, is_leaf)
				if is_leaf:
					return self.__nav.move_to_parent()
				else:
					return False
			elif action == NodeAction.TO_VISIT:
				return False
			else:
				assert False, "Unknown action type"

	def __log(self, message):
		"""
		@type message: string
		"""
		node = self.__nav.get_current_node()
		path_str = "/"+("/".join(self.__tree.get_path(node)))
		logging.debug("thread=\"{}\", node=\"{}\": {}".format(
			threading.current_thread().name, path_str, message))