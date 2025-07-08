from dataclasses import dataclass

@dataclass
class SimulationConfig:
    infection_chance: float = 0.5
    infection_duration: int = 3
    initial_infected: int = 1
