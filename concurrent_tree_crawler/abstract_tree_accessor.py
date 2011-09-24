from concurrent_tree_crawler.abstract_node import AbstractNode, NodeState

class NodeAction:
	"""Enumeration describing actions that can be taken by a crawler when
	entering a new node""" 
	
	TO_PROCESS = 0
	TO_VISIT = 1
	
	@staticmethod
	def to_str(action):
		"""@type action: L{NodeAction} enum"""
		if action == NodeAction.TO_PROCESS:
			return "TO_PROCESS"
		elif action == NodeAction.TO_VISIT:
			return "TO_VISIT"

class AbstractTreeAccessor:
	"""
	An interface for the tree made of L{AbstractNode}s.
	"""

	def get_sentinel(self):
		"""
		@return: sentinel node
		@rtype: L{AbstractNode}
		"""
		raise NotImplementedError
	
	def get_root(self):
		"""
		@return: root node
		@rtype: L{AbstractNode}
		"""
		raise NotImplementedError

	def get_path(self, node):
		"""
		A convenience method. Returns tree path to the given node.
		
		@type node: L{AbstractNode}
		@return: subsequent node names from the tree root to the current node
		@rtype: list of strings
		"""
		path = []
		while node != self.get_sentinel():
			path.append(node.get_name())
			node = node.get_parent()
		path.reverse()
		return path

	def update_and_get_child(self, node, possible_children_names):
		"""
		Append new children to the node and return a child that can be
		entered by the crawler.
		
		@param node: node considered
		@type node: L{AbstractNode}
		@param possible_children_names: list of children names
		@type possible_children_names: list of strings
		@return: children node along with information what the crawler should
			do with it. C{None} instead is returned if all children have 
			state C{NodeState.CLOSED} or C{NodeState.ERROR} or the node 
			has no children. 
		@rtype: (L{AbstractNode}, L{NodeAction}) pair or C{None}
		"""
		raise NotImplementedError

	def set_node_type(self, node, is_leaf):
		"""
		Set the leaf state of the node
		
		@param is_leaf: C{True} iff the node is a leaf		
		"""
		raise NotImplementedError

	def set_error(self, node):
		"""Set the node state as C{NodeState.ERROR}"""
		raise NotImplementedError