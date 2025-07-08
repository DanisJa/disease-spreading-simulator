from typing import Dict, List
from src.models import Node


class Graph:
    def __init__(self):
        self.nodes: Dict[int, 'Node'] = {}
        self.edges: Dict[int, List[int]] = {}

    def add_node(self, node: 'Node'):
        self.nodes[node.id] = node
        self.edges[node.id] = []

    def add_edge(self, id1: int, id2: int):
        if id1 in self.nodes and id2 in self.nodes:
            self.edges[id1].append(id2)
            self.edges[id2].append(id1)

    def get_neighbors(self, node_id: int) -> List[int]:
        return self.edges.get(node_id, [])