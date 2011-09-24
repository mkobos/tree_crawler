import threading

from collections import OrderedDict
from concurrent_tree_crawler.abstract_node import AbstractNode, NodeState

class StandardNode(AbstractNode):
	"""A simple in-memory implementation of the L{AbstractNode}."""
	
	def __init__(self, parent=None, name="sentinel", state=NodeState.OPEN):
		"""
		@type parent: L{StandardNode}, equals C{None} if node is 
			the	sentinel node
		@type name: string
		@type state: L{NodeState}
		"""
		self.__parent = parent
		
		self.__name = name
		
		self.__state = state
		
		self._children = \
			[OrderedDict() for _ in xrange(NodeState.MAX_ENUM_INDEX+1)]
		"""Array indexed by the L{NodeState} enumeration index"""
		
		self.__cond = threading.Condition()

	def get_children_cond(self):
		return self.__cond

	def get_name(self):
		return self.__name

	def get_state(self):
		return self.__state
	
	def set_state(self, new_state):
		if self.__parent is not None:
			child_found = False
			for state in xrange(NodeState.MAX_ENUM_INDEX+1):
				if self.__name in self.__parent._children[state]:
					del self.__parent._children[state][self.__name]
					child_found = True
					break
			assert child_found, "This node not found among parent's children"
			self.__parent._children[new_state][self.__name] = self
		self.__state = new_state
	
	def get_parent(self):
		return self.__parent

	def has_child(self, name):
		for state in xrange(NodeState.MAX_ENUM_INDEX+1):
			if name in self._children[state]:
				return True
		return False

	def get_child(self, name):
		for state in xrange(NodeState.MAX_ENUM_INDEX+1):
			if name in self._children[state]:
				return self._children[state][name]
		assert False, "Child with given name not found"
	
	def get_children(self):
		children = []
		for state in xrange(NodeState.MAX_ENUM_INDEX+1):
			for (_, node) in self._children[state].iteritems():
				children.append(node)
		return children
	
	def add_child(self, name, state):
		assert name not in self._children[state]
		new_child = StandardNode(self, name, state)
		self._children[state][name] = new_child
		return new_child
	
	def _has_children(self, state):
		return len(self._children[state]) > 0