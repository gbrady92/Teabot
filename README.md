# Teabot

Teabot is a bot that tells you the status of your teapot so you don't have to
stand up from your desk to check.

It combines a USB postage scale, an educational temperature sensor and a
Rasberry pi to determine which of the TeapotStates in constants.py your teapot
is in.

This implementation is tied to a webserver which acts as a relay between teabot
and Slack so that we can:

* Post alerts to slack when a new teapot has brewed
* Query slack with a / command to determine if any tea is left in the pot

## How does it work?

The states the teapot can be in and the transformations between those states
are encoded as a finite state machine and the readings from the sensors are
converted into those transformations that are then applied to the state
machine to determine the new state every cycle.

## Running Teabot

To run Teabot after setting up the hardware you'll need to:

1) Define the constants in contants.Constants
2) Install the requirements in requirement.txt using pip
3) Run ```./run```
