class NavigationException(Exception):
	"""
	See the description of C{AbstractTreeNavigator} class for a discussion
	of this exception usage.
	"""		
	pass

class AbstractTreeNavigator:
	"""
	An object that has a direct access to the physical tree elements 
	(e.g. web pages) traversed by the crawler.
	
	Each method declared in this abstract class can raise a 
	L{NavigationException}. If such an exception is raised, it will be gently
	handled by the crawler -- it won't terminate the crawler thread nor
	the whole program, but the information that an error occurred will be saved
	in the tree structure and the crawler will be restarted. If other
	kind of exception is raised, it will terminate the thread and the whole 
	program.
	"""
	
	def start_in_root(self):
		"""
		Start in the root node of the tree
		
		@raise NavigationException: see class description for details of
			ramification of raising such an exception.
		"""
		return NotImplementedError

	def get_children(self):
		"""
		@return: names of children of the current node
		@rtype: list of strings
		
		@raise NavigationException: see class description for details of
			ramification of raising such an exception.
		"""
		return NotImplementedError

	def move_to_child(self, child_name):
		"""
		Move to the child of the current node.
		
		@raise NavigationException: see class description for details of
			ramification of raising such an exception.
		"""
		return NotImplementedError
		
	def move_to_parent(self):
		"""
		Move to the parent of the current node
		
		@raise NavigationException: see class description for details of
			ramification of raising such an exception.
		"""
		return NotImplementedError

	def process_node_and_check_if_is_leaf(self):
		"""
		@return: C{True} if the current node is a leaf, C{False} if it is 
			an internal node. 
		@raise NavigationException: see class description for details of
			ramification of raising such an exception.
		"""
		return NotImplementedError
