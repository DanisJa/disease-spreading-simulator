import dataclasses
from .State import State

@dataclasses.dataclass
class Node:
    id: int
    state: State = State.SUSCEPTIBLE
    days_infected: int = 0

    def infect(self):
        if self.state == State.SUSCEPTIBLE or self.state == State.RECOVERED:
            self.state = State.INFECTED
            self.days_infected = 0

    def recover(self):
        if self.state == State.INFECTED:
            self.state = State.RECOVERED
            self.days_infected = 0

    def increment_infection_duration(self):
        if self.state == State.INFECTED:
            self.days_infected += 1