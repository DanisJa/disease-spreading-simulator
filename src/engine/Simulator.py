# src/engine/Simulator.py
from typing import Optional
from ..models import Node, Graph
from ..config import SimulationConfig
from ..models.State import State
from ..utils.random_utils import get_random_generator


class Simulator:
    def __init__(self, graph: Graph, config: Optional[SimulationConfig] = None):
        self.graph = graph
        self.config = config if config else SimulationConfig()
        self.day = 0
        self.rng = get_random_generator()

    def tick(self):
        self._spread_infection()
        self._update_infections()
        self.day += 1

    def _spread_infection(self):
        infected_nodes = [node for node in self.graph.nodes.values()
                          if node.state == State.INFECTED]

        for node in infected_nodes:
            for neighbor_id in self.graph.get_neighbors(node.id):
                neighbor = self.graph.nodes[neighbor_id]
                if (neighbor.state == State.SUSCEPTIBLE and
                        self.rng.random() < self.config.infection_chance):
                    neighbor.infect()

    def _update_infections(self):
        for node in self.graph.nodes.values():
            if node.state == State.INFECTED:
                node.increment_infection_duration()
                if node.days_infected >= self.config.infection_duration:
                    node.recover()