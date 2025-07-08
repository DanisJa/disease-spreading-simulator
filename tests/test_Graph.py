import unittest
from src.models.Graph import Graph
from src.models.Node import Node

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.node1 = Node(1)
        self.node2 = Node(2)
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)

    def test_add_node(self):
        self.assertIn(1, self.graph.nodes)
        self.assertIn(2, self.graph.nodes)
        self.assertEqual(len(self.graph.edges[1]), 0)

    def test_add_edge(self):
        self.graph.add_edge(1, 2)
        self.assertIn(2, self.graph.edges[1])
        self.assertIn(1, self.graph.edges[2])

    def test_get_neighbors(self):
        self.graph.add_edge(1, 2)
        neighbors = self.graph.get_neighbors(1)
        self.assertEqual(neighbors, [2])