import unittest
import os.path

from concurrent_tree_crawler.common.dir_tree_comparer import are_dir_trees_equal
from concurrent_tree_crawler.common.resources import Resources

class DirTreeComparerTestCase(unittest.TestCase):
	def test_equal_dir_trees(self):
		self.__check("equal_dir_trees", True)

	def test_additional_dir(self):
		self.__check("additional_dir", False)
	
	def test_additional_file(self):
		self.__check("additional_file", False)
	
	def test_missing_dir(self):
		self.__check("missing_dir", False)

	def test_missing_file(self):
		self.__check("missing_file", False)

	def test_one_byte_different_in_one_file(self):
		self.__check("one_byte_different_in_one_file", False)
	
	def __check(self, dir_name, should_be_equal):
		path = Resources.path(__file__, 
			os.path.join("data/dir_tree_comparer", dir_name))
		ret = are_dir_trees_equal(
			os.path.join(path, "01"), 
			os.path.join(path, "02"))
		if should_be_equal:
			self.assertTrue(ret)
		else:
			self.assertFalse(ret)