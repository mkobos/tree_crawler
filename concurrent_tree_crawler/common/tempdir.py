import shutil
import tempfile

class TempDir:
	def __init__(self, parent_dir=None, prefix="", suffix=""):
		self.__path = tempfile.mkdtemp(
			dir=parent_dir, prefix=prefix, suffix=suffix)

	def get_path(self):
		return self.__path

	def delete(self):
		shutil.rmtree(self.__path)

	def __enter__(self):
		return self
	
	def __exit__(self, type_, value, traceback):
		self.delete()
