from Map import Map, MapPosition
from Person import Person
from SimulationState import SimulationState
import random

import ImageGenerator
from src.ImageGenerator import ImageGenerator


def generate_person(pos: MapPosition, map: Map):
    return Person(pos, map)

def generate_position(map: Map):
    return MapPosition(random.randint(map.x_min, map.x_max), random.randint(map.y_min, map.y_max))

def generate_people(n: int, map: Map):
    people_with_pos = []
    for i in range(n):
        pos = generate_position(map)
        person_with_pos = (generate_person(pos, map), pos)
        people_with_pos.append(person_with_pos)
    return dict(people_with_pos)


class Simulation:
    def __init__(self, map: Map, num_people: int) -> None:
        self.map = map
        self.simulation_state = SimulationState(generate_people(num_people, self.map))
        self.image_generator = ImageGenerator()

    def step(self):
        self.simulation_state.step()
        self.image_generator.add_state(self.simulation_state, self.map)

    def steps(self, n):
        [self.step() for _ in range(n)]
        self.image_generator.save_image()


HEIGHT = 300
WIDTH = 300
Simulation(Map(HEIGHT, WIDTH), 90).steps(500)
