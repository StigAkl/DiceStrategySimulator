from Strategy.BetType import BET_TYPE
from Strategy.Action import Action
from Strategy.ActionType import ACTION_TYPE
from Strategy.ConditionType import BET_CONDITION_TYPE
from Strategy.BetCondition import BetCondition
from beta import DiceGame
from constants import Currency, Strategy
from dice import Dice
from matplotlib import pyplot as plt


strategy_45 = {
    Strategy.START_BET: 0.000,
    Strategy.ROLL_OVER: 550,
    Strategy.SIMULATIONS: 1000000,
    Strategy.MULTIPLIER: 2.2,
    Strategy.START_BALANCE: 100000,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.CURRENCY: Currency.NOK,
    Strategy.CONDITIONS: [
        BetCondition(BET_CONDITION_TYPE.every, 1, BET_TYPE.WIN, Action(ACTION_TYPE.resetBetAmount)), 
        BetCondition(BET_CONDITION_TYPE.firstStreakOf, 2, BET_TYPE.LOSE, Action(ACTION_TYPE.setBetAmount, 0.078)),
        BetCondition(BET_CONDITION_TYPE.streakGreaterThan, 2, BET_TYPE.LOSE, Action(ACTION_TYPE.increaseByPercentage, 0.84))
    ]
}

strategy_50_90 = {
    Strategy.START_BET: 0.0003,
    Strategy.ROLL_OVER: 505,
    Strategy.SIMULATIONS: 5000,
    Strategy.MULTIPLIER: 2.0,
    Strategy.START_BALANCE: 24,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.CURRENCY: Currency.NOK,
    Strategy.CONDITIONS: [
        BetCondition(BET_CONDITION_TYPE.every, 1, BET_TYPE.WIN, Action(ACTION_TYPE.resetBetAmount)), 
        BetCondition(BET_CONDITION_TYPE.every, 1, BET_TYPE.WIN, Action(ACTION_TYPE.resetWinChance)), 
        BetCondition(BET_CONDITION_TYPE.firstStreakOf, 1, BET_TYPE.LOSE, Action(ACTION_TYPE.setRollOver, (100, 1.1))),
        BetCondition(BET_CONDITION_TYPE.streakGreaterThan, 0, BET_TYPE.LOSE, Action(ACTION_TYPE.increaseByPercentage, 13))
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
    print("Profitt (Crpt): ", game._balance -
          game._strategy[Strategy.START_BALANCE])

    plot(game.profit_history, "Profit")

simulate(strategy_45)