from typing import Dict
from Map import MapPosition, in_range
from Person import Person, PersonState
from Diesease import Virus1
from src.statistics.StatisticSnapshot import StatisticSnapshot


def count_items(_list):
    return dict((x, _list.count(x)) for x in set(_list))


class WrappedDict:
    def __init__(self, dictionary: Dict[Person, MapPosition], map_size):  # Dict[Person, MapPosition]
        self.dictionary = dictionary

    def items(self):
        return self.dictionary.items()

    def keys(self):
        return self.dictionary.keys()

    def candidates(self, min_x=0, min_y=0, max_x=6, max_y=6):
        return self.dictionary.keys()

    def pop(self, x):
        return self.dictionary.pop(x)

    def __getitem__(self, y):
        return self.dictionary[y]

    def update_pos(self, person, old_pos, new_pos):
        self.dictionary[person] = new_pos


# class WrappedQuadtree:
#     def __init__(self, dictionary: Dict[Person, MapPosition], size=200):  # Dict[Person, MapPosition]
#         self.dictionary = dictionary
#         self.tree = pyqtree._QuadTree
#         for person, pos in dictionary.items():
#             self.tree.insert((pos.x_pos, pos.y_pos), (person, pos))
#
#     def items(self):
#         return self.dictionary.items()
#
#     def keys(self):
#         return self.dictionary.keys()
#
#     def pop(self, x):
#         self.tree.
#         return self.dictionary.pop(x)
#
#     def candidates(self, min_x=0, min_y=0, max_x=6, max_y=6):
#         return self.tree.within_bb(quads.BoundingBox(min_x, min_y, max_x, max_y))
#
#     def __getitem__(self, y):
#         return self.dictionary[y]
#
#     def __setitem__(self, key, value):
#         self.dictionary[key] = value


class Chunk:
    def __init__(self, people=None):
        if people is None:
            people = list()
        self.people = people

    def get_all_people(self):
        return self.people

    def add_person(self, person: Person):
        self.people.append(person)

    def remove_person(self, person: Person):
        self.people.remove(person)


class ChunkedDict:
    def __init__(self, dictionary: Dict[Person, MapPosition], map_size, chunks_per_axis=None):  # Dict[Person, MapPosition]
        self.dictionary = dictionary
        self.chunks_per_axis = chunks_per_axis
        if self.chunks_per_axis is None:
            self.chunks_per_axis = int(map_size / 10)
        self.chunks = []

        for i in range(self.chunks_per_axis):
            list_1d = []
            for j in range(self.chunks_per_axis):
                list_1d.append(Chunk())
            self.chunks.append(list_1d)
        for person, pos in dictionary.items():
            x_chunk = min(int(pos.x_pos // self.chunks_per_axis), self.chunks_per_axis - 1)
            y_chunk = min(int(pos.y_pos // self.chunks_per_axis), self.chunks_per_axis - 1)
            self.chunks[x_chunk][y_chunk].add_person(person)

    def items(self):
        return self.dictionary.items()

    def keys(self):
        return self.dictionary.keys()

    def candidates(self, min_x=0, min_y=0, max_x=6, max_y=6):
        min_x_chunk = max(int(min_x // self.chunks_per_axis) - 1, 0)
        min_y_chunk = max(int(min_y // self.chunks_per_axis) - 1, 0)
        max_x_chunk = min(int(max_x // self.chunks_per_axis), self.chunks_per_axis + 1 - 1)
        max_y_chunk = min(int(max_y // self.chunks_per_axis), self.chunks_per_axis + 1 - 1)

        candidate_list = []
        for i in range(min_x_chunk, max_x_chunk + 1):
            for j in range(min_y_chunk, max_y_chunk + 1):
                candidate_list.extend(self.chunks[i][j].get_all_people())
        # return self.dictionary.keys()
        return candidate_list

    def pop(self, x):
        x_chunk = min(int(x.pos.x_pos // self.chunks_per_axis), self.chunks_per_axis - 1)
        y_chunk = min(int(x.pos.y_pos // self.chunks_per_axis), self.chunks_per_axis - 1)
        self.chunks[x_chunk][y_chunk].remove_person(x)

        return self.dictionary.pop(x)

    def __getitem__(self, y):
        return self.dictionary[y]

    def update_pos(self, person, old_pos, new_pos):
        self.dictionary[person] = new_pos

        old_x_chunk = min(int(old_pos.x_pos // self.chunks_per_axis), self.chunks_per_axis - 1)
        old_y_chunk = min(int(old_pos.y_pos // self.chunks_per_axis), self.chunks_per_axis - 1)
        new_x_chunk = min(int(new_pos.x_pos // self.chunks_per_axis), self.chunks_per_axis - 1)
        new_y_chunk = min(int(new_pos.y_pos // self.chunks_per_axis), self.chunks_per_axis - 1)
        if (old_x_chunk != new_x_chunk) or (old_y_chunk != new_y_chunk):
            self.chunks[old_x_chunk][old_y_chunk].remove_person(person)
            self.chunks[new_x_chunk][new_y_chunk].add_person(person)


class SimulationState:
    def __init__(self, people: Dict[Person, MapPosition], map_size) -> None:
        super().__init__()
        # self.alive_people = people  # to be replaced with better data structure in the future
        # self.alive_people = WrappedDict(people, map_size)
        self.alive_people = ChunkedDict(people, map_size)
        self.dead_people = {}

    def step(self):
        people_dead_in_this_step = {}
        for person, pos in self.alive_people.items():
            new_pos, died = person.step()  # TODO: use observer pattern
            if died:
                people_dead_in_this_step[person] = pos
            self.update_position(person, pos, new_pos)

            if person.state.transmissable():
                self.spread_diesase(person)

        for person, pos in people_dead_in_this_step.items():
            self.remove_person(person)
            self.dead_people[person] = pos

    def spread_diesase(self, person):
        neighbors = self.find_neighbors(person)
        for neighbor in list(neighbors):
            if neighbor.state in [PersonState.DIESASE_RESISTANT, PersonState.DIESASE_HOST_ASYMPTOMATIC_NONTRANSMISSABLE]:
                continue
            host_diesase = person.diseases[0]  # TODO: don't use first virus but most relevant
            if host_diesase.type() not in map(lambda d: d.type(), neighbor.diseases):
                neighbor.diseases.append(host_diesase.clone(neighbor))
                neighbor.state = PersonState.DIESASE_HOST_SYMPTOMATIC

    def find_neighbors(self, person: Person, radius=10):
        predicate = self.find_position_predicate(radius)
        candidates = self.alive_people.candidates(person.pos.x_pos - radius, person.pos.y_pos - radius, person.pos.x_pos + radius, person.pos.y_pos + radius)
        return filter(lambda potential: predicate(person, potential), candidates)

    def find_position(self, person) -> MapPosition:
        return self.alive_people[person]

    # def find_position_predicate(self, distance):
    #     return lambda person: self.find_position(person).

    def find_position_predicate(self, distance):
        return lambda person, potential: in_range(self.find_position(person), self.find_position(potential), distance)

    def update_position(self, person, old_pos, new_position):
        # self.alive_people[person] = new_position
        self.alive_people.update_pos(person, old_pos, new_position)

    def remove_person(self, person):
        self.alive_people.pop(person)

    def all_people(self):
        return list(self.alive_people.keys()) + list(self.dead_people.keys())

    def get_statistic_snapshot(self):
        states = [p.state for p in self.all_people()]
        return StatisticSnapshot(count_items(states))
