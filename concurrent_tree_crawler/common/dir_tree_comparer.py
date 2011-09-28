import filecmp
import os.path

def are_dir_trees_equal(dir1, dir2, ignore=None):
	"""
	Compare two directories recursively. Files in each directory are
	assumed to be equal if their names and contents are equal.

	@param dir1: First directory path
	@param dir2: Second directory path
	@param ignore: list of names to ignore (none are ignored by default)

	@return: True if the directory trees are the same and 
		there were no errors while accessing the directories or files, 
		False otherwise.
	"""
	dirs_cmp = filecmp.dircmp(dir1, dir2, ignore=ignore)
	if len(dirs_cmp.left_only)>0 or len(dirs_cmp.right_only)>0 or \
		len(dirs_cmp.funny_files)>0:
		return False
	(_, mismatch, errors) =  filecmp.cmpfiles(
		dir1, dir2, dirs_cmp.common_files, shallow=False)
	if len(mismatch)>0 or len(errors)>0:
		return False
	for common_dir in dirs_cmp.common_dirs:
		new_dir1 = os.path.join(dir1, common_dir)
		new_dir2 = os.path.join(dir2, common_dir)
		if not are_dir_trees_equal(new_dir1, new_dir2, ignore=ignore):
			return False
	return True