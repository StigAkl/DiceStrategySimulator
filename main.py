from dicegame import DiceGame
from constants import Currency, Strategy
from dice import Dice
from matplotlib import pyplot as plt
import numpy as np

btc_to_nok = 317604.05
trx_to_nok = 0.6
ltc_to_nok = 1648.20

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


strategy_45 = {
    Strategy.START_BET: 0.01,
    Strategy.ROLL_OVER: 550.0,
    Strategy.INCREASE_ON_LOSS: 0.84,
    Strategy.SIMULATIONS: 50000,
    Strategy.MULTIPLIER: 2.2,
    Strategy.START_BALANCE: 1000,
    Strategy.IGNORE_OUT_OF_FUNDS: False,
    Strategy.CURRENCY: Currency.TRX
}

def plot_two_axis(data1, data2, label1, label2):
    fig, ax1 = plt.subplots()

    color = 'red'
    ax1.set_xlabel('Rounds')
    ax1.set_ylabel(label1, color=color)
    ax1.plot(data1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'blue'
    ax2.set_ylabel(label2, color=color)  # we already handled the x-label with ax1
    ax2.plot(data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

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


def probability_of_bust(strategy, runs=1000):
    first_bust = 0
    max_balance = 0
    busts = 0
    highest_profit = 0
    highest_lose_streak = 0
    total_profit = 0
    lowest_profit = 0
    num_no_busts = 0
    loss_streak_frequency = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(0, runs):
        dice = Dice(seed=None)
        game = DiceGame(strategy=strategy, dice=dice)
        game.run_simulation(quiet=True)

        loss_streak_frequency[game.highest_lose_streak]+=1

        if game.highest_lose_streak > highest_lose_streak:
            highest_lose_streak = game.highest_lose_streak

        if game._bust:
            busts += 1
            if first_bust == 0:
                first_bust = i
        else:
            if game._balance > max_balance:
                max_balance = game._balance
            if (game._balance-game._strategy[Strategy.START_BALANCE])*game._currency > highest_profit:
                highest_profit = (game._balance-game._strategy[Strategy.START_BALANCE])*game._strategy[Strategy.CURRENCY]
            if (game._balance-game._strategy[Strategy.START_BALANCE])*game._currency < lowest_profit:
                lowest_profit = (game._balance-game._strategy[Strategy.START_BALANCE])*game._currency < lowest_profit
            total_profit += (game._balance-game._strategy[Strategy.START_BALANCE])*game._currency
            num_no_busts += 1
    
    avg_profit = total_profit / num_no_busts

    plt.plot(loss_streak_frequency)
    plt.show()
    return ("Bust percent: {}\nHghest balance: {}\nHighest Profit: {}\nFirst bust: Run number {}\nLargest losing streak: {}\nAvg profit: {}".format((busts/runs)*100,
                                                                                                                             max_balance,
                                                                                                                             highest_profit,
                                                                                                                             first_bust,
                                                                                                                             highest_lose_streak,
                                                                                                                             avg_profit))

#print(probability_of_bust(strategy_45, runs=10000))
simulate(strategy_45)