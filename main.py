from Strategy.BetType import BET_TYPE
from Strategy.Action import Action
from Strategy.ActionType import ACTION_TYPE
from Strategy.ConditionType import CONDITION_TYPE
from Strategy.Condition import Condition
from beta import DiceGame
from constants import Currency, Strategy
from dice import Dice
from matplotlib import pyplot as plt

btc_to_nok = 317604.05
trx_to_nok = 0.6

strategy_45 = {
    Strategy.START_BET: 0.5,
    Strategy.ROLL_OVER: 550.0,
    Strategy.SIMULATIONS: 100,
    Strategy.MULTIPLIER: 2.2,
    Strategy.START_BALANCE: 1000,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.CURRENCY: Currency.TRX,
    Strategy.CONDITIONS: [
        Condition(CONDITION_TYPE.streakGreaterThan, 0, BET_TYPE.LOSE, Action(ACTION_TYPE.increaseByPercentage, 0.84)),
        Condition(CONDITION_TYPE.every, 1, BET_TYPE.WIN, Action(ACTION_TYPE.resetBetAmount))
    ]
}

def plot(data, label):
    plt.plot(data, color='k', linestyle='solid', label=label)
    plt.xlabel('Rounds')
    plt.ylabel(label)
    plt.title("Results from {} simulatoins".format(len(data)))
    plt.show()

def simulate(strategy):
    dice = Dice(seed=None)
    game = DiceGame(strategy=strategy, dice=dice)
    x_axis = []

    for i in range(0,5000):
        x_axis.append(i)
        
    game.run_simulation()

    print("Highest loss streak: ", game.highest_lose_streak)
    print("Balance: ", game._balance)
    print("Profit:", (game._balance -
          game._strategy[Strategy.START_BALANCE])*game._strategy[Strategy.CURRENCY])
    print("Profitt (TRX): ", game._balance -
          game._strategy[Strategy.START_BALANCE])

    plot(game.profit_history, "Profit")

simulate(strategy_45)