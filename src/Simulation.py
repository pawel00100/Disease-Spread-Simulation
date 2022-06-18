import random
import ImageGenerator
from Map import Map, MapPosition
from Person import Person, PersonState
from SimulationState import SimulationState
from Diesease import Virus1
from ImageGenerator import ImageGenerator
from statistics.StatisticSystem import StatisticSystem
from constants import RAND_IMMUNITY
from matplotlib import pyplot as plt

def generate_person(pos: MapPosition, map: Map, iter: int):
    return Person(pos, map, iter)


def generate_position(map: Map):
    return MapPosition(random.randint(map.x_min, map.x_max), random.randint(map.y_min, map.y_max), map)


def generate_people(n: int, map: Map, iter: int):
    people_with_pos = []
    for i in range(n):
        pos = generate_position(map)
        person_with_pos = (generate_person(pos, map, iter), pos)
        people_with_pos.append(person_with_pos)
    return dict(people_with_pos)


class Simulation:
    def __init__(self, map: Map, starting_state: SimulationState) -> None:
        self.map = map
        self.simulation_state = starting_state
        self.statistic_system = StatisticSystem()
        self.image_generator = ImageGenerator()

    def step(self, n):
        self.simulation_state.step()
        self.statistic_system.add_snapshot(self.simulation_state.get_statistic_snapshot())
        self.image_generator.add_state(self.simulation_state, self.map)

    def steps(self, n):
        [self.step(i) for i in range(n)]
        self.image_generator.save_image()
        self.statistic_system.display_plot()


HEIGHT = 200
WIDTH = 200

map = Map(HEIGHT, WIDTH)
fig, ax = plt.subplots(2, 2)

for i in range(len(RAND_IMMUNITY)):
    people = generate_people(160, map, i)

    sick_person = list(people.keys())[0]
    sick_person.diseases.append(Virus1(sick_person, i))
    sick_person.state = PersonState.DIESASE_HOST_SYMPTOMATIC

    starting_state = SimulationState(people, i)
    Simulation(map, starting_state).steps(250)

plt.show()