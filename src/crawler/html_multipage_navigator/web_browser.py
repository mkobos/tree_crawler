import mechanize

class AbstractWebBrowser:
	def open(self, address):
		"""Open web page with given address"""
		raise NotImplementedError
	
	def response(self):
		"""Return a copy of the current response object"""
		raise NotImplementedError
	
	def back(self, steps=1):
		"""Go back C{steps} steps in history"""
		raise NotImplementedError

class MechanizeBrowser(AbstractWebBrowser):
	def __init__(self):
		self.__br = mechanize.Browser()
	
	def open(self, address):
		self.__br.open(address)
	
	def response(self):
		return self.__br.response()
	
	def back(self, steps=1):
		self.__br.back(steps)