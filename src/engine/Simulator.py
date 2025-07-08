from typing import Optional, List, Dict
from ..models.State import State
from ..config.SimulationConfig import SimulationConfig
from ..models import Graph
from ..utils.random_utils import get_random_generator


class Simulator:
    def __init__(self, graph: Graph, config: Optional[SimulationConfig] = None):
        self.graph = graph
        self.config = config
        self.day = 0
        self.rng = get_random_generator()
        self.history: List[Dict[str, int]] = []

    def tick(self):
        self._spread_infection()
        self._update_infections()
        self._record_stats()
        self.day += 1

    def _record_stats(self):
        counts = {
            'day': self.day,
            'susceptible': 0,  # Initialize counters
            'infected': 0,
            'recovered': 0
        }

        for node in self.graph.nodes.values():
            if node.state == State.SUSCEPTIBLE:
                counts['susceptible'] += 1
            elif node.state == State.INFECTED:
                counts['infected'] += 1
            else:
                counts['recovered'] += 1

        self.history.append(counts)

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