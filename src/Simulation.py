from Map import Map, MapPosition
from Person import Person
from SimulationState import SimulationState
import random
from typing import Tuple
from PIL import Image, ImageDraw

HIGH = 300
WIDTH = 300

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
    def __init__(self, num_people) -> None:
        self.map = Map(HIGH, WIDTH)
        self.simulation_state = SimulationState(generate_people(num_people, self.map))
        self.imgs = []

    def step(self):
        self.simulation_state.step()
        # print(self.simulation_state.people)
        img = self.to_image()
        self.imgs.append(img)

    def steps(self, n):
        [self.step() for _ in range(n)]
        self.imgs[0].save('disease_spread.gif', save_all=True, append_images=self.imgs[1:], format='GIF', optimize=False, duration=90)
        
    def to_image(self) -> Image.Image:
        background_color = (0, 0, 0)
        size = (HIGH, WIDTH)
        image = Image.new("RGB", size, background_color)

        def get_color(person: Person):
            red = (255, 0, 0)
            blue = (0, 200, 235)
            green = (0, 205, 0)
            return blue

        for person, pos in self.simulation_state.people.items():
            x = pos.pos.x_pos
            y = pos.pos.y_pos
            padding = self.map.padding
            img = ImageDraw.Draw(image)
            img = img.ellipse([(x-padding, y-padding), (x+padding, y+padding)], get_color(person))
        return image

Simulation(90).steps(500)
