import random
import PySimpleGUI as sg
from src.models.Graph import Graph
from src.models.Node import Node
from src.engine.Simulator import Simulator
from src.config.SimulationConfig import SimulationConfig
from src.models.State import State
from src.visualization.Static import StaticVisualizer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, List


class DiseaseSpreadApp:
    def __init__(self):
        self.simulator = None
        self.graph = None
        self.setup_ui()

    def setup_ui(self):
        sg.theme('DarkBlue3')

        # Parameter controls
        controls = [
            [sg.Text('Network Parameters', font='_ 14')],
            [sg.Text('Nodes:'), sg.Slider((100, 2000), 500, 100, orientation='h', key='-NODES-')],
            [sg.Text('Edge Probability (%):'), sg.Slider((0.1, 10), 1, 0.1, orientation='h', key='-EDGE_PROB-')],
            [sg.Text('Initial Infected:'), sg.Slider((1, 50), 5, 1, orientation='h', key='-INIT_INFECTED-')],

            [sg.Text('Disease Parameters', font='_ 14')],
            [sg.Text('Infection Chance (%):'), sg.Slider((1, 100), 20, 1, orientation='h', key='-INFECT_CHANCE-')],
            [sg.Text('Infection Duration:'), sg.Slider((1, 14), 5, 1, orientation='h', key='-INFECT_DURATION-')],

            [sg.Text('Simulation Controls', font='_ 14')],
            [sg.Text('Days to Simulate:'), sg.Slider((10, 100), 30, 1, orientation='h', key='-DAYS-')],
            [sg.Button('Initialize'), sg.Button('Run Simulation'), sg.Button('Step Day'), sg.Button('Reset')],
        ]

        # Visualization area
        visualization = [
            [sg.Canvas(key='-SIR_CANVAS-')],
            [sg.Canvas(key='-NETWORK_CANVAS-')],
        ]

        # Status area
        status = [
            [sg.Text('Ready to initialize simulation', key='-STATUS-')],
            [sg.Text('Day: 0', key='-DAY-')],
            [sg.Text('S: 0', key='-S-'), sg.Text('I: 0', key='-I-'), sg.Text('R: 0', key='-R-')],
        ]

        layout = [
            [sg.Column(controls), sg.VSeparator(), sg.Column(visualization)],
            [sg.HSeparator()],
            [sg.Column(status)]
        ]

        # Create window without specifying icon
        self.window = sg.Window('Disease Spread Simulator', layout, finalize=True, resizable=True)
        self.figures = []

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            elif event == 'Initialize':
                self.initialize_simulation(values)

            elif event == 'Run Simulation':
                self.run_simulation(values)

            elif event == 'Step Day':
                self.step_simulation()

            elif event == 'Reset':
                self.reset_simulation()

        self.window.close()

    def initialize_simulation(self, values):
        try:
            num_nodes = int(values['-NODES-'])
            edge_prob = float(values['-EDGE_PROB-']) / 100
            init_infected = int(values['-INIT_INFECTED-'])

            self.graph = self.create_network(
                num_nodes=num_nodes,
                edge_probability=edge_prob
            )

            config = SimulationConfig(
                infection_chance=float(values['-INFECT_CHANCE-']) / 100,
                infection_duration=int(values['-INFECT_DURATION-']),
                initial_infected=init_infected
            )

            self.simulator = Simulator(self.graph, config)

            # Infect initial nodes
            patient_zero_ids = random.sample(list(self.graph.nodes.keys()), init_infected)
            for node_id in patient_zero_ids:
                self.graph.nodes[node_id].state = State.INFECTED

            self.update_status()
            self.window['-STATUS-'].update('Simulation initialized!')

        except Exception as e:
            sg.popup_error(f'Initialization failed: {str(e)}')

    def run_simulation(self, values):
        if not self.simulator:
            sg.popup_error('Please initialize simulation first')
            return

        days = int(values['-DAYS-'])

        for _ in range(days):
            self.step_simulation()

    def step_simulation(self):
        if not self.simulator:
            sg.popup_error('Please initialize simulation first')
            return

        self.simulator.tick()
        self.update_status()
        self.update_visualizations()

    def reset_simulation(self):
        self.simulator = None
        self.graph = None
        self.clear_figures()
        self.window['-STATUS-'].update('Simulation reset')
        self.window['-DAY-'].update('Day: 0')
        self.window['-S-'].update('S: 0')
        self.window['-I-'].update('I: 0')
        self.window['-R-'].update('R: 0')

    def create_network(self, num_nodes=500, edge_probability=0.01):
        graph = Graph()

        # Add nodes
        for i in range(1, num_nodes + 1):
            graph.add_node(Node(id=i))

        # Add random edges
        for i in range(1, num_nodes + 1):
            for j in range(i + 1, num_nodes + 1):
                if random.random() < edge_probability:
                    graph.add_edge(i, j)

        return graph

    def update_status(self):
        if not self.simulator:
            return

        current = self.simulator.history[-1]
        self.window['-DAY-'].update(f'Day: {current["day"]}')
        self.window['-S-'].update(f'S: {current["susceptible"]}')
        self.window['-I-'].update(f'I: {current["infected"]}')
        self.window['-R-'].update(f'R: {current["recovered"]}')

    def update_visualizations(self):
        if not self.simulator:
            return

        self.clear_figures()

        # SIR Plot
        fig_sir = StaticVisualizer.create_sir_figure(self.simulator.history)
        canvas_sir = FigureCanvasTkAgg(fig_sir, self.window['-SIR_CANVAS-'].TKCanvas)
        canvas_sir.draw()
        canvas_sir.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.figures.append((canvas_sir, fig_sir))

        # Network Plot (show subset for performance)
        if len(self.graph.nodes) > 100:
            small_graph = self.create_small_subset(self.graph, 100)
        else:
            small_graph = self.graph

        fig_net = StaticVisualizer.create_network_figure(small_graph, self.simulator.day)
        canvas_net = FigureCanvasTkAgg(fig_net, self.window['-NETWORK_CANVAS-'].TKCanvas)
        canvas_net.draw()
        canvas_net.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.figures.append((canvas_net, fig_net))

    def create_small_subset(self, graph, subset_size=100):
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

    def clear_figures(self):
        for canvas, fig in self.figures:
            canvas.get_tk_widget().destroy()
            plt.close(fig)
        self.figures = []


class StaticVisualizer:
    @staticmethod
    def create_sir_figure(history):
        days = [h['day'] for h in history]
        s = [h['susceptible'] for h in history]
        i = [h['infected'] for h in history]
        r = [h['recovered'] for h in history]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.stackplot(days, s, i, r,
                     labels=['Susceptible', 'Infected', 'Recovered'],
                     colors=['green', 'red', 'blue'],
                     alpha=0.7)
        ax.legend(loc='upper right')
        ax.set_title('Disease Spread Over Time')
        ax.set_xlabel('Days')
        ax.set_ylabel('Number of Nodes')
        ax.grid(True)
        plt.tight_layout()
        return fig

    @staticmethod
    def create_network_figure(graph, day=None):
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

        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, ax=ax, node_color=color_map, with_labels=True,
                node_size=100, font_size=8)

        title = 'Network State'
        if day is not None:
            title += f' (Day {day})'
        ax.set_title(title)

        return fig


if __name__ == '__main__':
    app = DiseaseSpreadApp()
    app.run()