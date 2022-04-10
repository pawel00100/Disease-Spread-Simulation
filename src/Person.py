from Map import MapPosition, Map
import random

class Person:
    def __init__(self, pos: MapPosition, map: Map) -> None:
        self.hasVirus = None # to be ultimately replaced with list of hosted viruses?
        self.dieseases = []
        self.age = None
        self.pos = pos
        self.map = map

    def step(self) -> MapPosition:
        x, y = random.randint(-1, 1), random.randint(-1, 1)
        if self.map.on_map(self.pos + (x, y)):
            self.pos += (x, y)
        return self

    def __repr__(self) -> str:
        return "Person at pos " + self.pos.__repr__()

class Diesease:
    def __init__(self) -> None:
        super().__init__()
        self.host = None # only for host information - not mutable
        self.date_caught = None # date - possibly not needed
        self.severity = 0.0
        self.gained_immunity = 0.0
