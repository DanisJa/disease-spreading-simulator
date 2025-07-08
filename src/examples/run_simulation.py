from src.models.Graph import Graph
from src.models.Node import Node
from src.engine.Simulator import Simulator
from src.config.SimulationConfig import SimulationConfig
from src.visualization.Console import ConsoleVisualizer


def create_sample_graph():
    graph = Graph()
    for i in range(1, 1000):
        graph.add_node(Node(i))
    for i in range (1, 1000):
        graph.add_edge(i, i + 1)
    return graph


def run_simulation():
    graph = create_sample_graph()
    config = SimulationConfig(
        infection_chance=0.9,
        infection_duration=3
    )
    sim = Simulator(graph, config)

    # Infect patient zero
    graph.nodes[1].infect()

    for _ in range(10):
        sim.tick()
        ConsoleVisualizer.show_live_stats(sim)

    ConsoleVisualizer.plot_history(sim)


if __name__ == "__main__":
    run_simulation()