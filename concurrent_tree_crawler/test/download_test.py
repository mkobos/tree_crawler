#import sys
import unittest
#import os.path
import time
import logging

#from concurrent_tree_crawler.common.logger import Logger
from concurrent_tree_crawler.common.resources import Resources
from concurrent_tree_crawler.common.dir_tree_comparer import are_dir_trees_equal
from concurrent_tree_crawler.common.tempdir import TempDir
from concurrent_tree_crawler.common.delayed_http_files_server import \
	DelayedHTTPFilesServer
from concurrent_tree_crawler.common.threads.token_bucket import \
	TokenBucketFiller, StandardTokenBucket
from concurrent_tree_crawler.test.subtrees_comparer import subtrees_equal

from concurrent_tree_crawler.crawlers_manager import CrawlersManager
from concurrent_tree_crawler.html_multipage_navigator.tree_navigator import \
	HTMLMultipageNavigator
from concurrent_tree_crawler.tree_accessor import TreeAccessor
from concurrent_tree_crawler.standard_node import StandardNode
from concurrent_tree_crawler.html_multipage_navigator.sample_page_analyzer \
	import LevelsCreator
from concurrent_tree_crawler.html_multipage_navigator.web_browser import \
	MechanizeBrowserCreator
from concurrent_tree_crawler.html_multipage_navigator.throttled_web_browser \
	import ThrottledWebBrowserCreator
from concurrent_tree_crawler.crawler_thread import CrawlerThread
from concurrent_tree_crawler.navigator_tree_wrapper import NavigatorTreeWrapper
from concurrent_tree_crawler.abstract_node import NodeState
from concurrent_tree_crawler.multithreaded_crawler import MultithreadedCrawler

class DownloadTestCase(unittest.TestCase):
	def test_single_threaded_download_without_manager(self):
#		temp_dir = TempDir(os.path.expanduser("~/tmp"), prefix="dfs_crawler-")
#		try:
		with TempDir() as temp_dir:
			levels = LevelsCreator(temp_dir.get_path()).create()
			address = "file:"+\
				Resources.path(__file__, "data/original_site/issues_1.html",
							convert_to_url=True)
			tree = TreeAccessor(_StandardNodeExtended())
			navigator = HTMLMultipageNavigator(address, levels)
			navigator_wrapper = _NavigatorTreeWrapperExtended(navigator, tree)
			crawler = CrawlerThread(navigator_wrapper, tree)
			crawler.run()
			expected_dir = Resources.path(__file__, "data/expected_download")
			actual_dir = temp_dir.get_path()
			self.assert_(are_dir_trees_equal(expected_dir, actual_dir, 
					ignore=[".gitignore"]))
			self.__check_tree_final_state(tree.get_root())
			self.__check_if_each_node_is_processed_once(
				tree.get_root(), {"/root/2011-07-16/06": 0})
#		finally:
#			pass
	
	def test_multithreaded_download(self):
		address = "file:"+\
			Resources.path(__file__, "data/original_site/issues_1.html",
						convert_to_url=True)
		for threads_no in [1, 2, 3, 4, 50]:
			self.__check_download(threads_no, address)
	
	def test_throttled_download(self):
#		Logger.start(logging_level=logging.DEBUG)
		address = "file:"+\
			Resources.path(__file__, "data/original_site/issues_1.html",
						convert_to_url=True)
		web_pages_no = 34
		max_page_opens_per_second = 15
		min_seconds_taken = float(web_pages_no)/max_page_opens_per_second
		for threads_no in [1, 3]:
			seconds_taken = self.__check_download(
				threads_no, address, max_page_opens_per_second)
#			print >>sys.stderr, "seconds_taken={}".format(seconds_taken)
			self.assertGreaterEqual(seconds_taken, min_seconds_taken)
#		Logger.stop()

	def test_throttled_download_with_HTTP_server(self):
#		Logger.start(logging_level=logging.DEBUG)
		with DelayedHTTPFilesServer(
				Resources.path(__file__, "data/original_site"), 0) as server:
			(address, ip_number) = server.start()
			root_address = "http://{}:{}/issues_1.html".format(
				address, ip_number)
			web_pages_no = 34
			max_page_opens_per_second = 15
			min_seconds_taken = float(web_pages_no)/max_page_opens_per_second
			for threads_no in [1, 3]:
				seconds_taken = self.__check_download(
					threads_no, root_address, max_page_opens_per_second)
#				print >>sys.stderr, "seconds_taken={}".format(seconds_taken)
				self.assertGreaterEqual(seconds_taken, min_seconds_taken)
#		Logger.stop()

	def test_multithreaded_download_speedup_with_slow_HTTP_server(self):
#		Logger.start(logging_level=logging.DEBUG)
		with DelayedHTTPFilesServer(
				Resources.path(__file__, "data/original_site"), 0.1) as server:
			(address, ip_number) = server.start()
			root_address = "http://{}:{}/issues_1.html".format(
				address, ip_number)
			time_taken = []
			threads_no_list = [1, 4]
			for threads_no in threads_no_list:
				run_time = self.__check_download(threads_no, root_address)
				time_taken.append(run_time)
			assert_str = "{} threads time taken: {}s while "\
				"{} threads time taken: {}s".format(
					threads_no_list[0], time_taken[0],
					threads_no_list[1], time_taken[1])
			min_speedup = 1
			## We're expecting at some speedup. The speedup
			## is not fully deterministic and depends e.g. on processor load
			self.assert_(time_taken[0] > min_speedup*time_taken[1], assert_str)
