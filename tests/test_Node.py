import unittest
from src.models.Node import Node
from src.models.State import State

class TestNode(unittest.TestCase):
    def setUp(self):
        self.node = Node(id=1)

    def test_initial_state(self):
        self.assertEqual(self.node.state, State.SUSCEPTIBLE)
        self.assertEqual(self.node.days_infected, 0)

    def test_infect(self):
        self.node.infect()
        self.assertEqual(self.node.state, State.INFECTED)
        self.assertEqual(self.node.days_infected, 0)

    def test_recover(self):
        self.node.infect()
        self.node.recover()
        self.assertEqual(self.node.state, State.RECOVERED)
        self.assertEqual(self.node.days_infected, 0)

    def test_increment_infection(self):
        self.node.infect()
        self.node.increment_infection_duration()
        self.assertEqual(self.node.days_infected, 1)