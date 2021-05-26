from dicegame import DiceGame
from constants import Strategy
from dice import Dice
from matplotlib import pyplot as plt

btc_to_nok = 317604.05

strategy_ostekake = {
    Strategy.START_BET: 0.00000005,
    Strategy.ROLL_OVER: 899,
    Strategy.INCREASE_ON_LOSS: 0.1137,
    Strategy.SIMULATIONS: 500000,
    Strategy.MULTIPLIER: 9.8020,
    Strategy.START_BALANCE: 0.0097
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
}

strategy_45 = {
    Strategy.START_BET: 0.0000000,
    Strategy.ROLL_OVER: 550.0,
    Strategy.INCREASE_ON_LOSS: 0.8335,
    Strategy.SIMULATIONS: 20000,
    Strategy.MULTIPLIER: 2.2,
    Strategy.START_BALANCE: 0.00970,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.ADD_TO_BET_ON_FIRST_LOSE_STREAK: 4,
    Strategy.AMOUNT_TO_BET_ON_FIRST_LOSE_STREAK: 0.00000010
}

dice = Dice(seed=None)

game = DiceGame(strategy=strategy_45, dice=dice)

game.run_simulation()

print("Highest loss streak: ", game.highest_lose_streak)
print("Balance: ", game._balance)
print("Profit:", (game._balance - game._strategy[Strategy.START_BALANCE])*btc_to_nok)
plt.plot(game.balance_history)
plt.show()