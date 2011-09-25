def subtrees_equal(expected_schema_node, actual_node):
	if expected_schema_node[0] != actual_node.get_name():
		return False
	if expected_schema_node[1] != actual_node.get_state():
		return False
	expected_children = expected_schema_node[2]
	actual_children = actual_node.get_children()
	actual_children_names = [child.get_name() for child in actual_children]
	actual_children_names.sort()
	if len(expected_children) != len(actual_children_names):
		return False
	for (expected_child, actual_child_name) in \
			zip(expected_children, actual_children_names):
		subtrees_equal(
			expected_child, actual_node.get_child(actual_child_name))
	return True