import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
import ipywidgets as widgets
from IPython.display import display
from typing import List, Dict


class InteractiveVisualizer:
    def __init__(self, graph, history):
        self.graph = graph
        self.history = history
        self.G = self._create_networkx_graph()
        self.pos = nx.spring_layout(self.G, seed=42)

    def _create_networkx_graph(self):
        G = nx.Graph()
        for node_id in self.graph.nodes:
            G.add_node(node_id)
        for node_id, neighbors in self.graph.edges.items():
            for neighbor_id in neighbors:
                G.add_edge(node_id, neighbor_id)
        return G

    def create_dashboard(self):
        plt.ioff()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Animation controls
        play = widgets.Play(
            interval=500,
            value=0,
            min=0,
            max=len(self.history) - 1,
            step=1,
            description="Press play"
        )
        slider = widgets.IntSlider(min=0, max=len(self.history) - 1)
        widgets.jslink((play, 'value'), (slider, 'value'))

        def update(frame):
            ax1.clear()
            ax2.clear()
            day = self.history[frame]['day']

            # Update network plot
            color_map = []
            for node_id, node in self.graph.nodes.items():
                if node.state.value == 'S':
                    color_map.append('green')
                elif node.state.value == 'I':
                    color_map.append('red')
                else:
                    color_map.append('blue')

            nx.draw(self.G, self.pos, ax=ax1, node_color=color_map,
                    with_labels=True, node_size=500)
            ax1.set_title(f"Network State (Day {day})")

            # Update SIR curve
            days = [h['day'] for h in self.history[:frame + 1]]
            s = [h['susceptible'] for h in self.history[:frame + 1]]
            i = [h['infected'] for h in self.history[:frame + 1]]
            r = [h['recovered'] for h in self.history[:frame + 1]]

            ax2.stackplot(days, s, i, r,
                          colors=['green', 'red', 'blue'],
                          alpha=0.7)
            ax2.set_title('Disease Spread Over Time')
            ax2.set_xlabel('Days')
            ax2.set_ylabel('Number of Nodes')
            ax2.set_xlim(0, len(self.history))
            ax2.set_ylim(0, len(self.graph.nodes))
            ax2.grid(True)
            ax2.legend(['Susceptible', 'Infected', 'Recovered'])

        display(widgets.HBox([play, slider]))
        anim = FuncAnimation(fig, update, frames=len(self.history), interval=500)
        plt.show()
        return anim