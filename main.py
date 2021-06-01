from Strategy.BetType import BET_TYPE
from Strategy.Action import Action
from Strategy.ActionType import ACTION_TYPE
from Strategy.ConditionType import BET_CONDITION_TYPE
from Strategy.BetCondition import BetCondition
from beta import DiceGame
from constants import Currency, Strategy
from dice import Dice
from matplotlib import pyplot as plt

btc_to_nok = 317604.05
trx_to_nok = 0.6

strategy_45 = {
    Strategy.START_BET: 0.000,
    Strategy.ROLL_OVER: 550,
    Strategy.SIMULATIONS: 23000,
    Strategy.MULTIPLIER: 2.2,
    Strategy.START_BALANCE: 1000,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.CURRENCY: Currency.TRX,
    Strategy.CONDITIONS: [
        BetCondition(BET_CONDITION_TYPE.every, 1, BET_TYPE.WIN,
                     Action(ACTION_TYPE.resetBetAmount)),
        BetCondition(BET_CONDITION_TYPE.firstStreakOf, 3, BET_TYPE.LOSE,
                     Action(ACTION_TYPE.setBetAmount, 0.02097152)),
        BetCondition(BET_CONDITION_TYPE.streakGreaterThan, 3,
                     BET_TYPE.LOSE, Action(ACTION_TYPE.increaseByPercentage, 0.8518))
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

    game.run_simulation()

    print("Highest loss streak: ", game.highest_lose_streak)
    print("Balance: ", game._balance)
    print("Profit:", (game._balance -
          game._strategy[Strategy.START_BALANCE])*game._strategy[Strategy.CURRENCY])
    print("Profitt (TRX): ", game._balance -
          game._strategy[Strategy.START_BALANCE])

    plot(game.profit_history, "Profit")


simulate(strategy_45)
