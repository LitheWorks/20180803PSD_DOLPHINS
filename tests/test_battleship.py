# Run with python3 -m unittest test_battleship.py
import unittest
from torpydo import ships
from torpydo.ships import Point
from torpydo.ships import Fleet
from torpydo.battleship import Player
from torpydo.battleship import ComputerPlayer, BattleshipGame
from torpydo.user_interface import BaseUI


class TestShip1(unittest.TestCase):
    def setUp(self):
        self.ship = ships.Ship("TestShip", 4, "White")
        self.field = ships.PlayField(4, 4)
        self.fleet = Fleet()
        self.player1 = Player('Bob', self.field, self.fleet)
        self.computer = ComputerPlayer(self.field, self.fleet)
        self.baseUI = BaseUI(self.player1._play_field)
        self.battle = BattleshipGame(self.field, self.baseUI, self.player1, self.computer)

    #
    # def test_battleshipgame_start(self):
    #     def do_turn(self, turn):
    #         return turn
    #
    #     self.battle.do_turn = new.instancemethod(do_turn, self.battle, None)
    #
    #     self.battle.start()

    def test_do_turn(self):
        self.assertTrue(self.battle.do_turn(3) == False)


    def test_is_at(self):
        self.ship.all_positions.add(Point(1, 2))

        self.assertTrue(self.ship.receive_fire(Point(1, 2)))

        self.assertTrue(self.ship.hits)

        self.assertFalse(self.ship.is_alive())

    def test_player_one(self):
        self.assertTrue(self.player1.name == 'Bob')

    def test_check_player_name_match(self):
        self.assertFalse(self.player1.name == self.computer.name)

    def test_check_computer__name_match(self):
        self.assertTrue(self.computer.name != self.player1.name)

    def test_player_one_fleet(self):
        self.assertTrue(self.player1.fleet == self.fleet)

    def test_player_one_is_human(self):
        self.assertFalse(self.player1.is_computer())

    def test_computer_is_alive(self):
        self.assertTrue(self.computer.is_computer())

    def test_battle_player_one(self):
        self.assertTrue(self.battle.player_1 == self.player1)

    def test_battle_computer(self):
        self.assertTrue(self.battle.player_2 == self.computer)


class TestPoint(unittest.TestCase):
    def setUp(self):
        self.point = Point(1, 2)

    def test_str(self):
        self.assertTrue(self.point.__str__() == '(1, 2)')


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = ships.Ship("TestShip", 4, "White")

    def test_is_at(self):
        self.ship.all_positions.add(Point(1, 2))

        self.assertTrue(self.ship.receive_fire(Point(1, 2)))

    def test_receive_fire(self):
        self.assertFalse(self.ship.receive_fire(Point(1, 2)))

    def test_is_alive(self):
        self.ship.all_positions.add(Point(1, 2))
        self.ship._hits.add(Point(1, 2))
        self.assertFalse(self.ship.is_alive())

    def test_is_alive2(self):
        self.ship.all_positions.add(Point(1, 2))
        self.ship._hits.add(Point(1, 3))
        self.assertTrue(self.ship.is_alive())

    def test_overlaps_with(self):
        self.assertFalse(self.ship.overlaps_with(ships.Ship("TestShip", 4, "White")))


class TestPlayField(unittest.TestCase):
    def setUp(self):
        self.playField = ships.PlayField(10, 10)

    def test_is_valid_coordinate(self):
        self.assertTrue(self.playField.is_valid_coordinate(Point(1, 2)))

    def test_is_valid_coordinate2(self):
        self.assertFalse(self.playField.is_valid_coordinate(Point(11, 2)))

    def test_get_random_position(self):
        self.assertTrue(self.playField.get_random_position().x < 10 and self.playField.get_random_position().y < 10)

    def test_get_random_position2(self):
        self.assertFalse(self.playField.get_random_position().x > 10)


class TestFleet(unittest.TestCase):
    def setUp(self):
        self.fleet = ships.Fleet()

    def test_add_ship(self):
        self.fleet.ships.append(ships.Ship("TestShip", 4, "White"))
        self.assertTrue(self.fleet.ships.__len__() == 1)

    def test_receive_fire(self):
        ship = ships.Ship("TestShip", 4, "Black")
        self.assertFalse(self.fleet.receive_fire(Point(1, 2)) == ship)

    def test_receive_fire2(self):
        ship2 = ships.Ship("TestShip2", 4, "White")
        ship2.all_positions.add(Point(1, 2))
        ship2.receive_fire(Point(1, 2))
        self.fleet.ships.append(ship2)
        self.assertFalse(self.fleet.receive_fire(Point(1, 2)) == "TestShip2")


if '__main__' == __name__:
    unittest.main()