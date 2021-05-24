import random

class Dice:
    def __init__(self, range=(0, 1000), seed=None):
        self.__roll_history = []
        self.__current_value = -1
        self.__lower_range = range[0]
        self.__upper_range = range[1]

        if seed != None : random.seed(seed)

    def roll_dice(self):
        self.__current_value = random.randint(self.__lower_range, self.__upper_range)

    def roll_multiple(self, num_rolls):
        for i in range(num_rolls) : self.__roll_history.append(random.randint(self.__lower_range, self.__upper_range))

    def get_dice_value(self):
        return self.__current_value

    def get_results(self):
        return self.__roll_history