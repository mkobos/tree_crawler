import unittest

from common.resources import Resources
from common.dir_tree_comparer import are_dir_trees_equal

from crawler.simple_dfs_crawler import SimpleDFSCrawler
from crawler.html_multipage_navigator.tree_navigator import \
	HTMLMultipageNavigator
from crawler.html_multipage_navigator.sample_page_analyzer import \
	PageAnalyzerFactory
from common.tempdir import TempDir

class SimpleDFSCrawlerTestCase(unittest.TestCase):
	def test_website_download(self):
		with TempDir() as temp_dir:
			analyzer_factory = PageAnalyzerFactory(temp_dir.get_path())
			address = "file://"+Resources.path(__file__, 
				"data/original_site-without_broken_links/issues_1.html")
			navigator = HTMLMultipageNavigator(analyzer_factory, address)
			crawler = SimpleDFSCrawler(navigator)
			crawler.run()
			expected_dir = Resources.path(__file__, 
				"data/expected_download-without_broken_links")
			actual_dir = temp_dir.get_path()
			self.assert_(are_dir_trees_equal(expected_dir, actual_dir))
