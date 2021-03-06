#! /usr/bin/python

# Given information about active users on the network, 
# find the shortest route for a message from one user (the sender) to another (the recipient). 
# Return a list of users that make up this route.

# Hints:
# Remember: both BFS and DFS will eventually find a path if one exists. The difference between the two is:
# BFS always finds the shortest path.
# DFS usually uses less space.


from collections import deque
import unittest


def reconstruct_path(previous_nodes, start_node, end_node):
	reversed_shortest_path = []
	
	# start from the end of the path and work backwards
	current_node = end_node
	while current_node:
		reversed_shortest_path.append(current_node)
		current_node = previous_nodes[current_node]
		
	# Reverse our path to get the right order
	reversed_shortest_path.reverse()  # flip it around, in place
	return reversed_shortest_path


def bfs_get_path(graph, start_node, end_node):
	if start_node not in graph:
		raise Exception("Start Node not in the Graph")
	if end_node not in graph:
		raise Exception("End node not in Graph")
		
	node_to_visit = deque()
	nodes_to_visit.append(start_node)
	
	# to keep track of how we got to each node
	# we will use this to reconstruct the shortest path at the end
	# we will also use this to keep track of which nodes we have already visited
	how_we_reached_nodes = {start_node: None}
	
	while len(nodes_to_visit) > 0:
		current_node = nodes_to_visit.popleft()
		
		# Stop when we reach the end node
		if current_node == end_node:
			return reconstruct_path(how_we_reached_nodes, start_node, end_node)
			
		for neighbor in graph[current_node]:
			node_to_visit.append(neighbor)
			how_we_reached_nodes[neighbor] = current_node
		
	# If we get here, than we never found the end node
	# so there's NO path from start_node to end_node
    return None



# Tests

class Test(unittest.TestCase):

    def setUp(self):
        self.graph = {
            'a': ['b', 'c', 'd'],
            'b': ['a', 'd'],
            'c': ['a', 'e'],
            'd': ['a', 'b'],
            'e': ['c'],
            'f': ['g'],
            'g': ['f'],
        }

    def test_two_hop_path_1(self):
        actual = get_path(self.graph, 'a', 'e')
        expected = ['a', 'c', 'e']
        self.assertEqual(actual, expected)

    def test_two_hop_path_2(self):
        actual = get_path(self.graph, 'd', 'c')
        expected = ['d', 'a', 'c']
        self.assertEqual(actual, expected)

    def test_one_hop_path_1(self):
        actual = get_path(self.graph, 'a', 'c')
        expected = ['a', 'c']
        self.assertEqual(actual, expected)

    def test_one_hop_path_2(self):
        actual = get_path(self.graph, 'f', 'g')
        expected = ['f', 'g']
        self.assertEqual(actual, expected)

    def test_one_hop_path_3(self):
        actual = get_path(self.graph, 'g', 'f')
        expected = ['g', 'f']
        self.assertEqual(actual, expected)

    def test_zero_hop_path(self):
        actual = get_path(self.graph, 'a', 'a')
        expected = ['a']
        self.assertEqual(actual, expected)

    def test_no_path(self):
        actual = get_path(self.graph, 'a', 'f')
        expected = None
        self.assertEqual(actual, expected)

    def test_start_node_not_present(self):
        with self.assertRaises(Exception):
            get_path(self.graph, 'h', 'a')

    def test_end_node_not_present(self):
        with self.assertRaises(Exception):
            get_path(self.graph, 'a', 'h')


unittest.main(verbosity=2)


# Space Complexity = O(N)
# Time Complexity = O(N + M)

# In the worst case, we'll go through the BFS loop once for every node in the graph, 
# since we only ever add each node to nodes_to_visit once 
# (we check how_we_reached_nodes to see if we've already added a node before). 
# Each loop iteration involves a constant amount of work to dequeue the node 
# and check if it's our end node. If we have n nodes, then this portion of the loop is 
# O(N).

# But there's more to each loop iteration: we also look at the current node's neighbors. 
# Over all of the nodes in the graph, checking the neighbors is O(M), 
# since it involves crossing each edge twice: once for each node at either end.

# Putting this together, the complexity of the breadth-first search is O(N+M).
