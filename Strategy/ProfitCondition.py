from Strategy.BlockType import BlockType
from Strategy.ConditionType import PROFIT_CONDITION_TYPE
from Strategy.BetType import PROFIT_TYPE
from Strategy.Action import Action


class ProfitCondition():
    def __init__(self, conditionType: PROFIT_CONDITION_TYPE, value: float, profit_type: PROFIT_TYPE, action: Action, block_type: BlockType = BlockType.PROFIT):
        self._conditionType = conditionType
        self._value = value
        self._bet_type = profit_type
        self._action = action
        self._block_type = block_type
