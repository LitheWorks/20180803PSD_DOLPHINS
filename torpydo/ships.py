import random
from enum import Enum
from itertools import repeat
from typing import NamedTuple, Optional


class Orientation(Enum):
    HORIZONTAL = 1,
    VERTICAL = 2


class Point(NamedTuple):

    """
    A two-dimensional, Cartesian coordinate.
    """

    x: int
    y: int

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'


class PlayField(object):
    """
    The play field has coordinates from (0,0) in the top-left corner to (width -1, height -1) in the bottom-right.
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @property
    def smallest_dimension(self) -> int:
        return min(self.height, self.width)

    @property
    def top_left(self) -> Point:
        return Point(0, 0)

    @property
    def bottom_right(self) -> Point:
        return Point(self.width - 1, self.height - 1)

    def is_valid_coordinate(self, coord: Point) -> bool:
        return 0 <= coord.x < self.width and 0 <= coord.y < self.height

    def get_random_position(self) -> Point:
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        return Point(x, y)


class Ship(object):
    def __init__(self, name: str, size: int, color: str):
        self.name = name
        self.size = size
        self.color = color
        self._position = None
        self._all_positions = set()
        self._hits = set()

    def receive_fire(self, position: Point) -> bool:
        if position in self.all_positions:
            self._hits.add(position)
            return True
        return False

    def is_alive(self) -> bool:
        return self._hits != self.all_positions

    @property
    def position(self):
        """
        The position of the ship, as a tuple of (Point, Orientation).
        :return: the ship position
        """
        return self._position

    @property
    def damage(self):
        return len(self._hits)

    @property
    def hits(self):
        return self._hits

    @property
    def all_positions(self):
        return self._all_positions

    def overlaps_with(self, ship):
        return self != ship and len(self.all_positions.intersection(ship.all_positions)) > 0

    def update_position(self, anchor: Point, orientation: Orientation):
        """
        Updates the position of the ship. This resets the ship's hits to zero.
        :param anchor: the anchor point.
        :param orientation: the orientation.
        """
        if not (anchor and orientation):
            raise ValueError
        self._position = (anchor, orientation)
        if orientation == Orientation.HORIZONTAL:
            xs = range(anchor.x, anchor.x + self.size)
            ys = repeat(anchor.y, self.size)
        else:
            xs = repeat(anchor.x, self.size)
            ys = range(anchor.y, anchor.y + self.size)
        self._all_positions = {p for p in map(lambda xy: Point(xy[0], xy[1]), zip(xs, ys))}
        self._hits = set()

    def __str__(self):
        return f'{self.name} at {self.position}'


class Fleet(object):
    def __init__(self):
        self.ships = list()

    def __iter__(self):
        return self.ships.__iter__()

    def add_ship(self, name: str, size: int, color: str):
        self.ships.append(Ship(name, size, color))

    def receive_fire(self, position: Point) -> Optional[Ship]:
        for ship in self.ships:
            if ship.receive_fire(position):
                return ship
        return None

    def is_alive(self) -> bool:
        return any(ship.is_alive() for ship in self.ships)

    def random_positioning(self, play_field: PlayField):
        """
        Positions the fleet randomly, modifying the data in-place.
        :param play_field: the field in which to place the fleet
        """
        for ship in self.ships:
            if ship.size > play_field.smallest_dimension:
                raise ValueError("Play Field is too small for ship " + ship.name)
            for _ in range(10000):
                orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
                if orientation == Orientation.HORIZONTAL:
                    x0 = random.randrange(play_field.width - ship.size)
                    y0 = random.choice(range(play_field.height))
                else:
                    x0 = random.choice(range(play_field.width))
                    y0 = random.randrange(play_field.height - ship.size)
                ship.update_position(Point(x0, y0), orientation)
                if not any(ship.overlaps_with(ship2) for ship2 in self.ships):
                    break
            else:
                raise ValueError(f"Unable to position {ship.name} without overlapping any other ship.")

    def total_damage(self):
        return sum(ship.damage for ship in self.ships)

    @staticmethod
    def standard_fleet():
        fleet = Fleet()
        fleet.add_ship("Aircraft Carrier", 5, 'CadetBlue')
        fleet.add_ship("Battleship", 4, 'Red')
        fleet.add_ship("Submarine", 3, 'Chartreuse')
        fleet.add_ship("Destroyer", 3, 'Yellow')
        fleet.add_ship("Patrol Boat", 2, 'Orange')
        return fleet
