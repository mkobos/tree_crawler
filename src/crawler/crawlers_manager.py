import Queue
from crawler.crawler_thread import CrawlerThread

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
		@type navigators: list of L{AbstractTreeNavigator}s
		"""
		self.__tree = tree
		self.__status_queue = Queue.Queue()
		self.__threads = []
		for navigator in navigators:
			crawler = CrawlerThread(navigator, tree, self.__status_queue)
			self.__threads.append(crawler)
	
	def start(self):
		assert len(self.__threads) > 0, "No threads available"
		for t in self.__threads:
			t.setDaemon(True)
			t.start()

	def stop(self):
		for t in self.__threads:
			t.stop_activity()
		self.wait_until_finish()
	
	def wait_until_finish(self):
		try:
			for _ in xrange(len(self.__threads)):
				ex_info = self.__status_queue.get()
				if ex_info is not None:
					raise CrawlersManagerException(ex_info[1])
		finally:
			del self.__threads[:]