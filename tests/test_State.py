import unittest
from src.models.State import State

class TestNodeState(unittest.TestCase):
    def test_state_values(self):
        self.assertEqual(State.SUSCEPTIBLE.value, 'S')
        self.assertEqual(State.INFECTED.value, 'I')
        self.assertEqual(State.RECOVERED.value, 'R')