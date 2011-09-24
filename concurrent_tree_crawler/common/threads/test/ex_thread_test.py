import unittest
import threading
from concurrent_tree_crawler.common.threads.ex_thread import ExThread

class MyException(Exception):
	pass

class MyThread(ExThread):
	def __init__(self):
		ExThread.__init__(self)
	
	def run_with_exception(self):
		thread_name = threading.current_thread().name
		raise MyException("An error in thread '{}'.".format(thread_name))

class ExThreadTestCase(unittest.TestCase):
	def test_basic(self):
		t = MyThread()
		t.start()
		self.assertRaises(MyException, t.join_with_exception)
