from dicegame import DiceGame
from constants import Strategy
from dice import Dice

strategy_ostekake = {
    Strategy.START_BET: 0.000000006,
    Strategy.ROLL_OVER: 89.90,
    Strategy.INCREASE_ON_LOSS: 0.1137,
    Strategy.SIMULATIONS: 1,
    Strategy.MULTIPLIER: 9.8020
}

dice = Dice()
game = DiceGame(strategy=strategy_ostekake, dice=dice, balance=0.0097)

game.run_simulation()

print(game._bet)