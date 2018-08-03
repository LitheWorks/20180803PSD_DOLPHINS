Feature: IsShipValid
	In order to avoid cheeting
	As a player
	I want to be notified if my ship has a invalid placement

Scenario: Valid ship placement
    Given I have a 5 ship on (1,1) with orientation horizontal
	When I check if the ship is valid
	Then the result should be true
