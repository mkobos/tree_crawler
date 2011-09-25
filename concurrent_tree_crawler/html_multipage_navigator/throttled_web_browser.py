from concurrent_tree_crawler.html_multipage_navigator.web_browser import \
	AbstractWebBrowser, AbstractWebBrowserCreator

class ThrottledWebBrowserWrapper(AbstractWebBrowser):
	def __init__(self, browser, token_bucket):
		"""
		@type browser: L{AbstractWebBrowser}
		@type token_bucket: L{TokenBucket}
		"""
		self.__br = browser
		self.__token_bucket = token_bucket		
	
	def open(self, address):
		self.__token_bucket.get_token()
		self.__br.open(address)
	
	def response(self):
		return self.__br.response()
	
	def back(self, steps=1):
		self.__br.back(steps)

class ThrottledWebBrowserCreator(AbstractWebBrowserCreator):
	def __init__(self, browser_creator, token_bucket):
		"""
		@param browser_creator: a creator of browsers that will be throttled
		@type browser_creator: L{AbstractWebBrowserCreator}
		@type token_bucket: L{TokenBucket}
		"""
		self.__browser_creator = browser_creator
		self.__token_bucket = token_bucket
	
	def create(self):
		bare_browser = self.__browser_creator.create()
		return ThrottledWebBrowserWrapper(bare_browser, self.__token_bucket)