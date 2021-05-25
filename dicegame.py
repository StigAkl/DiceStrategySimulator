from constants import Strategy
import time 
from matplotlib import pyplot as plt

def print_format(btc):
    return '{:.8f}'.format(btc)

class DiceGame():

    def __init__(self, strategy, dice):

        #Initialisation
        self._strategy = strategy
        self._dice = dice
        self._balance = strategy[Strategy.START_BALANCE]
        self._bet = strategy[Strategy.START_BET]
        self._last_payout = 0
        self._current_game = 0

        #Statistics
        self.lose_streak = 0
        self.highest_lose_streak = 0
        self.accumulated_bet = 0
        self.highest_bet = 0
        self.highest_accumulated_bet = 0
        self.game_no_highest_loss_streak = 0
        self.number_of_bets = 0

        #For plotting
        self.balance_history = []
        self.profit_history = []

    def __set_highest_lose_streak(self):
        if self.highest_lose_streak < self.lose_streak:
            self.highest_lose_streak = self.lose_streak
            self.game_no_highest_loss_streak = self._current_game

    def __update_lose_streak(self):
        self.lose_streak += 1

    def __update_highest_bet(self):
        if self.highest_bet < self._bet:
            self.highest_bet = self._bet

    def __update_balance(self, win):
        if win:
            payout = self._bet * self._strategy[Strategy.MULTIPLIER]
            self._balance = self._balance + payout
            self._last_payout = payout
            self._balance = self._balance - self._bet
        else:
            self._balance = self._balance - self._bet
            
    def __update_highest_accumulated_bet(self):
        if self.accumulated_bet > self.highest_accumulated_bet:
            self.highest_accumulated_bet = self.accumulated_bet

    def __update_stats(self, win):
        if not win:
            self.__update_lose_streak()
        self.__update_highest_bet()            
        self.__set_highest_lose_streak()
        self.number_of_bets += 1

    def __reset_on_win(self, start_bet):
        self._bet = start_bet
        self.lose_streak = 0
        self.accumulated_bet = 0

    def __increase_bet_on_loss(self, increase_on_loss):
        self._bet += round(self._bet*increase_on_loss,8)

    def execute(self):
        self._current_game += 1

        #Stop execution, we lost it all!
        if self._bet > self._balance:
            print("Balance too low")
            return False

        self.accumulated_bet += round(self._bet,8)
        self.__update_highest_accumulated_bet()

        self._dice.roll_dice()
        value = self._dice.get_dice_value()

        win = True if value > self._strategy[Strategy.ROLL_OVER] else False
        
        self.__update_balance(win)
        self.__update_stats(win)

        self.__reset_on_win(self._strategy[Strategy.START_BET]) if win else self.__increase_bet_on_loss(self._strategy[Strategy.INCREASE_ON_LOSS])

        return True

    def run_simulation(self):     
        self.balance_history.append(self._balance)
        self.profit_history.append(self._balance - self._strategy[Strategy.START_BALANCE])   
        for i in range(self._strategy[Strategy.SIMULATIONS]):

            if self.lose_streak == 30:
                self._bet = 0.00000006

            if Strategy.ADD_TO_BET_EVERY in self._strategy:
                if self.number_of_bets % self._strategy[Strategy.ADD_TO_BET_EVERY] == 0 and self.number_of_bets > 0:
                    self._bet += self._strategy[Strategy.AMOUNT_ADD_TO_BET]

            success = self.execute()

            self.balance_history.append(self._balance)
            self.profit_history.append(self._balance - self._strategy[Strategy.START_BALANCE])

            if not success:
                return False

        return True

    def plot_result(self, result, game_no_max_loss): 
        plt.plot(result)
        plt.xticks([0, game_no_max_loss])
        plt.xlabel("Number of games (" + str(self._current_game) + ")")
        plt.show()