from concurrent_tree_crawler.abstract_tree_navigator import \
	AbstractTreeNavigator

class SimpleDFSCrawler:
	def __init__(self, navigator):
		"""@type navigator: C{AbstractTreeNavigator}"""
		self.__navigator = navigator

	def run(self):
		self.__navigator.start_in_root()
		self.__process_current_node()

	def __process_current_node(self):
		is_leaf = None
		try:
			is_leaf = self.__navigator.process_node_and_check_if_is_leaf()
		except Exception as _:
			pass			
		if not is_leaf:
			children = self.__navigator.get_children()
			for child in children:
				self.__navigator.move_to_child(child)
				self.__process_current_node()
				self.__navigator.move_to_parent()

