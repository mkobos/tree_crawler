from concurrent_tree_crawler.common.threads.rw_lock import RWLock
from concurrent_tree_crawler.tree_accessor import TreeAccessor
from concurrent_tree_crawler.abstract_node import NodeState
from concurrent_tree_crawler.abstract_tree_accessor import NodeAction

class RWLockTreeAccessor(TreeAccessor):
	"""
	A version of the L{TreeAccessor} where sensitive methods are protected by
	readers-writers lock.
	"""
		
	def __init__(self, sentinel):
		TreeAccessor.__init__(self, sentinel)
		self.__lock = RWLock()
	
	def get_lock(self):
		return self.__lock
	
	def update_and_get_child(self, node, possible_children_names):
		while True:
			node.get_children_cond().acquire()
			try:
				child_info = self.__update_with_potential_tree_change(
					node, possible_children_names)
				if child_info is None:
					return None
				(child, state) = child_info
				if state == NodeState.OPEN:
					return (child, NodeAction.TO_PROCESS)
				elif state == NodeState.VISITED:
					return (child, NodeAction.TO_VISIT)
				elif state == NodeState.PROCESSING:
					node.get_children_cond().wait()
				else:
					assert False, "Unknown node state: {}".format(state)
			finally:
				node.get_children_cond().release()

	def __update_with_potential_tree_change(self, 
										node, possible_children_names):
		## We have to acquire this lock if we're going to make some
		## changes in the tree. This will prevent the `TreeSaverThread`
		## from accessing the tree while it is modified.
		self.__lock.reader_acquire()
		try:
			child = node.update_and_get_child(possible_children_names)
			if child is None: ## No accessible children are available
				return None
			state = child.get_state()
			if state == NodeState.OPEN:
				child.set_state(NodeState.PROCESSING)
			return (child, state)
		finally:
			self.__lock.reader_release()

	def set_node_type(self, node, is_leaf):
		self.__lock.reader_acquire()
		try:
			TreeAccessor.set_node_type(self, node, is_leaf)
		finally:
			self.__lock.reader_release()

	def set_error(self, node):
		self.__lock.reader_acquire()
		try:
			TreeAccessor.set_error(self, node)
		finally:
			self.__lock.reader_release()