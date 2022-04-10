import math


def in_range(first_pos, second_pos, distance: float) -> bool:
    return math.sqrt((first_pos.x_pos - second_pos.x_pos) ** 2 + (first_pos.y_pos - second_pos.y_pos) ** 2) < distance


class MapPosition:
    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.x_pos = x
        self.y_pos = y

    def in_range_of(self, second_pos, distance):
        # return math.sqrt((self.x_pos - second_pos.x_pos) + (self.x_pos - second_pos.x_pos)) < distance
        return self.in_range(self, second_pos, distance)

    def __add__(self, delta):
        return MapPosition(self.x_pos + delta[0], self.y_pos + delta[1])

    def __repr__(self) -> str:
        return "[" + str(self.x_pos) + ", " + str(self.y_pos) + "]"


class Map:
    def __init__(self, size_x, size_y, padding: int = 2) -> None:
        super().__init__()
        self.padding = padding
        self.x_min = padding
        self.x_max = size_x - padding
        self.y_min = padding
        self.y_max = size_y - padding

    def on_map(self, new_pos: MapPosition) -> bool:
        return (self.x_min <= new_pos.x_pos < self.x_max) and (self.y_min <= new_pos.y_pos < self.y_max)

    def dimensions(self):
        return (self.x_max - self.x_min, self.y_max - self.y_min)
