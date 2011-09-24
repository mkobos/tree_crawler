import mechanize

class AbstractWebBrowser:
	"""An abstract functionality of a web browser"""
	
	def open(self, address):
		"""Open a web page with a given address"""
		raise NotImplementedError
	
	def response(self):
		"""
		Return a copy of the currently opened web page

		@rtype: file-like object
		"""
		raise NotImplementedError
	
	def back(self, steps=1):
		"""Go back C{steps} steps in history"""
		raise NotImplementedError

class AbstractWebBrowserCreator:
	"""The 'Creator' class from the Factory Method design pattern"""
	
	def create(self):
		"""
		Create a browser. This method has to be thread-safe since it is 
		called as the method of the same object in different threads.
		
		@rtype: L{AbstractWebBrowser}
		"""
		raise NotImplementedError


class MechanizeBrowser(AbstractWebBrowser):
	"""The default browser. It uses C{mechanize} library"""

	def __init__(self):
		self.__br = mechanize.Browser()
	
	def open(self, address):
		self.__br.open(address) #PyLint ignore unneeded warning: IGNORE:E1102
	
	def response(self):
		return self.__br.response() #PyLint ignore unneeded warning: IGNORE:E1102
	
	def back(self, steps=1):
		self.__br.back(steps) #PyLint ignore unneeded warning: IGNORE:E1102

class MechanizeBrowserCreator(AbstractWebBrowserCreator):
	def create(self):
		return MechanizeBrowser()