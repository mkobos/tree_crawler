import argparse

class AbstractCmdLnNavigatorsCreator:
	def fill_parser(self, parser):
		"""
		Fill the given parser object with command-line arguments needed to
		initialize navigators which are created in L{create} method.

		@type parser: L{argparse.ArgumentParser}
		"""
		raise NotImplementedError()
	
	def create(self, args, navigators_count):
		"""
		Create navigators based on arguments from command-line.
		
		@param args: result of calling the C{parser.parse_args()} function. 
			Contains results of parsing of the arguments defined in 
			L{fill_parser} method.
		@type args: L{argparse.Namespace}
		@param navigators_count: number of L{AbstractTreeNavigator}s to create
		@return: navigators that will be used by the crawler threads. 
			Each navigator will be used by a single thread.
		@rtype: list of L{AbstractTreeNavigator}s
		"""
		raise NotImplementedError()

	def on_exit(self):
		"""
		This method is called before the program exit. 
		This is the place to do some cleanup.
		"""
		raise NotImplementedError()