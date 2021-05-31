from Strategy.BlockType import BlockType
from Strategy.ConditionType import BET_CONDITION_TYPE
from Strategy.BetType import BET_TYPE
from Strategy.Action import Action

class BetCondition():
    def __init__(self, conditionType: BET_CONDITION_TYPE, value: str, bet_type: BET_TYPE, action: Action, block_type: BlockType=BlockType.BETS):
        self._conditionType = conditionType
        self._value = value
        self._bet_type = bet_type
        self._action = action
        self._block_type = block_type