import math
from typing import Dict
from Map import MapPosition, in_range
from Person import Person


class SimulationState:
    def __init__(self, people: Dict[Person,MapPosition]) -> None:
        super().__init__()
        self.people = people  # to be replaced with better data structure in the future

    def step(self):
        for person, pos in self.people.items():
            new_pos = person.step() #TODO: use observer pattern
            self.update_position(person, new_pos)

    def find_neighbors(self, person: Person, predicate = None):
        if (predicate is None):
            predicate = self.find_position_predicate(10)
        return filter(lambda potential: predicate(person, potential), self.people.keys())

    def find_position(self, person) -> MapPosition:
        return self.people[person]

    # def find_position_predicate(self, distance):
    #     return lambda person: self.find_position(person).

    def find_position_predicate(self, distance):
        return lambda person, potential: in_range(self.find_position(person), self.find_position(potential), distance)

    def update_position(self, person, new_position):
        self.people[person] = new_position



