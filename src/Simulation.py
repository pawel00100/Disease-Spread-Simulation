import random
import ImageGenerator
from Map import Map, MapPosition
from Person import Person, PersonState
from SimulationState import SimulationState
from Diesease import Virus1
from ImageGenerator import ImageGenerator


def generate_person(pos: MapPosition, map: Map):
    return Person(pos, map)


def generate_position(map: Map):
    return MapPosition(random.randint(map.x_min, map.x_max), random.randint(map.y_min, map.y_max), map)


def generate_people(n: int, map: Map):
    people_with_pos = []
    for i in range(n):
        pos = generate_position(map)
        person_with_pos = (generate_person(pos, map), pos)
        people_with_pos.append(person_with_pos)
    return dict(people_with_pos)


class Simulation:
    def __init__(self, map: Map, starting_state: SimulationState) -> None:
        self.map = map
        self.simulation_state = starting_state
        self.image_generator = ImageGenerator()

    def step(self, n):
        self.simulation_state.step()
        self.image_generator.add_state(self.simulation_state, self.map)

    def steps(self, n):
        [self.step(i) for i in range(n)]
        self.image_generator.save_image()


HEIGHT = 300
WIDTH = 300

map = Map(HEIGHT, WIDTH)
people = generate_people(160, map)

sick_person = list(people.keys())[0]
sick_person.diseases.append(Virus1(sick_person))
sick_person.state = PersonState.DIESASE_HOST_SYMPTOMATIC

starting_state = SimulationState(people)
Simulation(map, starting_state).steps(150)
