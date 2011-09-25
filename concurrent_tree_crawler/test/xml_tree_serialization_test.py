import unittest
import StringIO
from concurrent_tree_crawler.standard_node import StandardNode
from concurrent_tree_crawler.abstract_node import NodeState
from concurrent_tree_crawler.test.subtrees_comparer import subtrees_equal
from concurrent_tree_crawler.xml_tree_serialization import \
	XMLTreeWriter, XMLTreeReader

class XMLTreeSerializationTestCase(unittest.TestCase):
	def test_basic_write_and_read(self):
		(sentinel, schema_root) = self.__create_tree()
		out = StringIO.StringIO()
		writer = XMLTreeWriter(out)
		writer.write(sentinel)
		out_str = out.getvalue()
		in_ = StringIO.StringIO(out_str)
		reader = XMLTreeReader(in_)
		new_sentinel = StandardNode()
		reader.read(new_sentinel)
		self.assert_(subtrees_equal(schema_root, new_sentinel.get_child("root")))
		out2 = StringIO.StringIO()
		writer2 = XMLTreeWriter(out2)
		writer2.write(new_sentinel)
		out2_str = out2.getvalue()
		self.assertEqual(out_str, out2_str)
	
	def __create_tree(self):
		sentinel = StandardNode()
		root = sentinel.add_child("root", NodeState.VISITED)
		i1 = root.add_child("issue1", NodeState.CLOSED)
		i1.add_child("article1-1", NodeState.CLOSED)
		i1.add_child("article1-2", NodeState.CLOSED)
		
		i2 = root.add_child("issue2", NodeState.VISITED)
		i2.add_child("article2-1", NodeState.OPEN)
		i2.add_child("article2-2", NodeState.CLOSED)
		i2.add_child("article2-3", NodeState.ERROR)
		
		root.add_child("issue3", NodeState.PROCESSING)
		
		i4 = root.add_child("issue4", NodeState.ERROR)
		i4.add_child("article4-1", NodeState.PROCESSING)
		
		t = ("root", NodeState.VISITED,
				[("issue1", NodeState.CLOSED, 
					[("article1-1", NodeState.CLOSED, []),
					("article1-2", NodeState.CLOSED, [])]
				),
				("issue2", NodeState.CLOSED, 
					[("article2-1", NodeState.OPEN, []),
					("article2-2", NodeState.CLOSED, []),
					("article2-3", NodeState.ERROR, [])]
				),
				("issue3", NodeState.PROCESSING, []),
				("issue4", NodeState.ERROR, 
					[("article4-1", NodeState.PROCESSING, [])]
				)]
			)
		self.assert_(subtrees_equal(t, root))
		return (sentinel, t)