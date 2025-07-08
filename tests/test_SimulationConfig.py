import unittest
from src.config.SimulationConfig import SimulationConfig

class TestSimulationConfig(unittest.TestCase):
    def test_default_values(self):
        config = SimulationConfig()
        self.assertEqual(config.infection_chance, 0.5)
        self.assertEqual(config.infection_duration, 3)
        self.assertEqual(config.initial_infected, 1)

    def test_custom_values(self):
        config = SimulationConfig(
            infection_chance=0.7,
            infection_duration=5,
            initial_infected=2
        )
        self.assertEqual(config.infection_chance, 0.7)
        self.assertEqual(config.infection_duration, 5)
        self.assertEqual(config.initial_infected, 2)