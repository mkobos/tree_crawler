import threading
import os.path
import shutil

from concurrent_tree_crawler.common.tempdir import TempDir
from concurrent_tree_crawler.common.threads.sleep import Sleep
from concurrent_tree_crawler.xml_tree_serialization import XMLTreeWriter

class TreeSaverThread(threading.Thread):	
	def __init__(self, dst_file_path, tree, sleep_time):
		"""
		@param sleep_time: sleep time between tree saves in seconds
		@type tree: L{RWLockTreeAccessor}
		"""
		threading.Thread.__init__(self)
		self.__path = dst_file_path
		self.__tree = tree
		self.__sleep_time = sleep_time
		self.__should_stop = False
		self.__sleep = Sleep()

	def run(self):
		while not self.__should_stop:
			self.__sleep.sleep(self.__sleep_time)
			with TempDir() as temp_dir:
				tmp_file_path = os.path.join(temp_dir.get_path(), "tree.xml")
				with open(tmp_file_path, "w") as tmp_f:
					writer = XMLTreeWriter(tmp_f)
					self.__tree.get_lock().writer_acquire()
					try:
						sentinel = self.__tree.get_sentinel()
						writer.write(sentinel)
					finally:
						self.__tree.get_lock().writer_release()
				shutil.copyfile(tmp_file_path, self.__path)
	
	def stop_activity(self):
		self.__should_stop = True
		self.__sleep.wake_up()