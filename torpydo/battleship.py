from typing import List, NamedTuple, Optional, Tuple

from torpydo import TerminationRequested
from torpydo.ships import Fleet, PlayField, Point, Ship
from torpydo.user_interface import AsciiUI, BaseUI

BATTLEFIELD_ROWS = 8
BATTLEFIELD_COLUMNS = 8


class Shot(NamedTuple):
    """
    Records the position and outcome of a shot fired.
    """
    pos: Point
    hit: bool

    def __str__(self) -> str:
        return f'({self.pos.x}, {self.pos.y} {"hit" if self.hit else "miss"})'


class Player(object):
    """
    Represents a player and all their knowledge about the game board.
    """
    def __init__(self, name: str, play_field: PlayField, fleet: Fleet):
        self._name = name
        self._play_field = play_field
        self._fleet = fleet
        self._own_shots = list()
        self._opponent_shots = list()

    def record_shot(self, coordinate: Point, hit: bool):
        self._own_shots.append(Shot(coordinate, hit))

    def receive_fire(self, position: Point) -> Tuple[bool, Optional[Ship]]:
        """
        Reports the damage of an incoming shot.
        :param position: the coordinates of the shot.
        :return: `(False, None)` if the shot missed, `(True, None)` if it hit, `(True, Ship)` if it sank a ship.
        """
        self._opponent_shots.append(position)
        ship = self.fleet.receive_fire(position)
        hit = bool(ship)
        sank = ship if hit and not ship.is_alive() else None
        return hit, sank

    def is_computer(self) -> bool:
        return False

    def get_computer_shot(self) -> Optional[Point]:
        """
        If the player is a computer it should return the `Point` at which it wants to shoot.
        """
        return None

    @property
    def name(self) -> str:
        return self._name

    @property
    def fleet(self) -> Fleet:
        return self._fleet

    @property
    def own_shots(self) -> List[Shot]:
        return self._own_shots

    @property
    def opponent_shots(self) -> List[Point]:
        return self._opponent_shots

    def get_shot_at(self, pos: Point) -> Optional[Shot]:
        for shot in self.own_shots:
            if shot.pos == pos:
                return shot
        return None


class ComputerPlayer(Player):
    """
    A computer player.
    """
    def __init__(self, play_field: PlayField, fleet: Fleet):
        super().__init__("Guessin' Gustavo", play_field, fleet)

    def is_computer(self) -> bool:
        return True

    def get_computer_shot(self) -> Point:
        while True:
            shot = self._play_field.get_random_position()
            if not self.get_shot_at(shot):
                return shot


class BattleshipGame(object):
    """
    BattleshipGame is the Presenter in our model-view-presenter structure, driving all interactions and state changes.
    """
    def __init__(self, play_field: PlayField, user_interface: BaseUI, player_1: Player, player_2: Player):
        self.play_field = play_field
        self.ui = user_interface
        self.player_1 = player_1
        self.player_2 = player_2

    def start(self):
        self.ui.draw_game_started(self.player_1, self.player_2)
        turn_number = 1
        try:
            while self.do_turn(turn_number):
                turn_number += 1
        except TerminationRequested:
            self.ui.draw_game_stopped(self.player_1, self.player_2)
            pass

    def do_turn(self, turn_number):
        self.ui.draw_board(turn_number, self.player_1)
        player_shot = self.ui.get_player_shot(self.player_1)
        hit, sunk_ship = self.player_2.receive_fire(player_shot)
        self.player_1.record_shot(player_shot, hit)
        self.ui.draw_damage(self.player_1, player_shot, hit, sunk_ship)
        if not self.player_2.fleet.is_alive():
            self.ui.draw_victory(turn_number, self.player_1, self.player_2)
            return False

        self.ui.draw_board(turn_number, self.player_2)
        computer_shot = self.ui.get_player_shot(self.player_2)
        hit, sunk_ship = self.player_1.receive_fire(computer_shot)
        self.player_2.record_shot(computer_shot, hit)
        self.ui.draw_damage(self.player_2, computer_shot, hit, sunk_ship)
        if not self.player_1.fleet.is_alive():
            self.ui.draw_victory(turn_number, self.player_2, self.player_1)
            return False
        return True


def start_game():
    play_field = PlayField(BATTLEFIELD_COLUMNS, BATTLEFIELD_ROWS)

    ui = AsciiUI(play_field)

    player_fleet = Fleet.standard_fleet()
    player_fleet.random_positioning(play_field)
    player = Player("Hawk-eyed Human", play_field, player_fleet)

    computer_fleet = Fleet.standard_fleet()
    computer_fleet.random_positioning(play_field)

    # for ship in computer_fleet:
    #     print(ship.name, ",".join(sorted(BaseUI.point_to_col_row(pos) for pos in ship.all_positions)))

    computer = ComputerPlayer(play_field, computer_fleet)

    game = BattleshipGame(play_field, ui, player, computer)
    game.start()


if __name__ == '__main__':
    start_game()
