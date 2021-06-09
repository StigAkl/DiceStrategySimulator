from Strategy.ActionType import ACTION_TYPE

class Action():
    def __init__(self, type: ACTION_TYPE, value = 0):
        self._type = type
        self._value = value