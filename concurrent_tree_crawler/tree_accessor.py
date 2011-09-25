import logging
import threading

from concurrent_tree_crawler.abstract_tree_accessor import \
	AbstractTreeAccessor, NodeAction
from concurrent_tree_crawler.abstract_node import NodeState

class TreeAccessor(AbstractTreeAccessor):
	"""
	An interface for the tree made of L{AbstractNode}s. 
	Access to sensitive methods is protected by concurrent programming objects:
	locks and conditions.
	"""
	def __init__(self, sentinel):
		"""
		@param sentinel: a technical node which will be made parent of the 
			root node.
		@type sentinel: L{AbstractNode}
		"""
		
		self.__sentinel = sentinel
		"""
		The sentinel is a purely technical object. It shouldn't be
		analyzed by the navigator. It is here just to make sure that the
		root of the tree has a parent. This is because it is required by our 
		algorithm that all of the nodes in the tree have a parent.
		"""
		
		self.__root = None
		"""The main business-level element of the tree"""
		
		## The one and only child of the sentinel is the root node
		if self.__sentinel.has_child("root"):
			self.__root = self.__sentinel.get_child("root")
		else:
			self.__root = self.__sentinel.add_child("root", NodeState.OPEN)
	
	def get_sentinel(self):
		return self.__sentinel
	
	def get_root(self):
		return self.__root

	def update_and_get_child(self, node, possible_children_names):
		while True:
			node.get_children_cond().acquire()
			try:
				child = node.update_and_get_child(possible_children_names)
				if child is None: ## No accessible children are available
					return None
				state = child.get_state()
				if state == NodeState.OPEN:
					child.set_state(NodeState.PROCESSING)
					return (child, NodeAction.TO_PROCESS)
				elif state == NodeState.VISITED:
					return (child, NodeAction.TO_VISIT)
				elif state == NodeState.PROCESSING:
					self.__log("Starting to wait on \"{}\" node children".\
						format(node.get_name()))
					node.get_children_cond().wait()
					self.__log("Done waiting on \"{}\" node children".format(
						node.get_name()))
				else:
					assert False, "Unknown node state: {}".format(state)
			finally:
				node.get_children_cond().release()				

	def set_node_type(self, node, is_leaf):
		assert node != self.__sentinel, "Processing sentinel is not allowed"
		parent = node.get_parent()
		parent.get_children_cond().acquire()
		try:
			if is_leaf:
				node.set_state(NodeState.CLOSED)
				self.__internal_update_node_state(parent)
			else:
				node.set_state(NodeState.VISITED)
		finally:
			parent.get_children_cond().notify_all()
			parent.get_children_cond().release()

	def set_error(self, node):
		self.__set_node_state_and_update(node, NodeState.ERROR)

	def __set_node_state_and_update(self, node, new_state):
		assert node != self.__sentinel, "Changing sentinel state is not allowed"
		parent = node.get_parent()
		parent.get_children_cond().acquire()
		try:
			node.set_state(new_state)
			self.__internal_update_node_state(parent)
		finally:
			parent.get_children_cond().notify_all()
			parent.get_children_cond().release()

	def __internal_update_node_state(self, node):
		"""@param node: L{AbstractNode}"""
		if node == self.__sentinel:
			## The state of the sentinel is undefined and not used 
			## in the program, it should not be changed
			return
		new_state = None
		if node.all_children_are_in_one_of_states({NodeState.CLOSED}):
			new_state = NodeState.CLOSED
		elif node.all_children_are_in_one_of_states(
				{NodeState.ERROR, NodeState.CLOSED}):
			new_state = NodeState.ERROR
		## Node state does not have to be changed
		if new_state is None:
			return
		parent = node.get_parent()
		parent.get_children_cond().acquire()
		try:
			node.set_state(new_state)
			self.__internal_update_node_state(parent)
		finally:
			parent.get_children_cond().notify_all()
			parent.get_children_cond().release()

	def __log(self, message):
		"""
		@type message: string
		"""
		logging.debug("thread=\"{}\", {}".format(
			threading.current_thread().name, message))