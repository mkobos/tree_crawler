from concurrent_tree_crawler.html_multipage_navigator.cmdln.abstract_levels_creator \
	import AbstractCmdLnLevelsCreator
from concurrent_tree_crawler.html_multipage_navigator.sample_page_analyzer \
	import LevelsCreator
from concurrent_tree_crawler.common.file_helper import lenient_makedir

class SampleCmdLnLevelsCreator(AbstractCmdLnLevelsCreator):
	def fill_parser(self, parser):
		parser.add_argument("destination_dir",
			help="directory where the downloaded pages will be saved.")
	
	def create(self, args):
		lenient_makedir(args.destination_dir)
		return LevelsCreator(args.destination_dir).create()
