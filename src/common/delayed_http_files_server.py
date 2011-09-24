import sys
import os
import threading
import SocketServer
import time
import SimpleHTTPServer


class DelayedHTTPFilesServer:
	"""
	HTTP Files server with a new thread created for each new connection.
	Execution of work of each thread is delayed by a given amount of time.
	"""

	def __init__(self, directory_to_serve, delay, host="localhost", port_no=0):
		"""
		@param directory_to_serve: directory which will be served
		@param delay: delay time of serving each page in seconds
		@param host: server's host address
		@param port_no: number of port to listen on. Port C{0} means that
			the server will use an arbitrary unused port.
		"""
		self.__dir_to_serve = directory_to_serve
		self.__delay = delay
		self.__host = host
		self.__port_no = port_no
		self.__server = None
		self.__server_thread = None

	def start(self):
		"""
		Start the server in a new thread.
		
		@return: server's (IP address, port number) pair
		"""
		self.__server = _ThreadedTCPServer(
			self.__delay, self.__dir_to_serve, 
			(self.__host, self.__port_no), _DelayedFilesServerHandler)
		
		self.__server_thread = threading.Thread(
			target=self.__server.serve_forever)
		self.__server_thread.setDaemon(True)
		self.__server_thread.start()
		return self.__server.server_address
	
	def stop(self):
		"""
		Stop the server and wait until it shuts down
		"""
		self.__server.shutdown()
		self.__server_thread.join()
		self.__server = None
		self.__server_thread = None

	def __enter__(self):
		return self
	
	def __exit__(self, type_, value, traceback):
		self.stop()

class _DelayedFilesServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def handle(self):
		time.sleep(self.server.delay)
		old_wd = os.getcwd()
		os.chdir(self.server.dir_to_serve)
		SimpleHTTPServer.SimpleHTTPRequestHandler.handle(self)
		os.chdir(old_wd)
	
	## Override the standard implementation that prints to sys.stderr and
	## print to sys.stdout instead
	def log_message(self, format_, *args):
			sys.stdout.write("{} - - [{}] {}\n".format(
				self.address_string(), self.log_date_time_string(),	
				format_%args))

class _ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	def __init__(self, delay, dir_to_serve, (host, port), my_TCP_handler):
		SocketServer.TCPServer.__init__(self, (host, port), my_TCP_handler)
		self.delay = delay
		self.dir_to_serve = dir_to_serve