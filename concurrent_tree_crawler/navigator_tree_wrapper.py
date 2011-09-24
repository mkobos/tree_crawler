import logging
import threading

from concurrent_tree_crawler.abstract_tree_navigator import NavigationException

class NavigatorTreeWrapper:
	"""
	Wrapper for the tree navigator (L{AbstractTreeNavigator}).
	It makes sure that accessing our tree representation
	object L{TreeAccessor} is synchronized with actions executed on
	L{AbstractTreeNavigator} object. It also handles L{NavigationException}s
	that might occur while using the navigator.
	"""
	
	def __init__(self, navigator, tree):
		"""
		@type navigator: L{AbstractTreeNavigator}
		@type tree: L{AbstractTreeAccessor}
		"""
		self.__nav = navigator
		self.__tree = tree
		self.__current_node = None

	def get_current_node(self):
		return self.__current_node

	def start_in_sentinel(self):
		self.__current_node = self.__tree.get_sentinel()
		self.__log("Started in sentinel")
	
	def get_possible_children(self):
		"""
		@return: children names
		@rtype: list of strings
		"""
		ret = None
		if self.__current_node == self.__tree.get_sentinel():
			ret = ["root"]
		else:
			try:
				ret = self.__nav.get_children()
			except NavigationException as ex:
				self.__handle_exception(ex, "Getting children failed")
		self.__log("Got possible children")
		return ret
	
	def move_to_child(self, destination_node):
		"""
		@param destination_node: L{AbstractNode}
		"""
		if self.__current_node == self.__tree.get_sentinel():
			self.__start_in_root()
		else:
			try:
				self.__current_node = destination_node
				self.__nav.move_to_child(destination_node.get_name())
			except NavigationException as ex:
				self.__handle_exception(ex, "Moving to child failed")
		self.__log("Moved to child")

	def __start_in_root(self):
		try:
			self.__current_node = self.__tree.get_root()
			self.__nav.start_in_root()
		except NavigationException as ex:
			self.__handle_exception(ex, 
				"Initializing navigator to start in the root failed")

	def move_to_parent(self):
		"""
		@return: C{True} iff the navigator is currently in the root. It means
			that the whole tree has been traversed.
		"""
		ret = None
		## The first part of this condition is true, when the root is CLOSEd
		## and a new thread starting from sentinel is coming
		if self.__current_node.get_parent() is None or \
			self.__current_node.get_parent() == self.__tree.get_sentinel():
			## The sentinel node should never be visited by the 
			## L{AbstractTreeNavigator}
			self.__current_node = self.__tree.get_sentinel()
			ret = True
		else:
			try:
				self.__current_node = self.__current_node.get_parent()
				self.__nav.move_to_parent()
				ret = False
			except NavigationException as ex:
				self.__handle_exception(ex, "Moving to parent failed")
		self.__log("Moved to parent")
		return ret

	def process_node_and_check_if_is_leaf(self):
		"""
		@return: C{True} if the current node is a leaf, C{False} if it is 
			an internal node. 
		"""
		assert self.__current_node != self.__tree.get_sentinel()
		try:
			ret =  self.__nav.process_node_and_check_if_is_leaf()
			self.__log("Processed node, is_leaf={}".format(ret))
			return ret
		except NavigationException as ex:
			self.__handle_exception(ex, "Processing node failed")

	def __handle_exception(self, ex, error_message):
		self.__log_exception(error_message, ex, self.__current_node)
		self.__tree.set_error(self.__current_node)
		raise ex		

	def __log_exception(self, error_message, ex, error_node):
		"""
		@type error_message: string
		@type ex: L{Exception}
		@type error_node: L{AbstractNode}
		"""
		path_str = "/"+("/".join(self.__tree.get_path(error_node)))
		logging.warning("thread==\"{}\", navigation exception in node \"{}\":"
			"{}\". Detailed message: \"{}\".".format(
				threading.current_thread().name, path_str, error_message, ex))
	
	def __log(self, message):
		"""
		@type message: string
		"""
		path_str = "/"+("/".join(self.__tree.get_path(self.get_current_node())))
		logging.debug("thread=\"{}\", node=\"{}\": {}".format(
			threading.current_thread().name, path_str, message))