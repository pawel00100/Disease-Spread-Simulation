from typing import Dict

from Map import MapPosition, in_range
from Person import Person
from src.Diesease import Virus1


class SimulationState:
    def __init__(self, people: Dict[Person, MapPosition]) -> None:
        super().__init__()
        self.people = people  # to be replaced with better data structure in the future

    def step(self):
        dead_people = []
        for person, pos in self.people.items():
            new_pos, died = person.step()  # TODO: use observer pattern
            if died:
                dead_people.append(person)
            self.update_position(person, new_pos)

            if person.state().transmissable():
                self.spread_diesase(person)

        for person in dead_people:
            self.remove_person(person)

    def spread_diesase(self, person):
        neighbors = self.find_neighbors(person)
        for neighbor in list(neighbors):
            print("Contact")
            neighbor.diseases.append(Virus1(neighbor))

    def find_neighbors(self, person: Person, predicate=None):
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

    def remove_person(self, person):
        self.people.pop(person)
