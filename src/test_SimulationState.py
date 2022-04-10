from unittest import TestCase
from Person import Person
from SimulationState import SimulationState, MapPosition


class TestSimulationState(TestCase):
    def test_find_neighbors(self):
        p0 = Person(MapPosition(0,0))
        p1 = Person(MapPosition(1,0))
        p2 = Person(MapPosition(0,100))
        people = {p0: MapPosition(0,0), p1: MapPosition(1,0), p2: MapPosition(0,100)}
        simulation_state = SimulationState(people)

        neighbors = simulation_state.find_neighbors(p0)

        self.assert_(p1 in neighbors)
        self.assert_(p2 not in neighbors)
