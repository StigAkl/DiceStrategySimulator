from enum import Enum


class ACTION_TYPE(Enum):
    increaseByPercentage = 0
    setBetAmount = 1
    resetBetAmount = 2
    resetWinChance = 3
    setRollOver = 4
