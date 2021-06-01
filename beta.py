from Strategy.Action import Action
from Strategy.BetCondition import BetCondition
from Strategy.ConditionType import BET_CONDITION_TYPE
from Strategy.BetType import BET_TYPE
from Strategy.ActionType import ACTION_TYPE
from constants import Strategy


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
        self._start_bet = strategy[Strategy.START_BET]
        self._ignore_out_of_funds = False if not Strategy.IGNORE_OUT_OF_FUNDS in strategy else strategy[
            Strategy.IGNORE_OUT_OF_FUNDS]
        self._conditions = strategy[Strategy.CONDITIONS]

        # Statistics
        self.lose_streak = 0
        self.highest_lose_streak = 0
        self.accumulated_bet = 0
        self.highest_bet = 0
        self.highest_accumulated_bet = 0
        self.game_no_highest_loss_streak = 0
        self._last_payout = 0
        self._current_game = 0
        self.wins = 0
        self.win_streak = 0
        self._losses = 0
        self._bust = False

        # For plotting
        self.balance_history = []
        self.profit_history = []
        self._bet_history = []
        self._accumulated_bet_history = []

    def perform_action(self, action: Action):
        actionType = action._type

        if actionType == ACTION_TYPE.increaseByPercentage:
            self._bet += round(self._bet*action._value, ndigits=8)

        if actionType == ACTION_TYPE.resetBetAmount:
            self._bet = round(self._start_bet, ndigits=8)

        if actionType == ACTION_TYPE.setBetAmount:
            self._bet = round(action._value, ndigits=8)

    def execute_lose_conditions(self):
        for i in range(0, len(self._conditions)):
            condition: BetCondition = self._conditions[i]
            if condition._bet_type == BET_TYPE.LOSE:

                # Perform conditions on loss
                if condition._conditionType == BET_CONDITION_TYPE.every and self._losses % condition._value == 0:
                    self.perform_action(condition._action)

                if condition._conditionType == BET_CONDITION_TYPE.streakGreaterThan and self.lose_streak > condition._value:
                    self.perform_action(condition._action)

                if condition._conditionType == BET_CONDITION_TYPE.firstStreakOf and self.lose_streak == condition._value:
                    self.perform_action(condition._action)

                if condition._conditionType == BET_CONDITION_TYPE.everyStreakOf and self.lose_streak > 0 and self.lose_streak % condition._value == 0:
                    self.perform_action(condition._action)

    def execute_win_conditions(self):
        for i in range(0, len(self._conditions)):
            condition: BetCondition = self._conditions[i]
            if condition._bet_type == BET_TYPE.WIN:

                # Perform conditions on win
                if condition._conditionType == BET_CONDITION_TYPE.every and self.wins % condition._value == 0:
                    self.perform_action(condition._action)
                if condition._conditionType == BET_CONDITION_TYPE.streakGreaterThan and self.win_streak > condition._value:
                    self.perform_action(condition._action)

    def execute(self):
        self._balance -= self._bet
        self.accumulated_bet += self._bet
        value = self._dice.get_dice_value()

        if value >= self._roll_over:
            self.__win()
        else:
            self.__lose()

    def __win(self):
        self._balance += round(self._bet*self._multiplier, ndigits=8)
        self.lose_streak = 0
        self.accumulated_bet = 0
        self.wins += 1
        self.win_streak += 1
        self.execute_win_conditions()

    def __lose(self):
        self.lose_streak += 1
        self.win_streak = 0
        self._losses += 1
        if self.lose_streak > self.highest_lose_streak:
            self.highest_lose_streak = self.lose_streak
        self.execute_lose_conditions()

    def perform_game_loop(self, quiet: bool):
        if self._balance >= 1500:
            print("Reached profit goal in {} spins".format(self._current_game))
            return False
        if self._bet > self._balance and not self._ignore_out_of_funds:
            if not quiet:
                print("Out of funds")
                print("Number of rolls:", self._current_game)
            self._bust = True
            return False

        # Update game count
        self._current_game += 1

        # Roll dice
        self._dice.roll_dice()

        # Update plot data
        self._bet_history.append(self._bet)
        self.balance_history.append(round(self._balance, 8))
        self.profit_history.append(
            self._balance - self._strategy[Strategy.START_BALANCE])
        self._accumulated_bet_history.append(self.accumulated_bet)

        # Execute main logic
        self.execute()
        return True

    def run_simulation(self, quiet=False):
        if self._simulations > 0:
            for i in range(self._strategy[Strategy.SIMULATIONS]):
                run = self.perform_game_loop(quiet)
                if not run:
                    break
        else:
            while True:
                run = self.perform_game_loop(quiet)
                if not run:
                    break
