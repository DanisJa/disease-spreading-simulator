from rich.console import Console
from rich.table import Table
from rich.progress import track
from typing import Dict, List


class ConsoleVisualizer:
    def __init__(self):
        self.console = Console()

    def show_snapshot(self, stats: Dict, graph):
        table = Table(title=f"Day {stats['day']}")
        table.add_column("State", style="cyan")
        table.add_column("Count", style="magenta")

        for state, count in stats.items():
            if state != 'day':
                table.add_row(state.upper(), str(count))

        self.console.print(table)
        self._print_network(graph)

    def _print_network(self, graph):
        net_table = Table(title="Network Connections")
        net_table.add_column("Node", style="bold")
        net_table.add_column("State")
        net_table.add_column("Neighbors")

        for node_id, node in graph.nodes.items():
            neighbors = ", ".join(str(n) for n in graph.get_neighbors(node_id))
            net_table.add_row(
                str(node_id),
                self._color_state(node.state.value),
                neighbors
            )

        self.console.print(net_table)

    def _color_state(self, state):
        colors = {'S': 'green', 'I': 'red', 'R': 'blue'}
        return f"[{colors.get(state, 'white')}]{state}[/]"