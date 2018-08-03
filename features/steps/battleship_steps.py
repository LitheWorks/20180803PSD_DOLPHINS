from behave import given, when, then, step
from torpydo.ships import Ship, Orientation, Point

@given('I have a {ship_length:d} ship on ({x:d},{y:d}) with orientation horizontal')
def step_impl(context, ship_length, x, y):
    context.ship_length = ship_length
    context.ship = Ship('test', ship_length, 'blue')
    context.ship.update_position(Point(x,y), Orientation.HORIZONTAL)

@when('I check if the ship is valid')
def step_impl(context):
    context.success = len(context.ship.all_positions) == context.ship_length

@then('the result should be true')
def step_impl(context):
    assert context.success is True
