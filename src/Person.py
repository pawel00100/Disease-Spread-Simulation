import random
from enum import Enum

from Map import MapPosition, Map


class PersonState(Enum):
    DIESASE_FREE = 1
    DIESASE_HOST_ASYMPTOMATIC_NONTRANSMISSABLE = 2
    DIESASE_HOST_ASYMPTOMATIC_TRANSMISSABLE = 3
    DIESASE_HOST_SYMPTOMATIC = 4
    DEAD = 5

    def transmissable(self):
        return self.value == PersonState.DIESASE_HOST_ASYMPTOMATIC_TRANSMISSABLE.value or \
               self.value == PersonState.DIESASE_HOST_SYMPTOMATIC.value


class Person:
    def __init__(self, pos: MapPosition, map: Map) -> None:
        self.hasVirus = None  # to be ultimately replaced with list of hosted viruses?
        self.diseases = []
        self.age = 25
        self.immunity_modifier = 0.0  # positive - better immunity
        self.pos = pos
        self.map = map
        self.dead = False
        self.general_direction = (random.randint(-1, 2), random.randint(-2, 2))

    def step(self) -> MapPosition:
        x, y = random.randint(-1, 1), random.randint(-1, 1)
        if self.map.on_map(self.pos + (x, y)):
            self.pos += self.general_direction
            self.pos += (x, y)

        if random.random() < 0.05:
            self.general_direction = (random.randint(-2, 2), random.randint(-2, 2))

        for disease in self.diseases:
            disease.step()

        return self.pos, self.dead

    def __repr__(self) -> str:
        return "Person{pos:" + self.pos.__repr__() + "," + "diseases:" + str(self.diseases) + "}"

    def die(self):
        print("Person died")
        self.dead = True

    def state(self):
        if self.dead:
            return PersonState.DEAD
        if not self.diseases:
            return PersonState.DIESASE_FREE
        return PersonState.DIESASE_HOST_SYMPTOMATIC  # TODO: expand
