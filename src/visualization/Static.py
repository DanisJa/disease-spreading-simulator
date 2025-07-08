import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Dict

class StaticVisualizer:
    @staticmethod
    def plot_sir_history(history: List[Dict]):
        days = [h['day'] for h in history]
        s = [h['susceptible'] for h in history]
        i = [h['infected'] for h in history]
        r = [h['recovered'] for h in history]

        plt.figure(figsize=(12, 6))
        plt.stackplot(days, s, i, r,
                      labels=['Susceptible', 'Infected', 'Recovered'],
                      colors=['green', 'red', 'blue'],
                      alpha=0.7)
        plt.legend(loc='upper right')
        plt.title('Disease Spread Over Time')
        plt.xlabel('Days')
        plt.ylabel('Number of Nodes')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_network(graph, day=None):
        G = nx.Graph()
        color_map = []

        for node_id, node in graph.nodes.items():
            G.add_node(node_id)
            if node.state.value == 'S':
                color_map.append('green')
            elif node.state.value == 'I':
                color_map.append('red')
            else:
                color_map.append('blue')

        for node_id, neighbors in graph.edges.items():
            for neighbor_id in neighbors:
                G.add_edge(node_id, neighbor_id)

        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, node_color=color_map, with_labels=True,
                node_size=800, font_size=10, font_weight='bold')

        title = 'Network State'
        if day is not None:
            title += f' (Day {day})'
        plt.title(title)

        # Create custom legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', label='Susceptible',
                       markerfacecolor='green', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', label='Infected',
                       markerfacecolor='red', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', label='Recovered',
                       markerfacecolor='blue', markersize=10)
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        plt.show()