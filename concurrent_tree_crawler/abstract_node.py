class NodeState:
	"""Enumeration describing state of processing of a certain node"""

	OPEN = 0
	"""Node has not been yet traversed/visited by any crawler.
	This is the initial state of each node."""

	PROCESSING = 1
	"""Node is currently processed by some crawler."""
	
	VISITED = 2
	"""Node has been visited by at least one crawler. It is an internal node.
	There is at least one child of this node that is in a state of 
	OPEN or VISITED or PROCESSING."""
	
	CLOSED = 3
	"""The leaf node has been processed or all the children of 
	the internal node are in a CLOSED state. 
	Traversing children of this node by a new crawler would be pointless."""
	
	ERROR = 4
	"""1) A crawler was not able to analyze this node or 2) 
	all children nodes of this node are in a state of CLOSED or ERROR"""
	
	MAX_ENUM_INDEX = ERROR
	"""A purely technical field indicating the maximal enumeration index"""
	
	@staticmethod
	def to_str(state):
		"""@type state: L{NodeState} enum"""
		if state == NodeState.OPEN:
			return "OPEN"
		elif state == NodeState.PROCESSING:
			return "PROCESSING"
		elif state == NodeState.VISITED:
			return "VISITED"
		elif state == NodeState.CLOSED:
			return "CLOSED"
		elif state == NodeState.ERROR:
			return "ERROR"
		else:
			return None
	
	@staticmethod
	def from_str(string):
		"""
		@return: enumeration corresponding to given string, C{None} if
			we were unable to parse the string
		@rtype: L{NodeState} enum
		"""
		if string == "OPEN":
			return NodeState.OPEN
		elif string == "PROCESSING":
			return NodeState.PROCESSING
		elif string == "VISITED":
			return NodeState.VISITED
		elif string == "CLOSED":
			return NodeState.CLOSED
		elif string == "ERROR":
			return NodeState.ERROR
		else:
			return None

class AbstractNode:
	"""A node representing a single element of the tree traversed by the
		crawler"""
	
	def get_children_cond(self):
		"""
		@return: condition object related to the children of this node
		@rtype: L{threading.Condition}
		"""
		raise NotImplementedError
	
	def get_name(self):
		"""
		@return: name of the node. It should be unique among children of
			this node's parent"""
		raise NotImplementedError
	
	def get_state(self):
		"""
		@return: state of the node
		@rtype: L{NodeState}
		"""
		raise NotImplementedError
	
	def set_state(self, new_state):
		"""
		@param new_state: new state of the node
		@type new_state: L{NodeState}
		"""
		raise NotImplementedError

	def get_parent(self):
		"""
		@rtype: L{AbstractNode}, it is C{None} if the node is the sentinel node
		"""
		raise NotImplementedError

	## OPTIMIZE?
	def update_and_get_child(self, possible_children_names):
		"""
		@rtype: L{AbstractNode}
		"""
		accessible_children = {NodeState.OPEN: None, 
			NodeState.VISITED: None, NodeState.PROCESSING: None}
		for possible_name in possible_children_names:
			if not self.has_child(possible_name):
				self.add_child(possible_name, NodeState.OPEN)
			child = self.get_child(possible_name)
			state = child.get_state()
			if state in accessible_children:
				if accessible_children[state] is None:
					accessible_children[state] = child
		accessible_children_state_priority = [NodeState.OPEN, 
			NodeState.VISITED, NodeState.PROCESSING]
		for state in accessible_children_state_priority:
			if accessible_children[state] is not None:
				return accessible_children[state]
		return None

	def has_child(self, name):
		"""
		@return: True if node has child with given name
		"""
		raise NotImplementedError
					
	def get_child(self, name):
		"""
		@rtype: L{AbstractNode}
		"""
		raise NotImplementedError
	
	def get_children(self):
		"""
		@rtype: list of L{AbstractNode}s
		"""
		raise NotImplementedError
	
	def add_child(self, child_name, state):
		"""
		@type state: L{NodeState}
		@return: added child node
		@rtype: L{AbstractNode}
		"""
		raise NotImplementedError
	
	def all_children_are_in_one_of_states(self, states):
		"""
		@type states: set of L{NodeState}s
		@return: C{True} iff all children are in one of the given states
		"""
		no_children_encountered = True
		for state in xrange(NodeState.MAX_ENUM_INDEX+1):
			if state not in states:
				if self._has_children(state):
					return False
			else:
				if self._has_children(state) > 0:
					no_children_encountered = False
		assert not no_children_encountered, "The given node has no children"
		return True

	def _has_children(self, state):
		"""
		An auxiliary method used only by the 
		L{all_children_are_in_one_of_states} method
		
		@type state: L{NodeState}
		@return: C{True} iff the node has at least one child in given state
		"""
		raise NotImplementedError
	
	def __str__(self):
		return "name=\"{}\", state=\"{}\"".format(
			self.get_name(), NodeState.to_str(self.get_state()))