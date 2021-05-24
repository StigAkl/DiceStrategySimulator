from constants import Strategy
import time 

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

        #Statistics
        self.lose_streak = 0
        self.highest_lose_streak = 0
        self.accumulated_bet = 0
        self.highest_bet = 0
        self.highest_accumulated_bet = 0

        #For plotting
        self.balance_history = []
        self.profit_history = []

    def __set_highest_lose_streak(self):
        if self.highest_lose_streak < self.lose_streak:
            self.highest_lose_streak = self.lose_streak

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
        else:
            self._balance = self._balance - self._bet
            
    def __update_highest_accumulated_bet(self):
        if self.accumulated_bet > self.highest_accumulated_bet:
            self.highest_accumulated_bet = self.accumulated_bet

    def __update_stats(self, win):
        if not win:
            self.__update_lose_streak()
        self.__update_highest_bet()            
        self.__update_highest_accumulated_bet()
        self.__set_highest_lose_streak()

    def __reset_on_win(self, start_bet):
        self._bet = start_bet
        self.lose_streak = 0
        self.accumulated_bet = 0

    def __increase_bet_on_loss(self, increase_on_loss):
        self._bet += self._bet*increase_on_loss

    def __upate(self):
        #Stop execution, we lost it all!
        if self._bet > self._balance:
            print("Balance too low")
            return False

        self.accumulated_bet += self._bet

        value = self._dice.get_dice_value()
        win = True if value > self._strategy[Strategy.ROLL_OVER] else False

        self.__update_balance(win)
        self.__update_stats(win)

        if win:
            self.__reset_on_win(self._strategy[Strategy.START_BET])
        else:
            self.__increase_bet_on_loss(self._strategy[Strategy.INCREASE_ON_LOSS])

        return True

    def run_simulation(self, debug=False):        
        for i in range(self._strategy[Strategy.SIMULATIONS]):
            self._dice.roll_dice()

            if debug:
                self.__print_debug_information()

            success = self.__upate()

            if not success:
                return False

        return True

    def __print_debug_information(self):
        print("Lose streak", self.lose_streak)
        print("Balance", print_format(self._balance))
        print("Bet", print_format(self._bet))
        print("Highest lose streak", self.highest_lose_streak)
        print("Highest bet", print_format(self.highest_bet))
        print("Last payout: ", print_format(self._last_payout))
        print("Dice: ", self._dice.get_dice_value())
        print()
        time.sleep(1.5)