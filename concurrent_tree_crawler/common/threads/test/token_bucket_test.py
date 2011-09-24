import unittest
import time
import threading
from concurrent_tree_crawler.common.threads.token_bucket import \
	StandardTokenBucket, TokenBucketFiller

class TokenBucketTestCase(unittest.TestCase):
	def test_get(self):
		bucket = StandardTokenBucket(1000)
		filler = TokenBucketFiller(bucket, 2, 3)
		ths = []
		threads_no = 2
		for i in xrange(threads_no):
			ths.append(_Incrementor(bucket))
			ths[i].start()
		filler.start()
		time.sleep(3)
		for i in xrange(threads_no):
			ths[i].order_stop()
		for i in xrange(threads_no):
			ths[i].join()
		filler.stop()
		results = []
		sum = 0
		for i in xrange(threads_no):
			results.append(ths[i].get_result())
			sum += results[i]
		self.assertEqual(8, sum)
		
class _Incrementor(threading.Thread):
	def __init__(self, bucket):
		threading.Thread.__init__(self)
		self.__bucket = bucket
		self.__stop_lock = threading.Lock()
		self.__stop = False
		self.__value = 0
		self.setDaemon(True)
	
	def run(self):
		while not self.__should_stop():
			self.__bucket.get_token()
			self.__value += 1
			
	def get_result(self):
		return self.__value
		
	def order_stop(self):
		self.__stop_lock.acquire()
		self.__stop = True
		self.__stop_lock.release()
		
	def __should_stop(self):
		self.__stop_lock.acquire()
		should_stop = self.__stop
		self.__stop_lock.release()
		return should_stop