from enum import Enum
class BET_CONDITION_TYPE(Enum):
    streakGreaterThan = 0
    firstStreakOf = 1
    streakLowerThan = 2
    everyStreakOf = 3
    every = 4