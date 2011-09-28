import unittest
from concurrent_tree_crawler.common.resources import Resources
from concurrent_tree_crawler.html_multipage_navigator.tree_navigator import \
	HTMLMultipageNavigator
from concurrent_tree_crawler.html_multipage_navigator.sample_page_analyzer \
	import *

class HTMLMultipageNavigatorTestCase(unittest.TestCase):
	def test_simple_browsing(self):
		navigator = HTMLMultipageNavigator("file:"+Resources.path(__file__, 
			"../../test/data/original_site/issues_1.html", convert_to_url=True),
			LevelsCreator(None).create())
		navigator.start_in_root()
		root_name = navigator.get_path()[0]
		children1 = navigator.get_children()
		self.assertEqual(["2011-07-12", "2011-07-13", "2011-07-14", 
			"2011-07-16", "2011-07-16-repetition_1", "2011-07-17"], children1) 
		navigator.move_to_child(children1[0])
		self.assertEqual([root_name, "2011-07-12"], navigator.get_path())
		children2 = navigator.get_children()
		self.assertEqual(["01", "02", "03", "04", "05", "06", "07", "08"], 
						children2)
		navigator.move_to_child("05")
		self.assertEqual([root_name, "2011-07-12", "05"], navigator.get_path())
		navigator.move_to_parent()
		self.assertEqual([root_name, "2011-07-12"], navigator.get_path())
		navigator.move_to_parent()
		self.assertEqual([root_name], navigator.get_path())
