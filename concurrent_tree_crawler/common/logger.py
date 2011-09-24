import logging
import sys

class Logger:
	__default_root_log_level = logging.WARNING
	__console_h = None
	__file_h = None

	@staticmethod
	def start(stream = sys.stderr, file_path = None, 
		logging_level = logging.WARNING,
		format_ = '%(asctime)s %(levelname)s %(message)s'):
		"""@param stream: output stream where logs are written. If C{None}, 
			logs are not written to any stream.
			@param file_path: if it is not C{None}, logging messages are written
			not only to the stream, but to the specified file as well.
			@param logging_level: logging level accepted by logging devices"""
		## Not used version with non-default formatting
		#datefmt = "%Y-%m-%d %H:%M:%S"
		#formatter = logging.Formatter(format), datefmt)
		
		formatter = logging.Formatter(format_)
		
		root_logger = logging.getLogger("")
		root_logger.setLevel(logging_level)
		
		
		if stream is not None:
			Logger.__console_h = logging.StreamHandler(stream)
			Logger.__console_h.setLevel(logging_level)
			Logger.__console_h.setFormatter(formatter)
			root_logger.addHandler(Logger.__console_h)
		if file_path is not None:
			Logger.__file_h = logging.FileHandler(file_path)
			Logger.__file_h.setLevel(logging_level)
			Logger.__file_h.setFormatter(formatter)
			root_logger.addHandler(Logger.__file_h)
			
	@staticmethod
	def stop():
		"""Set the default values in the logging system"""
		root_logger = logging.getLogger()
		if Logger.__console_h is not None:
			root_logger.removeHandler(Logger.__console_h)
			Logger.__console_h.close()
		if Logger.__file_h is not None:
			root_logger.removeHandler(Logger.__file_h)
			Logger.__file_h.close()
		root_logger.setLevel(Logger.__default_root_log_level)