import random
from enum import Enum
import numpy as np
from Map import MapPosition, Map

PROB = np.concatenate((np.full((1,50), 50)[0], np.arange(50,0,-1)))


class PersonState(Enum):
    DIESASE_FREE = 1
    DIESASE_HOST_ASYMPTOMATIC_NONTRANSMISSABLE = 2
    DIESASE_HOST_ASYMPTOMATIC_TRANSMISSABLE = 3
    DIESASE_HOST_SYMPTOMATIC = 4
    DIESASE_RESISTANT = 5
    DEAD = 6

    def transmissable(self):
        return self.value == PersonState.DIESASE_HOST_ASYMPTOMATIC_TRANSMISSABLE.value or \
               self.value == PersonState.DIESASE_HOST_SYMPTOMATIC.value


class Person:
    def __init__(self, pos: MapPosition, map: Map) -> None:
        self.hasVirus = None  # to be ultimately replaced with list of hosted viruses?
        self.diseases = []
        self.age = random.choices(np.arange(1,101), weights=PROB)[0]
        self.immunity_modifier = random.randint(0, 11)  # positive - better immunity
        self.pos = pos
        self.map = map
        self.dead = False
        self.resistant = False
        self.as_nt = False
        self.as_t = False
        self.general_direction = (random.randint(-1, 2), random.randint(-2, 2))

    def step(self) -> MapPosition:
        x, y = random.randint(-1, 1), random.randint(-1, 1)
        if self.map.on_map(self.pos + (x, y)):
            self.pos += self.general_direction
            self.pos += (x, y)

        if random.random() < 0.05:
            self.general_direction = (random.randint(-2, 2), random.randint(-2, 2))

        if self.diseases:
            self.immunity_modifier += 0.15 - 0.001 * self.age

        for disease in self.diseases:
            disease.step()

        if self.resistant:
            self.days_of_resistance -= 1 
            if self.days_of_resistance == 0:
                self.resistant = False 

        return self.pos, self.dead

    def __repr__(self) -> str:
        return "Person{pos:" + self.pos.__repr__() + "," + "diseases:" + str(self.diseases) + "}"
    
    def resistance(self):
        self.resistant = True
        self.days_of_resistance = random.randint(20,30)
        self.diseases.pop()

    def die(self):
        # print("Person died")
        self.dead = True

    def state(self):
        if self.dead:
            return PersonState.DEAD
        elif self.as_t:
            return PersonState.DIESASE_HOST_ASYMPTOMATIC_TRANSMISSABLE
        elif self.as_nt:
            return PersonState.DIESASE_HOST_ASYMPTOMATIC_NONTRANSMISSABLE
        elif self.resistant:
            return PersonState.DIESASE_RESISTANT
        elif not self.diseases:
            return PersonState.DIESASE_FREE
        return PersonState.DIESASE_HOST_SYMPTOMATIC  # TODO: expand
