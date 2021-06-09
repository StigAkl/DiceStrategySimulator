import random


simulations = 50
total_rounds = 0
limit = 6
roll_over = 100
least_rounds = 9999999
max_rounds = 0
for i in range(simulations):
    maxLoseStreak = 0
    rounds = 0
    currentLoseStreak = 0
    while True:
        num = random.randint(0, 1000)

        rounds = rounds +1 
        if num >= roll_over:
            currentLoseStreak = 0
        else:
            currentLoseStreak+=1
        if maxLoseStreak < currentLoseStreak:
            maxLoseStreak = currentLoseStreak

        if maxLoseStreak == limit:
            break

    total_rounds += rounds
    if least_rounds > rounds:
        least_rounds = rounds
    if max_rounds < rounds:
        max_rounds = rounds

print("Average rounds until limit reach: {}".format(total_rounds/simulations))
print("Least rounds until limit reach {}".format(least_rounds))
print("Max rounds until limit reach {}".format(max_rounds))