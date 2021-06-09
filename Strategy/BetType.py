from enum import Enum


class BET_TYPE(Enum):
    WIN = 0
    LOSE = 1
    BET = 3

class PROFIT_TYPE(Enum):
    PROFIT = 0
    BALANCE = 1
    LOSS = 2