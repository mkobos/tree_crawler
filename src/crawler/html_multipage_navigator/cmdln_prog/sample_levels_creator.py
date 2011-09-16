from crawler.html_multipage_navigator.cmdln_prog.abstract_levels_creator \
	import AbstractCmdLnLevelsCreator
from crawler.html_multipage_navigator.sample_page_analyzer import LevelsCreator
from common.file_helper import lenient_makedir

class SampleCmdLnLevelsCreator(AbstractCmdLnLevelsCreator):
	def fill_parser(self, parser):
		parser.add_argument("destination_dir",
			help="directory where the downloaded pages will be saved.")
	
	def create(self, args):
		lenient_makedir(args.destination_dir)
		return LevelsCreator.create(args.destination_dir)