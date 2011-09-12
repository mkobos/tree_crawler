import sys
import threading
import Queue

class ExThread(threading.Thread):
	"""A thread that can throw an exception to the joining thread."""
	
	def __init__(self, status_queue = None):
		"""@type status_queue: L{Queue.Queue} or C{None}"""
		threading.Thread.__init__(self)
		self.__status_queue = status_queue
		if self.__status_queue is None:
			self.__status_queue = Queue.Queue()
	
	def run_with_exception(self):
		"""This method should be overriden."""
		raise NotImplementedError

	def run(self):
		"""This method should NOT be overriden."""
		try:
			self.run_with_exception()
		except Exception:
			self.__status_queue.put(sys.exc_info())
		self.__status_queue.put(None)
	
	def wait_for_exc_info(self):
		return self.__status_queue.get()
	
	def join_with_exception(self):
		ex_info = self.wait_for_exc_info()
		if ex_info is None:
			return
		else:
			raise ex_info[1]