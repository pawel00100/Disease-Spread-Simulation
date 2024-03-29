import random
from enum import Enum
import numpy as np
from Map import MapPosition, Map

PROB = np.concatenate((np.full((1,50), 50)[0], np.arange(50,0,-1)))

def faster_randint(min, max):
    return random.random()*(max-min) + min

class PersonState(Enum):
    DIESASE_FREE = 'Healthy'
    DIESASE_HOST_ASYMPTOMATIC_NONTRANSMISSABLE = 'Non transmissible'
    DIESASE_HOST_ASYMPTOMATIC_TRANSMISSABLE = 'Transmissible'
    DIESASE_HOST_SYMPTOMATIC = 'Symptomatic'
    DIESASE_RESISTANT = 'Resistant'
    DEAD = 'Dead'

    def transmissable(self):
        return self.value == PersonState.DIESASE_HOST_ASYMPTOMATIC_TRANSMISSABLE.value or \
               self.value == PersonState.DIESASE_HOST_SYMPTOMATIC.value


possible_person_states_names = [e.name for e in PersonState]
possible_person_states_values = [e.value for e in PersonState]


class Person:
    def __init__(self, pos: MapPosition, map: Map, state: PersonState = PersonState.DIESASE_FREE) -> None:
        self.hasVirus = None  # to be ultimately replaced with list of hosted viruses?
        self.diseases = []
        self.age = random.choices(np.arange(1,101), weights=PROB)[0]
        self.immunity_modifier = faster_randint(0, 11)  # positive - better immunity
        self.pos = pos
        self.map = map
        self.state = state
        self.dead = False
        self.general_direction = (faster_randint(-1, 2), faster_randint(-2, 2))

    def step(self) -> MapPosition:
        x, y = faster_randint(-1, 1), faster_randint(-1, 1)
        if self.map.on_map(self.pos + (x, y)):
            self.pos += self.general_direction
            self.pos += (x, y)

        if random.random() < 0.05:
            self.general_direction = (faster_randint(-2, 2), faster_randint(-2, 2))

        for disease in self.diseases:
            if not self.dead:
                disease.step()

        if self.state == PersonState.DIESASE_RESISTANT:
            self.days_of_resistance -= 1
            if self.days_of_resistance == 0:
                self.state = PersonState.DIESASE_FREE

        return self.pos, self.dead

    def __repr__(self) -> str:
        return "Person{pos:" + self.pos.__repr__() + "," + "diseases:" + str(self.diseases) + "}"
    
    def resistance_gained(self):
        self.state = PersonState.DIESASE_RESISTANT
        self.days_of_resistance = faster_randint(20, 30)
        self.diseases.pop()

    def die(self):
        self.dead = True
        self.state = PersonState.DEAD

    def get_inmmunity_modifier(self):
        diesase_count = len(self.diseases)
        if diesase_count > 1:
            return self.immunity_modifier + (diesase_count - 1) * 5
        return  self.immunity_modifier


