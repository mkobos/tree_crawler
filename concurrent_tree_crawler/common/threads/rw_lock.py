import threading
#import time ##DEBUG
#import logging ##DEBUG

__author__ = "Mateusz Kobos"

"""
This code is a derivative of the code from ActiveState Code service at the address:
http://code.activestate.com/recipes/577803-reader-writer-lock-with-priority-for-writers
and is licensed under the MIT license.
"""

class RWLock:
	"""Synchronization object used in a solution of so-called second 
	readers-writers problem. In this problem, many readers can simultaneously 
	access a share, and a writer has an exclusive access to this share.
	Additionally, the following constraints should be met: 
		- no reader should be kept waiting if the share is currently opened for 
			reading unless a writer is also waiting for the share, 
		- no writer should be kept waiting for the share longer than absolutely 
			necessary. 
	
	The implementation is based on [1, secs. 4.2.2, 4.2.6, 4.2.7] 
	with a modification -- adding an additional lock (C{self.__readers_queue})
	-- in accordance with [2].
		
	Sources:
		1. A.B. Downey: "The little book of semaphores", Version 2.1.5, 2008
		2. P.J. Courtois, F. Heymans, D.L. Parnas:
			"Concurrent Control with 'Readers' and 'Writers'", 
			Communications of the ACM, 1971 (via [3])
		3. http://en.wikipedia.org/wiki/Readers-writers_problem
	"""
	
	def __init__(self):
		self.__read_switch = _LightSwitch()
		self.__write_switch = _LightSwitch()
		self.__no_readers = threading.Lock()
		self.__no_writers = threading.Lock()
		self.__readers_queue = threading.Lock()
		"""A lock giving an even higher priority to the writer in certain
		cases (see [2] for a discussion)"""
	
	def reader_acquire(self):
		##DEBUG
		#logging.info("thread={}: reader_acquire: BEGIN".format(threading.current_thread().name))
		self.__readers_queue.acquire()
		#logging.info("thread={}: reader_acquire: after readers_queue.acquire()".format(threading.current_thread().name))
		self.__no_readers.acquire()
		#logging.info("thread={}: reader_acquire: after no_readers.acquire()".format(threading.current_thread().name))
		self.__read_switch.acquire(self.__no_writers)
		#logging.info("thread={}: reader_acquire: after read_switch.acquire(self.__no_writers)".format(threading.current_thread().name))
		self.__no_readers.release()
		#logging.info("thread={}: reader_acquire: after no_readers.release()".format(threading.current_thread().name))
		self.__readers_queue.release()
		##DEBUG
		#logging.info("thread={}: reader_acquire: END".format(threading.current_thread().name))
	
	def reader_release(self):
		##DEBUG
		#logging.info("thread={}: reader_release: BEGIN".format(threading.current_thread().name))
		self.__read_switch.release(self.__no_writers)
		##DEBUG
		#logging.info("thread={}: reader_release: END".format(threading.current_thread().name))
	
	def writer_acquire(self):
		##DEBUG
		#logging.info("thread={}: writer_acquire: BEGIN".format(threading.current_thread().name))
		self.__write_switch.acquire(self.__no_readers)
		#logging.info("thread={}: writer_acquire: after write_switch.acquire(self.__no_readers)".format(threading.current_thread().name))
		self.__no_writers.acquire()
		##DEBUG
		#logging.info("thread={}: writer_acquire: END".format(threading.current_thread().name))
	
	def writer_release(self):
		##DEBUG
		#logging.info("thread={}: writer_release: BEGIN".format(threading.current_thread().name))
		self.__no_writers.release()
		self.__write_switch.release(self.__no_readers)
		##DEBUG
		#logging.info("{} thread={}: writer_release: END".format(threading.current_thread().name))
	

class _LightSwitch:
	"""An auxiliary "light switch"-like object. The first thread turns on the 
	"switch", the last one turns it off (see [1, sec. 4.2.2] for details)."""
	def __init__(self):
		self.__counter = 0
		self.__mutex = threading.Lock()
	
	def acquire(self, lock):
		self.__mutex.acquire()
		self.__counter += 1
		if self.__counter == 1:
			lock.acquire()
		self.__mutex.release()

	def release(self, lock):
		self.__mutex.acquire()
		self.__counter -= 1
		if self.__counter == 0:
			lock.release()
		self.__mutex.release()
