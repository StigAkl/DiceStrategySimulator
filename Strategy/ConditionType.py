from enum import Enum


class BET_CONDITION_TYPE(Enum):
    streakGreaterThan = 0
    firstStreakOf = 1
    streakLowerThan = 2
    everyStreakOf = 3
    every = 4


class PROFIT_CONDITION_TYPE(Enum):
    greaterThan = 0
    greaterThanOrEqual = 1
    lowerThan = 2
    lowerThanOrEqual = 3
