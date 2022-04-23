from PIL import Image, ImageDraw

from Map import Map
from Person import Person, PersonState
from SimulationState import SimulationState

red = (185, 0, 0)
pink = (255, 115, 220)
lightpink = (255, 182, 193)
blue = (0, 200, 235)
green = (0, 205, 0)


def to_image(simulation_state: SimulationState, map: Map) -> Image.Image:
    background_color = (0, 0, 0)
    size = map.dimensions()
    image = Image.new("RGB", size, background_color)

    def get_color(person: Person):
        states_colors = {
            PersonState.DIESASE_FREE: green,
            PersonState.DIESASE_RESISTANT: blue,
            PersonState.DIESASE_HOST_ASYMPTOMATIC_NONTRANSMISSABLE: lightpink,
            PersonState.DIESASE_HOST_ASYMPTOMATIC_TRANSMISSABLE: pink,
            PersonState.DIESASE_HOST_SYMPTOMATIC: red,
        }
        return states_colors[person.state]

    for person, pos in simulation_state.people.items():
        x = pos.x_pos
        y = pos.y_pos
        padding = 2
        img = ImageDraw.Draw(image)
        img = img.ellipse([(x - padding, y - padding), (x + padding, y + padding)], get_color(person))
    return image


class ImageGenerator:
    def __init__(self) -> None:
        self.imgs = []

    def add_state(self, simulation_state: SimulationState, map: Map):
        image = to_image(simulation_state, map)
        self.imgs.append(image)

    def save_image(self):
        self.imgs[0].save('disease_spread.gif', save_all=True, append_images=self.imgs[1:], format='GIF', optimize=False, duration=90)