#		Logger.stop()

	def __check_download(self,
			threads_no, address, max_page_opens_per_second=None):
		"""@return: run time in seconds"""
#		temp_dir = TempDir(os.path.expanduser("~/tmp"), prefix="dfs_crawler-")
#		try:
		with TempDir() as temp_dir:
			token_filler = None
			browser_creator = None
			if max_page_opens_per_second is not None:
				token_bucket = None
				token_bucket = StandardTokenBucket(max_page_opens_per_second)
				token_filler = TokenBucketFiller(token_bucket, 1, 
					max_page_opens_per_second)
				token_filler.start()
				browser_creator = ThrottledWebBrowserCreator(
					MechanizeBrowserCreator(), token_bucket)
			else:
				browser_creator = MechanizeBrowserCreator()
			
			navigators = []
			for _ in xrange(threads_no):
				navigators.append(HTMLMultipageNavigator(address,
					LevelsCreator(temp_dir.get_path()).create(), 
					browser_creator))
			sentinel = _StandardNodeExtended()
			crawler = _MultithreadedCrawlerExtended(navigators, sentinel)
			start = time.time()
			crawler.run()
			end = time.time()
			expected_dir = Resources.path(__file__, "data/expected_download")
			actual_dir = temp_dir.get_path()
			self.assert_(are_dir_trees_equal(expected_dir, actual_dir, 
					ignore=[".gitignore"]))
			self.__check_tree_final_state(sentinel.get_child("root"))
			self.__check_if_each_node_is_processed_once(
				sentinel.get_child("root"), {"/root/2011-07-16/06": 0})
			if max_page_opens_per_second is not None:
				token_filler.stop()
			return end - start
#		finally:
#			print >>sys.stderr, "Temp Dir path =\"{}\"".format(temp_dir.get_path())

	def __check_tree_final_state(self, root):
		t = ("root", NodeState.ERROR,
				[("2011-07-12", NodeState.CLOSED, 
					[("01", NodeState.CLOSED, []),
					("02", NodeState.CLOSED, []),
					("03", NodeState.CLOSED, []),
					("04", NodeState.CLOSED, []),
					("05", NodeState.CLOSED, []),
					("06", NodeState.CLOSED, []),
					("07", NodeState.CLOSED, []),
					("08", NodeState.CLOSED, [])]
				),
				("2011-07-13", NodeState.CLOSED, 
					[("01", NodeState.CLOSED, [])]
				),
				("2011-07-14", NodeState.CLOSED, []),
				("2011-07-16", NodeState.ERROR, 
					[("01", NodeState.CLOSED, []),
					("02", NodeState.CLOSED, []),
					("03", NodeState.ERROR, []),
					("04", NodeState.CLOSED, []),
					("05", NodeState.CLOSED, []),
					("06", NodeState.ERROR, []),
					("07", NodeState.CLOSED, [])]
				),
				("2011-07-16-repetition_1", NodeState.CLOSED, 
					[("01", NodeState.CLOSED, []),
					("02", NodeState.CLOSED, []),
					("03", NodeState.CLOSED, [])]
				),
				("2011-07-17", NodeState.ERROR, [])]
			)
		self.assert_(subtrees_equal(t, root))
	
	def __check_if_each_node_is_processed_once(self, root, exception_nodes):
		self.__check_if_each_node_in_subtree_is_processed_once("/root", root, 
			exception_nodes)
	
	def __check_if_each_node_in_subtree_is_processed_once(self, path, node, 
														exception_nodes):
		expected_count = 1
		if path in exception_nodes:
			expected_count = exception_nodes[path]
		assert isinstance(node, _StandardNodeExtended)
		self.assertEqual(expected_count, node.processed_times)
		children_names = [ch.get_name() for ch in node.get_children()]
		for child_name in children_names:
			child = node.get_child(child_name)
			child_path = path + "/" + child_name
			self.__check_if_each_node_in_subtree_is_processed_once(child_path, 
				child, exception_nodes)

class _StandardNodeExtended(StandardNode):
	def __init__(self, parent=None, name="sentinel", state=NodeState.OPEN):
		StandardNode.__init__(self, parent=parent, name=name, state=state)
		self.processed_times = 0
	
	def add_child(self, name, state):
		assert name not in self._children[state]
		new_child = _StandardNodeExtended(self, name, state)
		self._children[state][name] = new_child
		return new_child

class _NavigatorTreeWrapperExtended(NavigatorTreeWrapper):
	def __init__(self, navigator, tree):
		NavigatorTreeWrapper.__init__(self, navigator, tree)
	
	def process_node_and_check_if_is_leaf(self):
		self.get_current_node().processed_times += 1
		return NavigatorTreeWrapper.process_node_and_check_if_is_leaf(self)

class _MultithreadedCrawlerExtended(MultithreadedCrawler):
		def __init__(self, navigators, sentinel, activity_schedule=None,  
			log_file_path=None, state_file_path=None, save_period=None,
			logging_level=logging.ERROR):
			MultithreadedCrawler.__init__(self, navigators, sentinel, 
				activity_schedule, log_file_path, state_file_path, 
				save_period, logging_level)

		def _create_crawlers_manager(self, tree, navigators):
			navigator_wrappers = []
			for navigator in navigators:
				navigator_wrapper = \
					_NavigatorTreeWrapperExtended(navigator, tree)
				navigator_wrappers.append(navigator_wrapper)
			return CrawlersManager(tree, navigator_wrappers)