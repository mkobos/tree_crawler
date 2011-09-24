import re
import shutil
import os.path
from xml.etree.ElementTree import ElementTree
from concurrent_tree_crawler.abstract_tree_navigator import NavigationException
from concurrent_tree_crawler.common.file_helper import lenient_makedir
from concurrent_tree_crawler.html_multipage_navigator.abstract_page_analyzer \
	import PageLinks, AbstractPageAnalyzer, Level, AbstractLevelsCreator

class PageAnalyzerException(NavigationException):
	pass

class MagazinePageAnalyzer(AbstractPageAnalyzer):
	"""A class that parses magazine-level pages"""
	
	def get_links(self, page_file, child_links_retrieved_so_far):
		children = []
		doc = ElementTree(file=page_file)
		links = doc.findall("body/div/div[@id='elements']/table/tr/td/a")
		for link in links:
			link_text = self.__convert_date(link.text)
			children.append((link_text, link.attrib["href"]))
		next_page_elem = \
			doc.find("body/div/div[@id='navigation']/table/tr/td[3]/a")
		next_page_link = None
		if next_page_elem is not None:
			next_page_link = next_page_elem.attrib["href"]
		return PageLinks(children, next_page_link)

	@staticmethod
	def __convert_date(text):
		months = {"January": 1, "February": 2, "March": 3, "April": 4,
			"May": 5, "June": 6, "July": 7, "August": 8, "September": 9,
			"October": 10, "November": 11, "December": 12}
		(month_str, day_str, year_str) = \
			re.match("^(\w+) (\d+), (\d+)$", text).group(1, 2, 3)
		month = _convert_to_2_digit_number(
			int(months[month_str]))
		day = _convert_to_2_digit_number(int(day_str))
		return "{}-{}-{}".format(year_str, month, day)

class IssuePageAnalyzer(AbstractPageAnalyzer):
	"""A class that parses issues-level pages"""

	def __init__(self, dst_dir_path):
		self.__dst_dir_path = dst_dir_path	

	def process(self, tree_path, page_file):
		assert len(tree_path) > 0
		dir_path = os.path.join(self.__dst_dir_path,
			_convert_tree_path_to_dir_path(tree_path))
		lenient_makedir(dir_path)
		error_page_path = os.path.join(dir_path, "error.txt")
		_handle_error_page(page_file, error_page_path)

	def get_links(self, page_file, child_links_retrieved_so_far):
		children = []
		doc = ElementTree(file=page_file)
		links = doc.findall("body/div/div[@id='elements']/table/tr/td/a")
		for i, link in enumerate(links):
			#link_text = self.__convert_title(link.text)
			link_text = _convert_to_2_digit_number(
				child_links_retrieved_so_far + i+1)
			children.append((link_text, link.attrib["href"]))
		next_page_elem = \
			doc.find("body/div/div[@id='navigation']/table/tr/td[3]/a")
		next_page_link = None
		if next_page_elem is not None:
			next_page_link = next_page_elem.attrib["href"]
		return PageLinks(children, next_page_link)

class ArticlePageAnalyzer(AbstractPageAnalyzer):
	"""A class that downloads article pages"""
	
	def __init__(self, dst_dir_path):
		self.__dst_dir_path = dst_dir_path

	def process(self, tree_path, page_file):
		assert len(tree_path) > 0
		dir_path = os.path.join(self.__dst_dir_path,
			_convert_tree_path_to_dir_path(tree_path[:-1]))
		lenient_makedir(dir_path)
		error_page_path = os.path.join(dir_path, tree_path[-1]+"-error.txt")
		_handle_error_page(page_file, error_page_path)
		file_path = os.path.join(dir_path, tree_path[-1]+".html")
		self.__download_page(page_file, file_path)

	def __download_page(self, page_file, dst_file):
		f = open(dst_file, 'wb')
		shutil.copyfileobj(page_file, f)
		f.close()

class LevelsCreator(AbstractLevelsCreator):
	def __init__(self, download_dir_path):
		self.__download_dir_path = download_dir_path

	def create(self):
		return [Level("magazine", MagazinePageAnalyzer()),
				Level("issue", IssuePageAnalyzer(self.__download_dir_path)),
				Level("article", ArticlePageAnalyzer(self.__download_dir_path))]

def _handle_error_page(page_file, file_path):
	"""@return: C{True} iff the given page is an error page"""
	if not _is_error_page(page_file):
		return
	with open(file_path, "w") as f:
		print >>f, "An error message shown after requesting the page"
	raise PageAnalyzerException("Error page encountered")

def _is_error_page(page_file):
	doc = ElementTree(file=page_file)
	title = doc.find("head/title")
	page_file.seek(0) ## reset file's current position
	if title.text.find("not available") != -1:
		return True
	return False

def _convert_tree_path_to_dir_path(tree_path):
	## Skip root element
	return '/'.join(tree_path[1:])

def _convert_to_2_digit_number(number):
	assert number > 0 and number < 99
	str_ = str(number)
	if number < 10:
		return "0"+str_
	return str_
