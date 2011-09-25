import os

def lenient_makedir(dir_path):
	"""Create given directory path if it doesn't already exist"""
	if not os.access(dir_path, os.F_OK):
		os.makedirs(dir_path)