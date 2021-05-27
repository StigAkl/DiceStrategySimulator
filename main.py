from dicegame import DiceGame
from constants import Currency, Strategy
from dice import Dice
from matplotlib import pyplot as plt
plt.style.use('classic')

btc_to_nok = 317604.05
trx_to_nok = 0.6

strategy_ostekake = {
    Strategy.START_BET: 0.00000005,
    Strategy.ROLL_OVER: 899,
    Strategy.INCREASE_ON_LOSS: 0.1137,
    Strategy.SIMULATIONS: 500000,
    Strategy.MULTIPLIER: 9.8020,
    Strategy.START_BALANCE: 0.0097,
    Strategy.CURRENCY: Currency.BTC
}

strategy_65 = {
    Strategy.START_BET: 0.00000005,
    Strategy.ROLL_OVER: 550.0,
    Strategy.INCREASE_ON_LOSS: 0.65,
    Strategy.SIMULATIONS: 10000,
    Strategy.MULTIPLIER: 1.8,
    Strategy.START_BALANCE: 0.000608,
    Strategy.CURRENCY: Currency.BTC
}

strategy_33 = {
    Strategy.START_BET: 0.00000005,
    Strategy.ROLL_OVER: 970.0,
    Strategy.INCREASE_ON_LOSS: 0.0350,
    Strategy.SIMULATIONS: 5000,
    Strategy.MULTIPLIER: 33.0,
    Strategy.START_BALANCE: 0.00970,
    Strategy.CURRENCY: Currency.BTC
}


strategy_3 = {
    Strategy.START_BET: 0.00000005,
    Strategy.ROLL_OVER: 970,
    Strategy.INCREASE_ON_LOSS: 0.033,
    Strategy.SIMULATIONS: 10000,
    Strategy.MULTIPLIER: 33,
    Strategy.START_BALANCE: 0.0097,
    Strategy.ADD_EVERY_BET: 20,
    Strategy.ADD_AMOUNT_EVERY_BET: 0.00000005,
    Strategy.CURRENCY: Currency.BTC
}

strategy_49 = {
    Strategy.START_BET: 0.00005000,
    Strategy.ROLL_OVER: 505,
    Strategy.INCREASE_ON_LOSS: 1.01,
    Strategy.SIMULATIONS: 10000,
    Strategy.MULTIPLIER: 2.0,
    Strategy.START_BALANCE: 997,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.ADD_TO_BET_ON_FIRST_LOSE_STREAK: 3,
    Strategy.AMOUNT_TO_BET_ON_FIRST_LOSE_STREAK: 0.01048576,
    Strategy.CURRENCY: Currency.BTC
}

strategy_45 = {
    Strategy.START_BET: 0.0,
    Strategy.ROLL_OVER: 550.0,
    Strategy.INCREASE_ON_LOSS: 0.8616,
    Strategy.SIMULATIONS: 5000,
    Strategy.MULTIPLIER: 2.2,
    Strategy.START_BALANCE: 1000,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.ADD_TO_BET_ON_FIRST_LOSE_STREAK: 5,
    Strategy.AMOUNT_TO_BET_ON_FIRST_LOSE_STREAK: 0.0222458,
    Strategy.CURRENCY: Currency.TRX
}


def simulate(strategy):
    dice = Dice(seed=None)
    game = DiceGame(strategy=strategy, dice=dice)

    game.run_simulation()

    print("Highest loss streak: ", game.highest_lose_streak)
    print("Balance: ", game._balance)
    print("Profit:", (game._balance -
          game._strategy[Strategy.START_BALANCE])*Currency.TRX)

    fig, ax = plt.subplots()
    ax.ticklabel_format(useOffset=False)
    plt.plot(game.balance_history)

    plt.show()


def probability_of_bust(strategy, runs=1000):

    first_bust = 0
    max_balance = 0
    busts = 0
    highest_profit = 0
    highest_lose_streak = 0

    for i in range(0, runs):
        dice = Dice(seed=None)
        game = DiceGame(strategy=strategy, dice=dice)
        game.run_simulation(quiet=True)

        if game.highest_lose_streak > highest_lose_streak:
            highest_lose_streak = game.highest_lose_streak

        if game._bust:
            busts += 1
            if first_bust == 0:
                first_bust = i
        else:
            if game._balance > max_balance:
                max_balance = game._balance
            if game._balance-game._strategy[Strategy.START_BALANCE] > highest_profit:
                highest_profit = (
                    game._balance-game._strategy[Strategy.START_BALANCE])*trx_to_nok

    return ("Bust percent: {}\nHghest balance: {}\nProfit: {}\nFirst bust: Run number {}.\nLargest losing streak: {}".format((busts/runs)*100,
                                                                                                                             max_balance,
                                                                                                                             highest_profit,
                                                                                                                             first_bust,
                                                                                                                             highest_lose_streak))


print(probability_of_bust(strategy_45))
# simulate(strategy_45)
