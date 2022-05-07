from unittest import TestCase

from Person import Person
from SimulationState import SimulationState, MapPosition
from src.Map import Map


class TestSimulationState(TestCase):
    def test_find_neighbors(self):
        map = Map(200, 200)

        p0 = Person(MapPosition(0, 0, map), map)
        p1 = Person(MapPosition(1, 0, map), map)
        p2 = Person(MapPosition(0, 100, map), map)
        people = {p0: MapPosition(0, 0, map), p1: MapPosition(1, 0, map), p2: MapPosition(0, 100, map)}
        simulation_state = SimulationState(people)

        neighbors = simulation_state.find_neighbors(p0)

        self.assert_(p1 in neighbors)
        self.assert_(p2 not in neighbors)
