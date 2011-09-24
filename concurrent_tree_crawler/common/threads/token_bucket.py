import threading
import logging

from concurrent_tree_crawler.common.threads.sleep import Sleep

class TokenBucket:
	"""Interface of a token bucket"""
	
	def get_token(self):
		"""Remove single token from the bucket"""
		raise NotImplementedError
	
	def put_tokens(self, no):
		"""
		@param no: number of tokens to add to the bucket
		"""
		raise NotImplementedError

class InfiniteTokenBucket(TokenBucket):
	"""Token bucket with an infinite supply of tokens"""

	def get_token(self):
		pass
	
	def put_tokens(self, no):
		pass

class StandardTokenBucket(TokenBucket):
	def __init__(self, token_capacity):
		self.__token_capacity = token_capacity
		self.__cond = threading.Condition()
		self.__tokens_no = 0
	
	def get_token(self):
		self.__cond.acquire()
		while not self.__tokens_no>0:
			self.__cond.wait()
		self.__tokens_no = self.__tokens_no-1
		self.__cond.release()
	
	def put_tokens(self, no):
		self.__cond.acquire()
		self.__tokens_no = min(self.__tokens_no+no, self.__token_capacity)
		self.__cond.notifyAll()
		self.__cond.release()
		
class TokenBucketFiller(threading.Thread):
	"""This thread fills the token bucket every C{fill_interval_in_secs} seconds 
		with C{fill_amount} number of tokens."""

	def __init__(self, bucket, fill_interval_in_secs, fill_amount):
		"""
		@type bucket: L{TokenBucket}
		"""
		threading.Thread.__init__(self)
		self.__bucket = bucket
		self.__fill_interval = fill_interval_in_secs
		self.__fill_amount = fill_amount
		self.__should_stop = False
		self.__sleep = Sleep()
		
	def run(self):
		try:
			while not self.__should_stop:
				self.__bucket.put_tokens(self.__fill_amount)
				self.__sleep.sleep(self.__fill_interval)
		except Exception as ex:
			logging.error('In TokenBucketFiller, an exception was caught: '
				'"{}"'.format(str(ex)))
	
	## HACK: in this implementation there is a very rare situation that would
	## lead to taking up to '__fill_interval' seconds to completely stop 
	## this thread.
	def stop(self):
		self.__should_stop = True
		self.__sleep.wake_up()
		self.join()