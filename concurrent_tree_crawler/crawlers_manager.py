import Queue
import time
from concurrent_tree_crawler.crawler_thread import CrawlerThread

class CrawlersManagerException(Exception):
	pass

#	def __str__(self):
#		"An exception occurred in one of crawler threads: {}".format(self.__ex)

class CrawlersManager:
	"""Starts and stops different crawler threads"""
	
	def __init__(self, tree, navigators):
		"""
		@param tree: L{TreeAccessor} object to be used by all of the threads
		@type tree: L{TreeAccessor}
		@param navigators: navigators to be used by the threads. Each thread
			obtains a single navigator. Number of threads created is the same
			as the number of navigators.
		@type navigators: list of L{NavigatorTreeWrapper}s
		"""
		self.__tree = tree
		self.__navigators = navigators
		self.__status_queue = None
		self.__threads = None
	
	def start(self):
		assert len(self.__navigators) > 0, "No navigators available"
		self.__status_queue = Queue.Queue()
		self.__threads = []
		for navigator in self.__navigators:
			crawler = CrawlerThread(navigator, self.__tree, self.__status_queue)
			self.__threads.append(crawler)
		for t in self.__threads:
			t.setDaemon(True)
			t.start()

	def stop(self):
		for t in self.__threads:
			t.stop_activity()
		self.wait_until_finish()
	
	def wait_until_finish(self, timeout=None):
		"""
		Wait until all threads finished their jobs and then get rid of them. If
		C{timeout} seconds pass before the threads are finished, they are 
		stopped.
		
		@param timeout: if the value is not C{None}, the method 
			blocks at most for C{timeout} number of seconds, otherwise 
			the method blocks until all threads are finished.
		@return: C{False} iff the wait ended because of the timeout 
		"""
		try:
			for _ in xrange(len(self.__threads)):
				wait_start = time.time()
				ex_info = self.__status_queue.get(timeout=timeout)
				wait_end = time.time()
				if ex_info is not None:
					raise CrawlersManagerException(ex_info[1])
				if timeout is not None:
					timeout = timeout - (wait_end - wait_start)
					if timeout <= 0:
						raise Queue.Empty
			return True
		## Timeout exception
		except Queue.Empty as _:
			for t in self.__threads:
				t.stop_activity()
			for t in self.__threads:
				t.join()
			return False
		finally:
			del self.__threads[:]