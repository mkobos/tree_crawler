from crawler.html_multipage_navigator.web_browser import AbstractWebBrowser
from common.threads.token_bucket import TokenBucket

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