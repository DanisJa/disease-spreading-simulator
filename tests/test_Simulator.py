import unittest
from unittest.mock import patch
from src.engine.Simulator import Simulator
from src.models.Graph import Graph
from src.models.Node import Node
from src.models.State import State
from src.config.SimulationConfig import SimulationConfig  # Import the class directly

class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.node1 = Node(1)
        self.node2 = Node(2)
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(1, 2)
        self.config = SimulationConfig(
            infection_chance=1.0,  # 100% chance for deterministic testing
            infection_duration=2
        )

    def test_initialization(self):
        simulator = Simulator(self.graph, self.config)
        self.assertEqual(simulator.day, 0)
        self.assertEqual(len(simulator.graph.nodes), 2)

    @patch('random.Random')
    def test_infection_spread(self, mock_random):
        # Configure mock to always return 0.5 (less than our 1.0 infection_chance)
        mock_random.return_value.random.return_value = 0.5

        simulator = Simulator(self.graph, self.config)
        self.node1.infect()  # Manually infect node1

        simulator.tick()  # Should infect node2

        self.assertEqual(self.node2.state, State.INFECTED)

    def test_recovery_after_duration(self):
        simulator = Simulator(self.graph, self.config)
        self.node1.infect()

        # Day 1 - should increment duration
        simulator.tick()
        self.assertEqual(self.node1.state, State.INFECTED)
        self.assertEqual(self.node1.days_infected, 1)

        # Day 2 - should recover
        simulator.tick()
        self.assertEqual(self.node1.state, State.RECOVERED)