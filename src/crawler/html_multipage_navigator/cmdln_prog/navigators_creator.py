from crawler.html_multipage_navigator.web_browser import MechanizeBrowserCreator
from crawler.html_multipage_navigator.throttled_web_browser import \
	ThrottledWebBrowserCreator
from common.threads.token_bucket import TokenBucketFiller, StandardTokenBucket
from crawler.html_multipage_navigator.tree_navigator import \
	HTMLMultipageNavigator
from crawler.html_multipage_navigator.sample_page_analyzer import LevelsCreator
from crawler.abstract_cmdln_navigators_creator import \
	AbstractCmdLnNavigatorsCreator
from crawler.html_multipage_navigator.cmdln_prog.abstract_levels_creator \
	import AbstractCmdLnLevelsCreator

class CmdLnNavigatorsCreator(AbstractCmdLnNavigatorsCreator):
	def __init__(self, levels_creator):
		"""@type levels_creator: L{AbstractCmdLnLevelsCreator}"""
		self.__token_filler = None
		self.__levels_creator = levels_creator
	
	def fill_parser(self, parser):
		parser.add_argument("source_addres", 
			help="the address of the web site to crawl.")
		parser.add_argument("destination_dir",
			help="directory where the downloaded pages will be saved.")
		parser.add_argument("--max_pages_per_second", type=float, 
			help="Maximal number of web pages downloads per second. "\
				"By default no limit is imposed.")
		self.__levels_creator.fill_parser(parser)
	
	def create(self, args, navigators_count):
		browser_creator = self.__get_browser_creator_and_start_token_filler(
			args.max_pages_per_second)
		navigators = []
		for _ in range(navigators_count):
			navigators.append(
				HTMLMultipageNavigator(args.source_address, 
					self.__levels_creator.create(args), 
					browser_creator))
		return navigators

	def __get_browser_creator_and_start_token_filler(self, 
			max_pages_per_second):
		self.__token_filler = None
		browser_creator = None
		if max_pages_per_second is not None:
			token_bucket = StandardTokenBucket(max_pages_per_second)
			browser_creator = ThrottledWebBrowserCreator(
				self._create_browser_creator(), token_bucket)
			self.__token_filler = TokenBucketFiller(
				token_bucket, 1, max_pages_per_second)
			self.__token_filler.start()
		else:
			browser_creator = self._create_browser_creator()
		return browser_creator
	
	def _create_browser_creator(self):
		"""
		It is possible to override this function to use a different 
			C{AbstractWebBrowserCreator}.
		
		@rtype: C{AbstractWebBrowserCreator}
		"""  
		return MechanizeBrowserCreator()

	def on_exit(self):
		if self.__token_filler is not None:
			self.__token_filler.stop()
		self.__levels_creator.on_exit()