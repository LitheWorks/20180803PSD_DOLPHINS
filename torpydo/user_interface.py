import string
from typing import Optional

from torpydo import asciiart, TerminationRequested
from torpydo.ships import PlayField, Point, Ship, Orientation


class BaseUI(object):
    def __init__(self, play_field: PlayField):
        self.play_field = play_field

    def draw_board(self, turn_number: int, player):
        pass

    def draw_damage(self, shooter, shot: Point, hit: bool, sunk_ship: Optional[Ship]):
        pass

    def draw_victory(self, turn_number: int, victor, loser):
        pass

    def get_player_shot(self, player) -> Point:
        pass

    def draw_game_started(self, player_1, player_2):
        pass

    def draw_game_stopped(self, player_1, player_2):
        pass

    @staticmethod
    def point_to_col_row(point: Point):
        """
        Converts a point such as `Point(1, 3)` to the corresponding col_row such as `'B4'`.
        """
        return "".join([string.ascii_uppercase[point.x], str(point.y + 1)])

    def col_row_to_point(self, input_str):
        """
        Converts a col_row such as `'D1'` to the corresponding point such as `Point(5, 0)`.
        """
        try:
            letter = input_str[0].upper()
            x = string.ascii_uppercase.index(letter)
            y = int(input_str[1:]) - 1
            p = Point(x, y)
            if self.play_field.is_valid_coordinate(p):
                return p
        except IndexError:
            pass
        except ValueError:
            pass
        return None


class AsciiUI(BaseUI):
    SPACER = '    '

    def __init__(self, play_field: PlayField):
        super().__init__(play_field)
        self.numbers_column = f"{{:{len(str(play_field.height))}d}} "
        self.numbers_spacer = " " * (1 + len(str(play_field.height)))

    def draw_game_started(self, player_1, player_2):
        print(asciiart.ASCII_BATTLESHIP)
        print()
        fight_title = f'The battle between {player_1.name} and {player_2.name}'
        print(asciiart.ASCII_DIVIDER)
        print(fight_title)
        print(asciiart.ASCII_DIVIDER)
        print()

    def draw_board(self, turn_number: int, player):
        if player.is_computer():
            pass
        else:
            print()
            print(f"{player.name}, turn #{turn_number}")
            cols = string.ascii_uppercase[:self.play_field.width]
            print(self.numbers_spacer, cols, self.SPACER, self.numbers_spacer, cols, sep='')
            for y in range(self.play_field.height):
                print(self.numbers_column.format(y + 1), end='')
                for x in range(self.play_field.width):
                    shot = player.get_shot_at(Point(x, y))
                    if shot:
                        print('*' if shot.hit else '○', end='')
                    else:
                        print('·', end='')
                print(self.SPACER, self.numbers_column.format(y + 1), sep='', end='')
                for x in range(self.play_field.width):
                    pos = Point(x, y)
                    oppo = pos in player.opponent_shots
                    char = '○' if oppo else '·'
                    for ship in player.fleet:
                        if pos in ship.all_positions:
                            char = '*' if oppo else '═' if ship.position[1] == Orientation.HORIZONTAL else '║'
                    print(char, end='')
                print()


    def draw_damage(self, shooter, shot: Point, hit: bool, sunk_ship: Optional[Ship]):
        if sunk_ship:
            print(f"{shooter.name} fired at {self.point_to_col_row(shot)} and SANK a {sunk_ship.name}!")
        else:
            print(f"{shooter.name} fired at {self.point_to_col_row(shot)} and {'hit' if hit else 'missed'}!")

    def draw_victory(self, turn_number: int, victor, loser):
        print()
        print(f"{victor.name}'s mighty fleet vanquished {loser.name} in turn {turn_number}!")

    def draw_game_stopped(self, player_1, player_2):
        print("The game ended before either fleet was completely defeated.")
        print(f"{player_1.name} hit {player_2.name}'s ships {player_2.fleet.total_damage()} time(s).")
        print(f"{player_2.name} hit {player_1.name}'s ships {player_1.fleet.total_damage()} time(s).")

    def get_player_shot(self, player) -> Point:
        # See if we fire an automated shot
        if player.is_computer():
            return player.get_computer_shot()

        # Otherwise get a shot from user input
        print("Player, it's your turn.")
        try:
            player_shot = None
            while player_shot is None:
                input_value = input('Please enter a coordinate between {} and {}, or CTRL-D to quit: '.format(
                    AsciiUI.point_to_col_row(self.play_field.top_left),
                    AsciiUI.point_to_col_row(self.play_field.bottom_right)))
                player_shot = self.col_row_to_point(input_value)
            print()
            return player_shot
        except EOFError:
            raise TerminationRequested()
