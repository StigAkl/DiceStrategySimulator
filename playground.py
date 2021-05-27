import random


streak = 0
max_streak=0

roll_over = 970
for i in range(0,5000000):
    if random.randint(0, 1000) <= 970:
        streak+=1
    else:
        streak = 0

    if streak > max_streak: max_streak = streak

print(max_streak)