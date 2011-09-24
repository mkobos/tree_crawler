import threading

class Sleep:
	"""A counterpart of the C{time.sleep()} function. This implementation
	allows some thread to wake up the sleeping thread. 
	"""
	def __init__(self):
		self.__cond = threading.Condition()
	
	def sleep(self, seconds):
		self.__cond.acquire()
		self.__cond.wait(seconds)
		self.__cond.release()
	
	def wake_up(self):
		self.__cond.acquire()
		self.__cond.notifyAll()
		self.__cond.release()