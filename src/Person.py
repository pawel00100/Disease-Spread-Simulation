from src.Map import MapPosition
import random

class Person:
    def __init__(self, pos: MapPosition) -> None:
        self.hasVirus = None # to be ultimately replaced with list of hosted viruses?
        self.dieseases = []
        self.age = None
        self.pos = pos

    def step(self) -> MapPosition:
        self.pos += (random.randint(-1,1), random.randint(-1,1)) #TODO make sure is in boundaies
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
