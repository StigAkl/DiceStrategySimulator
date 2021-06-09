from constants import Strategy
import time
from matplotlib import pyplot as plt


def print_format(btc):
    return '{:.8f}'.format(btc)


class DiceGame():
    def __init__(self, strategy, dice):
        # Initialisation
        self._strategy = strategy
        self._dice = dice
        self._balance = strategy[Strategy.START_BALANCE]
        self._bet = strategy[Strategy.START_BET]
        self._simulations = strategy[Strategy.SIMULATIONS]
        self._roll_over = strategy[Strategy.ROLL_OVER]
        self._multiplier = strategy[Strategy.MULTIPLIER]
        self._increase_on_loss = strategy[Strategy.INCREASE_ON_LOSS]
        self._start_bet = strategy[Strategy.START_BET]
        self._ignore_out_of_funds = False if not Strategy.IGNORE_OUT_OF_FUNDS in strategy else strategy[
            Strategy.IGNORE_OUT_OF_FUNDS]
        self.set_bet_on_lose_streak = strategy[Strategy.ADD_TO_BET_ON_FIRST_LOSE_STREAK] if Strategy.ADD_TO_BET_ON_FIRST_LOSE_STREAK in strategy else 0
        self.amount_on_lose_streak = strategy[Strategy.AMOUNT_TO_BET_ON_FIRST_LOSE_STREAK] if Strategy.AMOUNT_TO_BET_ON_FIRST_LOSE_STREAK in strategy else 0
        self._currency = strategy[Strategy.CURRENCY]

        # Add every bet
        self.add_every_bet = strategy[Strategy.ADD_EVERY_BET] if Strategy.ADD_EVERY_BET in strategy else 0
        self.add_amount_every_bet = strategy[Strategy.ADD_AMOUNT_EVERY_BET] if Strategy.ADD_AMOUNT_EVERY_BET in strategy else 0

        # Statistics
        self.lose_streak = 0
        self.highest_lose_streak = 0
        self.accumulated_bet = 0
        self.highest_bet = 0
        self.highest_accumulated_bet = 0
        self.game_no_highest_loss_streak = 0
        self._last_payout = 0
        self._current_game = 0
        self._bust = False

        # For plotting
        self.balance_history = []
        self.profit_history = []
        self._bet_history = []
        self._accumulated_bet_history = []

    def execute(self):
        self._balance -= self._bet
        self.accumulated_bet += self._bet
        value = self._dice.get_dice_value()

        if value > self._roll_over:
            self.__win()
        else:
            self.__lose()

    def __win(self):
        self._balance += self._bet*self._multiplier
        self.lose_streak = 0
        self.accumulated_bet = 0
        self._bet = self._start_bet

    def __lose(self):
        self.lose_streak += 1
        increase = round(self._bet*self._increase_on_loss, ndigits=8)
        self._bet += increase
        if self.lose_streak > self.highest_lose_streak:
            self.highest_lose_streak = self.lose_streak

    def run_simulation(self, quiet=False):
        # Game loop
        for i in range(self._strategy[Strategy.SIMULATIONS]):
            if self._bet > self._balance and not self._ignore_out_of_funds:
                if self._balance > 0:
                    self._bet = self._balance
                else:
                    if not quiet:
                        print("Out of funds")
                        print("Balance:", self._balance)
                        print("Current bet:", self._bet)
                        print("Number of rolls:", self._current_game)
                    self._bust = True
                    break

            # Update game count
            self._current_game += 1

            # Set advanced bet rules
            if self.set_bet_on_lose_streak > 0 and self.lose_streak == self.set_bet_on_lose_streak:
                self._bet = self.amount_on_lose_streak
            if self.add_every_bet > 0 and self._current_game % self.add_every_bet == 0:
                self._bet += self.add_amount_every_bet

            # Roll dice
            self._dice.roll_dice()

            #Update plot data
            self._bet_history.append(self._bet)
            self.balance_history.append(round(self._balance, 8))
            self.profit_history.append(
                self._balance - self._strategy[Strategy.START_BALANCE])
            self._accumulated_bet_history.append(self.accumulated_bet)

            # Execute main logic
            self.execute()
