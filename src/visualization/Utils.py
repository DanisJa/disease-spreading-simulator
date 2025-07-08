import matplotlib.colors as mcolors
from typing import List


class VisualizationUtils:
    @staticmethod
    def generate_distinct_colors(n):
        """Generate n visually distinct colors"""
        return list(mcolors.TABLEAU_COLORS.values())[:n]

    @staticmethod
    def prepare_network_data(graph):
        """Prepare network data for visualization"""
        nodes = []
        edges = []
        colors = []

        for node_id, node in graph.nodes.items():
            nodes.append(node_id)
            if node.state.value == 'S':
                colors.append('green')
            elif node.state.value == 'I':
                colors.append('red')
            else:
                colors.append('blue')

        for node_id, neighbors in graph.edges.items():
            for neighbor_id in neighbors:
                if (node_id, neighbor_id) not in edges and (neighbor_id, node_id) not in edges:
                    edges.append((node_id, neighbor_id))

        return nodes, edges, colors