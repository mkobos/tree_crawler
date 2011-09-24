import xml.parsers.expat
from concurrent_tree_crawler.abstract_node import AbstractNode, NodeState

class XMLTreeWriter:
	def __init__(self, file_):
		self.__f = file_

	def write(self, sentinel):
		"""
		@type sentinel: L{AbstractNode}
		"""
		root = sentinel.get_child("root")
		self.__print(0, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
		self.__print(0, "<tree>")
		self.__print_node(1, root)
		self.__print(0, "</tree>")
	
	def __print_node(self, level, node):
		prefix_str = "<node name=\"{}\" state=\"{}\"".format(
			node.get_name(), NodeState.to_str(node.get_state()))
		children = node.get_children()
		if children:
			self.__print(level, "{}>".format(prefix_str))
			for child in node.get_children():
				self.__print_node(level+1, child)
			self.__print(level, "</node>")
		else:
			self.__print(level, "{}/>".format(prefix_str))
	
	def __print(self, level, text):
		print >>self.__f, "{}{}".format("\t"*level, text)

class XMLTreeReader:
	def __init__(self, file_):
		self.__file = file_
		self.__curr_node = None
		self.__parser = xml.parsers.expat.ParserCreate()
	
		self.__parser.StartElementHandler = self.__start_element
		self.__parser.EndElementHandler = self.__end_element
		self.__parser.CharacterDataHandler = self.__char_data
	
	def __start_element(self, name, attrs):
		if name == "tree":
			return
		if name == "node":
			state = NodeState.from_str(attrs["state"])
			node_name = attrs["name"]
			self.__curr_node = self.__curr_node.add_child(node_name, state)
	
	def __end_element(self, name):
		if name == "tree":
			return
		if name == "node":
			self.__curr_node = self.__curr_node.get_parent()
	
	def __char_data(self, data):
		pass
	
	def read(self, sentinel):
		"""
		@param sentinel: a node that will be treated as sentinel in the
			newly created tree, it shouldn't have any children.
		@type sentinel: L{AbstractNode}
		""" 
		assert not sentinel.get_children(), \
			"The sentinel should be a single node, without children"
		self.__curr_node = sentinel
		self.__parser.ParseFile(self.__file)