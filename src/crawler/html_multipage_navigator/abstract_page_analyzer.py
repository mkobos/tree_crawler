from crawler.html_multipage_navigator.web_browser import AbstractWebBrowser

class PageLinks:
	def __init__(self, children, next_page_link):
		"""
		@param children: A list of (name of child, child link) pairs.
		@param next_page_link: Link to the next page on this level.
		"""
		self.children = children
		"""A list of (name of child, child link) pairs."""

		self.next_page_link = next_page_link
		"""Link to the next page on this level. 
		C{None}, if there is no such link on the page."""

class AbstractPageAnalyzer:
	def process(self, tree_path, page_file):
		"""
		Process the node (usually the processing is done once for every node).
		"""
		pass
	
	def get_links(self, page_file, child_links_retrieved_so_far_count):
		"""
		@param page_file: file-like structure to be analyzed
		@param child_links_retrieved_so_far_count: number of child links 
			retrieved so far in current node (from previous pages)
		@return: information about links on given page. 
			The given default implementation is made for a leaf node 
			(a page with no children).
		@rtype: L{PageLinks}
		"""
		return PageLinks([], None)

class Level:
	def __init__(self, name, page_analyzer):
		"""
		@type name: Name of the level. 
			Example names: "books", "chapters", "sections".
		@type page_analyzer: L{AbstractPageAnalyzer}
		"""
		self.name = name
		"""Name of the level. Example names: "books", "chapters", "sections"."""

		self.page_analyzer = page_analyzer
		"""L{AbstractPageAnalyzer} object."""

class AbstractPageAnalyzerFactory:
	def create_browser(self, address):
		"""
		Create the browser and navigate it to the start page.
		This method has to be thread-safe since it is called as the method
		of the same object in different threads.
		This method contains a default implementation.

		@rtype: L{AbstractWebBrowser}
		"""
		raise NotImplementedError

	def create_page_analyzers(self):
		"""
		@return: list of L{Level} objects. The first element is a level 
			corresponding to the root node, the last one corresponds to
			leafs level.
		"""
		raise NotImplementedError