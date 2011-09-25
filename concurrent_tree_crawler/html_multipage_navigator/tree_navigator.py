import logging
from collections import OrderedDict
from collections import deque

from concurrent_tree_crawler.abstract_tree_navigator import \
	AbstractTreeNavigator, NavigationException
from concurrent_tree_crawler.html_multipage_navigator.web_browser import \
	MechanizeBrowserCreator

class HTMLMultipageNavigator(AbstractTreeNavigator):
	"""
	A web site tree navigator. 
	
	It is assumed that all web pages corresponding to the nodes of the tree on 
	the given level have the same basic	characteristics and are analyzed 
	in the same way, namely by the same object inheriting from  
	L{AbstractPageAnalyzer}. In particular, all of the leaf web pages are 
	placed on the same level of the tree. Some of the parts of the tree might
	be missing, which results in marking certain nodes of the tree as ERROR.
	"""
	
	__repetition_suffix_template = "-repetition_{}"
	__generate_new_name_max_repetitions = int(10e4)

	def __init__(self, address, levels, browser_creator=None):
		"""
		@param browser_creator: a creator of browsers that will be used
			while crawling the web site. The default browser used here 
			is L{MechanizeBrowser}.
		@type browser_creator: L{AbstractWebBrowserCreator}
		@param levels: list of L{Level} objects. The first element is a level 
			corresponding to the root node, the last one corresponds to
			leafs level.
		@param address: URL address string
		"""
		self.__address = address
		self.__browser_creator = browser_creator
		if browser_creator is None:
			self.__browser_creator = MechanizeBrowserCreator()
		self.__br = None
		self.__levels = levels
		self.__path = None
		self.__children_history = None
		self.__current_children = None
		"""
		Info about children on current level of tree structure.
		L{OrderedDictionary} with the key as child name and the value 
		as a link to child web page.
		"""

	def start_in_root(self):
		self.__br = self.__browser_creator.create()
		self.__br.open(self.__address)
		self.__path = [self.__levels[0].name]
		self.__children_history = _ChildrenHistory()
		self.__current_children = self.__get_current_children()

	def get_path(self):
		"""
		@return: path to the tree node the navigator is currently in i.e.
			subsequent node names from the tree root to the current node
		"""
		return self.__path

	def get_children(self):
		return self.__current_children.keys()
	
	def __get_current_children(self):
		children = OrderedDict()
		page_index = 0
		child_links_retrieved_so_far = 0
		current_level = self.__levels[self.__get_current_level()]
		while True:
			page_links = \
				current_level.page_analyzer.get_links(
					self.__br.response(), child_links_retrieved_so_far)
			for (name, link) in page_links.children:
				if name in children:
					new_name = \
						self.__generate_new_name(name, children)
					if new_name is None:
						logging.error("Unable to generate a new name "
							"for a repeating child name \"{}\" "
							"(link=\"{}\") in node \"{}\": "
							"all of the proposed new name variants are "
							"already in use".format(
								name, link, "/".join(self.__path)))
						continue
					children[new_name] = link
				else:
					children[name] = link
			next_page_link = page_links.next_page_link
			if next_page_link is None:
				break
			self.__br.open(next_page_link)
			page_index += 1
			child_links_retrieved_so_far += len(page_links.children)
		if page_index > 0:
			self.__br.back(page_index) ## Get back to the first page
		return children
	
	@staticmethod
	def __generate_new_name(original_name, children_dict):
		max_rep = HTMLMultipageNavigator.__generate_new_name_max_repetitions
		for i in xrange(max_rep):
			name = original_name + \
				HTMLMultipageNavigator.__repetition_suffix_template.format(i+1)
			if name not in children_dict:
				return name
		return None
		
	def __get_current_level(self):
		return len(self.get_path())-1

	def __is_on_leafs_level(self):
		return len(self.__path) == len(self.__levels)

	def move_to_child(self, child_name):
		assert not self.__is_on_leafs_level()
		try:
			self.__br.open(self.__current_children[child_name])
			self.__path.append(child_name)
			self.__children_history.push(self.__current_children)
			self.__current_children = self.__get_current_children()
		except Exception as ex:
			raise NavigationException(ex)
		
	def move_to_parent(self):
		assert self.__get_current_level() > 0
		try:
			self.__br.back()
			self.__path = self.__path[:-1]
			self.__current_children = self.__children_history.pop()
		except Exception as ex:
			raise NavigationException(ex)

	def process_node_and_check_if_is_leaf(self):
		try:
			response = self.__br.response()
			analyzer = self.__levels[self.__get_current_level()].page_analyzer
			analyzer.process(self.__path, response)
			if len(self.__current_children) > 0:
				return False
			return True
		except Exception as ex:
			raise NavigationException(ex)

class _ChildrenHistory:
	"""
	A history of children nodes on consecutive levels of hierarchy. 
	Implemented as a FIFO queue.
	"""
	
	def __init__(self):
		self.__queue = deque()
	
	def push(self, children):
		"""
		@param children: info about children on current level of tree structure 
		@type children: L{OrderedDictionary} with the key being the child name
			and the value being the link to child web page.
		"""
		self.__queue.append(children)
	
	def pop(self):
		"""
		@return: info about children on current level of tree structure 
		@rtype: L{OrderedDictionary} with the key being the child name
			and the value being the link to child web page.
		"""
		return self.__queue.pop()
