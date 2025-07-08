import random
from src.models.Graph import Graph
from src.models.Node import Node
from src.engine.Simulator import Simulator
from src.config.SimulationConfig import SimulationConfig
from src.models.State import State
from src.visualization.Console import ConsoleVisualizer
from src.visualization.Static import StaticVisualizer
from src.visualization.Interactive import InteractiveVisualizer

def create_large_network(num_nodes=1000, edge_probability=0.005):
    graph = Graph()
    for i in range(1, num_nodes + 1):
        graph.add_node(Node(id=i))
    for i in range(1, num_nodes + 1):
        for j in range(i + 1, num_nodes + 1):
            if random.random() < edge_probability:
                graph.add_edge(i, j)
    return graph

def run_simulation():
    print("Creating network with 1000 nodes...")
    graph = create_large_network(num_nodes=1000, edge_probability=0.05)
    config = SimulationConfig(
        infection_chance=0.2,
        infection_duration=7,
        initial_infected=1
    )
    sim = Simulator(graph, config)
    patient_zero_ids = random.sample(list(graph.nodes.keys()), config.initial_infected)
    for node_id in patient_zero_ids:
        graph.nodes[node_id].state = State.INFECTED
    print("Running simulation for 30 days...")
    for day in range(30):
        sim.tick()
        if day % 1 == 0:
            print(f"Day {day}: {sum(1 for n in graph.nodes.values() if n.state == State.INFECTED)} infected")
    return sim, graph

def visualize_results(simulator, graph):
    print("\nVisualizing results...")
    console = ConsoleVisualizer()
    console.show_snapshot(simulator.history[-1], graph)
    print("Generating static plots...")
    StaticVisualizer.plot_sir_history(simulator.history)
    print("Generating network visualization (subset of 50 nodes)...")
    small_graph = create_small_subset(graph, 50)
    StaticVisualizer.plot_network(small_graph, simulator.day)
    if 'get_ipython' in globals():
        print("Preparing interactive visualization...")
        interactive = InteractiveVisualizer(graph, simulator.history)
        return interactive.create_dashboard()

def create_small_subset(graph, subset_size=50):
    small_graph = Graph()
    node_ids = random.sample(list(graph.nodes.keys()), subset_size)
    for node_id in node_ids:
        original_node = graph.nodes[node_id]
        new_node = Node(id=node_id)
        new_node.state = original_node.state
        new_node.days_infected = original_node.days_infected
        small_graph.add_node(new_node)
    for node_id in node_ids:
        for neighbor_id in graph.get_neighbors(node_id):
            if neighbor_id in node_ids:
                small_graph.add_edge(node_id, neighbor_id)
    return small_graph

if __name__ == "__main__":
    sim, graph = run_simulation()
    visualize_results(sim, graph)
