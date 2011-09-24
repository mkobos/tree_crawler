import os.path
from pkg_resources import resource_stream

class Resources:
	@staticmethod
	def open(_name_, relative_file_path):
		"""Safe way of accessing the resource file (it will work even in
			code enclosed in *.egg/*.zip package)
		
			@param _name_: C{__name__} variable (of the calling module)
			@return: file-like object"""
		
		return resource_stream(_name_, relative_file_path)
	
	@staticmethod
	def path(_file_, relative_path):
		"""*Unsafe* way of getting path to a resource (dir/file) - it won't 
			work inside code enclosed in *.egg/*.zip package
			
			@param _file_: C{__file__} variable of calling module
			@return: absolute-like path to given resource"""
		
		return os.path.join(os.path.dirname(_file_), relative_path)
