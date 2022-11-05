import random
import time

import ImageGenerator
from Map import Map, MapPosition
from Person import Person, PersonState
from SimulationState import SimulationState
from Diesease import Virus1
from ImageGenerator import ImageGenerator
from src.statistics.StatisticSystem import StatisticSystem


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
        self.statistic_system = StatisticSystem()
        self.image_generator = ImageGenerator()

    def step(self, save_gif, plot_image):
        self.simulation_state.step()
        if plot_image:
            self.statistic_system.add_snapshot(self.simulation_state.get_statistic_snapshot())
        if save_gif:
            self.image_generator.add_state(self.simulation_state, self.map)

    def steps(self, n, save_gif = True, plot_image = True):
        [self.step(save_gif, plot_image) for i in range(n)]
        if save_gif:
            self.image_generator.save_image()
        if plot_image:
            self.statistic_system.display_plot()


# HEIGHT = 200
# WIDTH = 200
HEIGHT = 400
WIDTH = 400
# HEIGHT = 800
# WIDTH = 800

# steps = 250
steps = 1000

map = Map(HEIGHT, WIDTH)
# people = generate_people(160, map)
people = generate_people(640, map)
# people = generate_people(2560, map)

sick_person = list(people.keys())[0]
sick_person.diseases.append(Virus1(sick_person))
sick_person.state = PersonState.DIESASE_HOST_SYMPTOMATIC

starting_state = SimulationState(people, HEIGHT)
start = time.time()
# Simulation(map, starting_state).steps(250, False, True)
Simulation(map, starting_state).steps(steps, False, False)
end = time.time()
print(end - start)