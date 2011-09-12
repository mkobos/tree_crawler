while True:
	node = get_sentinel()
	try:
		while True:
			node = analyze_children_and_move_to_next_node(node)
			if node is None: # The whole tree has been traversed
				return
	except Exception as ex:
		pass

def analyze_children_and_move_to_next_node(node):
	(child, action) = get_available_child(node)
	if child is None:
		return move_to_parent(node)
	else:
		node = move_to_child(child)
		if action == TO_PROCESS:
			is_leaf = process_node_and_check_if_is_leaf(node)
			set_node_type(node, is_leaf)
			if is_leaf:
				return move_to_parent(node)
			else:
				return node
		elif action == TO_VISIT:
			return node

def get_available_child(node):
	while True:
		node.children_cond.acquire()
		child = internal_get_available_child(node)
		if child is None: # No accessible children are available
			node.children_cond.release()
			return (None, None)
		if child.state == OPEN:
			child.state = PROCESSING
			node.children_cond.release()
			return (child, TO_PROCESS)
		elif child.state == VISITED:
			node.children_cond.release()
			return (child, TO_VISIT)
		elif child.state == PROCESSING:
			node.children_cond.wait()
			node.children_cond.release()

def internal_get_available_child(node): 
	# Check for child node in the following order: OPEN, VISITED, PROCESSING 
	# and return it. If not such node is found, return None.

def set_node_type(node, is_leaf):
	node.parent.get_children_cond().acquire()
	if is_leaf:
		node.state = CLOSED
		internal_update_node_state(node.parent)
	else:
		node.state = VISITED
	node.parent.children_cond.notify_all()
	node.parent.children_cond.release()

def internal_update_node_state(node):
	if node == sentinel:
		# The state of the sentinel is undefined and not used 
		# in the program, it should not be changed
		return
	new_state = None
	if node.all_children_are_in_one_of_states({CLOSED}):
		new_state = CLOSED
	elif node.all_children_are_in_one_of_states({ERROR, CLOSED}):
		new_state = ERROR
	# Node state does not have to be changed
	if new_state is None:
		return
	node.parent.children_cond.acquire()
	node.state = new_state
	internal_update_node_state(node.parent)
	node.parent.children_cond.notify_all()
	node.parent.children_cond.release()

def set_error(node):
	node.parent.children_cond.acquire()
	node.state = ERROR
	internal_update_node_state(node.parent)
	node.parent.children_cond.notify_all()
	node.parent.children_cond.release()

def handle_error(node):
	# This function is called when one of the functions used in the
	# analyze_children... function fails for some reson. The node 
	# parameter is set to the currently visited node.
	set_error(node)
	raise Exception()
