from src.Map import Map, MapPosition
from src.Person import Person
from src.SimulationState import SimulationState
import random


def generate_person(pos: MapPosition):
    return Person(pos)


def generate_position(map: Map):
    return MapPosition(random.randint(map.x_min, map.x_max), random.randint(map.y_min, map.y_max))


def generate_people(n: int, map: Map):
    people_with_pos = []
    for i in range(n):
        pos = generate_position(map)
        person_with_pos = (generate_person(pos), pos)
        people_with_pos.append(person_with_pos)
    return dict(people_with_pos)


class Simulation:
    def __init__(self, num_people) -> None:
        self.map = Map(200,200)
        self.simulation_state = SimulationState(generate_people(num_people, self.map))

    def step(self):
        self.simulation_state.step()
        print(self.simulation_state.people)

    def steps(self, n):
        [self.step() for _ in range(n)]

Simulation(10).steps(10)
