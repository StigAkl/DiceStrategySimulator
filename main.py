from dicegame import DiceGame
from constants import Strategy
from dice import Dice
from matplotlib import pyplot as plt
import time
import random

strategy_ostekake = {
    Strategy.START_BET: 0.00000000,
    Strategy.ROLL_OVER: 899,
    Strategy.INCREASE_ON_LOSS: 0.1137,
    Strategy.SIMULATIONS: 1000000,
    Strategy.MULTIPLIER: 9.8020,
    Strategy.START_BALANCE: 0.000614
}

strategy_65 = {
    Strategy.START_BET: 0.00000005,
    Strategy.ROLL_OVER: 550.0,
    Strategy.INCREASE_ON_LOSS: 0.65,
    Strategy.SIMULATIONS: 10000,
    Strategy.MULTIPLIER: 1.8,
    Strategy.START_BALANCE: 0.000608
}

strategy_33 = {
    Strategy.START_BET: 0.00000005,
    Strategy.ROLL_OVER: 970.0,
    Strategy.INCREASE_ON_LOSS: 0.0350,
    Strategy.SIMULATIONS: 5000,
    Strategy.MULTIPLIER: 33.0,
    Strategy.START_BALANCE: 0.00970,
    Strategy.ADD_TO_BET_EVERY: 20,
    Strategy.AMOUNT_ADD_TO_BET: 0.00000100
}

dice = Dice(seed=None)

game = DiceGame(strategy=strategy_ostekake, dice=dice)
game.run_simulation()
print("Highest acc bet: ", game.highest_accumulated_bet)
print("Acc bet: ", game.accumulated_bet)
print("Highest lose streak: ", game.highest_lose_streak)
print("Balance: ", '{:.8f}'.format(game._balance))
game.plot_result(game.profit_history, game.game_no_highest_loss_streak)
