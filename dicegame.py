from constants import Strategy

class DiceGame():

    def __init__(self, strategy, dice, balance):

        #Initialisation
        self._strategy = strategy
        self._dice = dice
        self._balance = balance
        self._bet = strategy[Strategy.START_BET]

        #Statistics
        self.lose_streak = 0
        self.highest_lose_streak = 0
        self.accumulated_bet = 0
        self.highest_bet = 0

        #For plotting
        self.balance_history = []
        self.profit_history = []

    def __set_highest_lose_streak(self):
        if self.highest_lose_streak < self.lose_streak:
            self.highest_lose_streak = self.lose_streak

    def __reset_on_win(self, start_bet):
        self._bet = start_bet
        self.lose_streak = 0
        self.accumulated_bet = 0

    def __update_lose_streak(self):
        self.lose_streak += 1

    def __update_highest_bet(self):
        if self.highest_bet < self._bet:
            self.highest_bet = self._bet

    def __update_balance(self, win):
        if win:
            self._balance = self._balance + (self._bet * self._strategy[Strategy.MULTIPLIER])
        else:
            self._balance = self._balance - self._bet
            

    def __update_stats(self, win):
        start_bet = self._strategy[Strategy.START_BET]

        self.__update_highest_bet()            

        if win:
            self.__set_highest_lose_streak()
            self.__reset_on_win(start_bet)
        else:
            self.__update_lose_streak()


    def __upate(self):
        value = self._dice.get_dice_value()
        win = True if value > self._strategy[Strategy.ROLL_OVER] else False

        self.__update_balance(win)
        self.__update_stats(win)

    def run_simulation(self):        
        for i in range(self._strategy[Strategy.SIMULATIONS]):
            self._dice.roll_dice()
            self.__upate()