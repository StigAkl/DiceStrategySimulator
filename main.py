from dicegame import DiceGame
from constants import Strategy
from dice import Dice
from matplotlib import pyplot as plt
import time
import random

strategy_ostekake = {
    Strategy.START_BET: 0.00000006,
    Strategy.ROLL_OVER: 899,
    Strategy.INCREASE_ON_LOSS: 0.1137,
    Strategy.SIMULATIONS: 5000,
    Strategy.MULTIPLIER: 9.8020,
    Strategy.START_BALANCE: 0.0097
}

dice = Dice(seed=None)

for k in range(0, 10):
    lose_streak = 0
    highest_streak = 0
    for i in range(5000):
        value = random.randint(0,1000)

        if value <= 899:
            lose_streak += 1
        else:
            lose_streak = 0

        if lose_streak > highest_streak:
            highest_streak = lose_streak

    game = DiceGame(strategy=strategy_ostekake, dice=dice)
    game.run_simulation(debug=False)
    print(k+1, "Highest streak: ", highest_streak, "/", game.highest_lose_streak)