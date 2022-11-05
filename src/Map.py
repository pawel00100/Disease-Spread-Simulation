import math


def in_range(first_pos, second_pos, distance: float) -> bool:
    x = (first_pos.x_pos - second_pos.x_pos)
    y = (first_pos.y_pos - second_pos.y_pos)
    return (x * x + y * y) < distance * distance


class MapPosition:
    def __init__(self, x: float, y: float, map) -> None:
        # super().__init__()
        self.x_pos = x
        self.y_pos = y
        self.map = map

    def in_range_of(self, second_pos, distance):
        # return math.sqrt((self.x_pos - second_pos.x_pos) + (self.x_pos - second_pos.x_pos)) < distance
        return self.in_range(self, second_pos, distance)

    def __add__(self, delta):
        new_x, new_y = self.x_pos + delta[0], self.y_pos + delta[1]
        new_x, new_y = new_x % self.map.x_max, new_y % self.map.y_max
        return MapPosition(new_x, new_y, self.map)

    def __repr__(self) -> str:
        return "(" + str(self.x_pos) + ", " + str(self.y_pos) + ")"


class Map:
    def __init__(self, size_x: int, size_y: int) -> None:
        super().__init__()
        self.x_min = 0
        self.x_max = size_x
        self.y_min = 0
        self.y_max = size_y

    def on_map(self, new_pos: MapPosition) -> bool:
        return (self.x_min <= new_pos.x_pos < self.x_max) and (self.y_min <= new_pos.y_pos < self.y_max)

    def dimensions(self):
        return (self.x_max, self.y_max)
