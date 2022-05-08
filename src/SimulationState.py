from typing import Dict
from Map import MapPosition, in_range
from Person import Person, PersonState
from Diesease import Virus1
from src.statistics.StatisticSnapshot import StatisticSnapshot


def count_items(_list):
    return dict((x, _list.count(x)) for x in set(_list))


class SimulationState:
    def __init__(self, people: Dict[Person, MapPosition]) -> None:
        super().__init__()
        self.alive_people = people  # to be replaced with better data structure in the future
        self.dead_people = {}

    def step(self):
        people_dead_in_this_step = {}
        for person, pos in self.alive_people.items():
            new_pos, died = person.step()  # TODO: use observer pattern
            if died:
                people_dead_in_this_step[person] = pos
            self.update_position(person, new_pos)

            if person.state.transmissable():
                self.spread_diesase(person)

        for person, pos in people_dead_in_this_step.items():
            self.remove_person(person)
            self.dead_people[person] = pos

    def spread_diesase(self, person):
        neighbors = self.find_neighbors(person)
        for neighbor in list(neighbors):
            if neighbor.state in [PersonState.DIESASE_RESISTANT, PersonState.DIESASE_HOST_ASYMPTOMATIC_NONTRANSMISSABLE]:
                continue
            host_diesase = person.diseases[0]  # TODO: don't use first virus but most relevant
            if host_diesase.type() not in map(lambda d: d.type(), neighbor.diseases):
                neighbor.diseases.append(host_diesase.clone(neighbor))
                neighbor.state = PersonState.DIESASE_HOST_SYMPTOMATIC

    def find_neighbors(self, person: Person, predicate=None):
        if (predicate is None):
            predicate = self.find_position_predicate(10)
        return filter(lambda potential: predicate(person, potential), self.alive_people.keys())

    def find_position(self, person) -> MapPosition:
        return self.alive_people[person]

    # def find_position_predicate(self, distance):
    #     return lambda person: self.find_position(person).

    def find_position_predicate(self, distance):
        return lambda person, potential: in_range(self.find_position(person), self.find_position(potential), distance)

    def update_position(self, person, new_position):
        self.alive_people[person] = new_position

    def remove_person(self, person):
        self.alive_people.pop(person)

    def all_people(self):
        return self.alive_people | self.dead_people

    def get_statistic_snapshot(self):
        states = [p.state for p in self.all_people()]
        return StatisticSnapshot(count_items(states))
