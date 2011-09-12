import threading

class LockProtectedVariable:
	"""A single object with access protected by a threading lock"""
	
	def __init__(self, value):
		self.__val = value
		self.__lock = threading.Lock()
	
	def get(self):
		self.__lock.acquire()
		val = self.__val
		self.__lock.release()
		return val
	
	def set(self, value):
		self.__lock.acquire()
		self.__val = value
		self.__lock.release()