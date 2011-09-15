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

		@param page_file: file-like structure to be processed
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
		"""Name of the level. Example names: "book", "chapter", "section"."""

		self.page_analyzer = page_analyzer
		"""L{AbstractPageAnalyzer} object."""