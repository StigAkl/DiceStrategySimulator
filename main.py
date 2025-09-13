from Strategy.ProfitCondition import ProfitCondition
from Strategy.BetType import BET_TYPE, PROFIT_TYPE
from Strategy.Action import Action
from Strategy.ActionType import ACTION_TYPE
from Strategy.ConditionType import BET_CONDITION_TYPE, PROFIT_CONDITION_TYPE
from Strategy.BetCondition import BetCondition
from beta import DiceGame
from constants import Currency, Strategy
from dice import Dice
from matplotlib import pyplot as plt


strategy_3 = {
    Strategy.START_BET: 0.00009,
    Strategy.ROLL_OVER: 9730,
    Strategy.SIMULATIONS: 5000,
    Strategy.MULTIPLIER: 33,
    Strategy.START_BALANCE: 350,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.CURRENCY: Currency.TRX,
    Strategy.CONDITIONS: [
        BetCondition(BET_CONDITION_TYPE.every, 1, BET_TYPE.WIN,
                     Action(ACTION_TYPE.resetBetAmount)),
        BetCondition(BET_CONDITION_TYPE.firstStreakOf, 10, BET_TYPE.LOSE,
                     Action(ACTION_TYPE.addToBet, 0.0010342)),
        BetCondition(BET_CONDITION_TYPE.every, 20, BET_TYPE.LOSE,
                     Action(ACTION_TYPE.addToBet, 0.0020)),
        ProfitCondition(BET_CONDITION_TYPE.every, 1, BET_TYPE.LOSE,
                        Action(ACTION_TYPE.increaseByPercentage, 0.031))
    ]
}

strategy_50_90 = {
    Strategy.START_BET: 0.0,
    Strategy.ROLL_OVER: 505,
    Strategy.SIMULATIONS: 5000,
    Strategy.MULTIPLIER: 2.0,
    Strategy.START_BALANCE: 16000,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.CURRENCY: Currency.NOK,
    Strategy.CONDITIONS: [
        BetCondition(BET_CONDITION_TYPE.every, 1, BET_TYPE.WIN, Action(ACTION_TYPE.resetBetAmount)), 
        BetCondition(BET_CONDITION_TYPE.every, 1, BET_TYPE.WIN, Action(ACTION_TYPE.resetWinChance)), 
        BetCondition(BET_CONDITION_TYPE.firstStreakOf, 1, BET_TYPE.LOSE, Action(ACTION_TYPE.setRollOver, (100, 1.1))),
        BetCondition(BET_CONDITION_TYPE.streakGreaterThan, 0, BET_TYPE.LOSE, Action(ACTION_TYPE.increaseByPercentage, 13))
    ]
}

strategy_45 = {
    Strategy.START_BET: 0.0,
    Strategy.ROLL_OVER: 550,
    Strategy.SIMULATIONS: 200000,
    Strategy.MULTIPLIER: 2.2,
    Strategy.START_BALANCE: 400000,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.CURRENCY: Currency.NOK,
    Strategy.CONDITIONS: [
        BetCondition(BET_CONDITION_TYPE.every, 1, BET_TYPE.WIN, Action(ACTION_TYPE.resetBetAmount)), 
        BetCondition(BET_CONDITION_TYPE.streakGreaterThan, 1, BET_TYPE.LOSE, Action(ACTION_TYPE.increaseByPercentage, 0.87)),
        BetCondition(BET_CONDITION_TYPE.firstStreakOf, 1, BET_TYPE.LOSE, Action(ACTION_TYPE.setBetAmount, 0.05)), 
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
    print("Wins:", game.wins)
    print("Losses:", game._losses)
    print("Balance: ", game._balance)
    print("Profit:", (game._balance -
          game._strategy[Strategy.START_BALANCE])*game._strategy[Strategy.CURRENCY])
    print("Profitt (Crpt): ", game._balance -
          game._strategy[Strategy.START_BALANCE])

    plot(game.profit_history, "Profit")


def probability_of_bust(strategy, runs=300):
    busts = 0
    totalProfit = 0
    for i in range(0, runs):
        dice = Dice(seed=None)
        game = DiceGame(strategy=strategy, dice=dice)
        game.run_simulation(quiet=True)

        if game._bust:
            busts += 1
        else:
            totalProfit += game._balance - strategy[Strategy.START_BALANCE]

    print("Probability of bust on {} spins: {}".format(
        game._simulations, (busts/runs)*100))
    print("Average profit per run: {}".format(totalProfit/(runs-busts)))


simulate(strategy_45)
#probability_of_bust(strategy_45)
