import argparse
from concurrent_tree_crawler.html_multipage_navigator.sample_page_analyzer import LevelsCreator

class AbstractCmdLnLevelsCreator:
	def fill_parser(self, parser):
		"""
		Fill the given parser object with command-line arguments needed to
		initialize levels creator returned in L{create} method.

		@type parser: L{argparse.ArgumentParser}
		"""
		pass
	
	def create(self, args):
		"""
		Create L{AbstractLevelsCreator} based on command line arguments.
		
		@param args: result of calling the C{parser.parse_args()} function. 
			Contains result of parsing the arguments defined in L{fill_parser}
			method.
		@type args: L{argparse.Namespace}
		@rtype: L{AbstractLevelsCreator}
		"""
		raise NotImplementedError()

	def on_exit(self):
		"""
		This method is called before the program exit. 
		This is the place to execute some cleanup actions.
		"""
		pass